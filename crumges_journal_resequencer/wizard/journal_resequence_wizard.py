from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError

class JournalResequenceWizard(models.TransientModel):
    _name = 'journal.resequence.wizard'
    _description = 'Wizard de resecuenciación de diarios'

    journal_id = fields.Many2one('account.journal', string='Diario', required=True, readonly=True)
    old_code = fields.Char(string='Código Actual', related='journal_id.code', readonly=True)
    new_code = fields.Char(string='Nuevo Código Corto', required=True, size=5)

    def action_apply_resequence(self):
        # 1. Seguridad estricta: Solo OdooBot (uid=1) o el entorno su
        if not self.env.su and self.env.uid != 1:
            raise AccessError("Solo el superusuario del sistema (OdooBot) puede ejecutar esta acción de resecuenciación destructiva.")

        journal = self.journal_id

        # 1.1 Validaciones de Localización y Tipo de Diario
        if journal.company_id.account_fiscal_country_id.code != 'AR':
            raise UserError("Esta herramienta está diseñada exclusivamente para compañías bajo la localización Argentina.")
        
        if journal.type in ('sale', 'purchase') and journal.l10n_latam_use_documents:
            raise UserError("No se permite resecuenciar diarios de Ventas o Compras que utilizan Documentos Legales de AFIP.")

        if not self.new_code or self.old_code == self.new_code:
            return {'type': 'ir.actions.act_window_close'}

        old_prefix = self.old_code
        new_prefix = self.new_code
        
        # 2. Bypassing ORM para cambiar el código del diario
        self.env.cr.execute("UPDATE account_journal SET code = %s WHERE id = %s", [new_prefix, journal.id])

        # 3. Buscar asientos con el prefijo viejo (inician con viejo_codigo + "/")
        search_domain = [
            ('journal_id', '=', journal.id),
            ('name', '=like', f"{old_prefix}/%")
        ]
        moves = self.env['account.move'].search(search_domain)

        if not moves:
            # Si no hay asientos, simplemente retorna con mensaje
            journal.message_post(body=f"El código corto del diario fue cambiado forzosamente de {old_prefix} a {new_prefix}. No había asientos para resecuenciar.")
            return {'type': 'ir.actions.act_window_close'}

        # 4. Modificar SQL crudo para los asientos y sus líneas
        for move in moves:
            old_name = move.name
            new_name = old_name.replace(f"{old_prefix}/", f"{new_prefix}/", 1)
            
            # Actualizar asiento
            self.env.cr.execute("UPDATE account_move SET name = %s WHERE id = %s", [new_name, move.id])
            # Actualizar move_name en las líneas
            self.env.cr.execute("UPDATE account_move_line SET move_name = %s WHERE move_id = %s", [new_name, move.id])
            
            # Actualizar payment_reference si era igual al viejo nombre
            if move.payment_reference == old_name:
                self.env.cr.execute("UPDATE account_move SET payment_reference = %s WHERE id = %s", [new_name, move.id])
                
            # Actualizar ref si era igual al viejo nombre
            if move.ref == old_name:
                self.env.cr.execute("UPDATE account_move SET ref = %s WHERE id = %s", [new_name, move.id])
                
            # 5. Rastro de Auditoría en Asiento
            move.message_post(body=f"El prefijo de la secuencia fue modificado forzosamente de {old_name} a {new_name}.")

        # 6. Rastro de Auditoría en Diario
        journal.message_post(body=f"El código corto del diario fue cambiado forzosamente de {old_prefix} a {new_prefix} y se resecuenciaron los prefijos de {len(moves)} asientos contables.")

        return {'type': 'ir.actions.act_window_close'}
