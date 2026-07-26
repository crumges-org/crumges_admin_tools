from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError

class JournalMoveWizard(models.TransientModel):
    _name = 'journal.move.wizard'
    _description = 'Wizard para trasladar asientos entre diarios'

    new_journal_id = fields.Many2one('account.journal', string='Diario Destino', required=True)
    move_count = fields.Integer(string='Cantidad de Asientos', compute='_compute_move_count')

    @api.depends('new_journal_id')
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(self.env.context.get('active_ids', []))

    def action_apply_move(self):
        # 1. Seguridad estricta
        if not self.env.su and self.env.uid != 1:
            raise AccessError("Solo el superusuario (OdooBot) puede trasladar asientos forzosamente.")

        move_ids = self.env.context.get('active_ids', [])
        if not move_ids:
            return {'type': 'ir.actions.act_window_close'}

        moves = self.env['account.move'].browse(move_ids)
        new_journal = self.new_journal_id

        # 2. Validar que todos los asientos provengan de un mismo diario origen
        old_journals = moves.mapped('journal_id')
        if len(old_journals) > 1:
            raise UserError("Por favor, selecciona asientos que pertenezcan a un único diario de origen. No puedes mezclar asientos de múltiples diarios en un solo traslado.")
        
        old_journal = old_journals[0]
        if old_journal == new_journal:
            raise UserError("El diario destino debe ser diferente al diario origen.")

        for move in moves:
            old_name = move.name
            new_name = old_name

            # 3. Lógica de Resecuenciación del Nombre
            if old_journal.l10n_latam_use_documents and new_journal.l10n_latam_use_documents:
                # Caso Facturas Argentina: Cambiar el Punto de Venta (POS) si aplica
                if old_journal.l10n_ar_afip_pos_number and new_journal.l10n_ar_afip_pos_number:
                    old_pos_str = f"{old_journal.l10n_ar_afip_pos_number:05d}"
                    new_pos_str = f"{new_journal.l10n_ar_afip_pos_number:05d}"
                    if old_pos_str != new_pos_str:
                        new_name = old_name.replace(old_pos_str, new_pos_str, 1)
            elif not old_journal.l10n_latam_use_documents and not new_journal.l10n_latam_use_documents:
                # Caso Interno: Cambiar el prefijo del código corto
                if old_name and old_name.startswith(old_journal.code + '/'):
                    new_name = old_name.replace(f"{old_journal.code}/", f"{new_journal.code}/", 1)

            # 4. Actualizar Nombre y Referencias (Si cambió)
            if new_name != old_name:
                self.env.cr.execute("UPDATE account_move SET name = %s WHERE id = %s", [new_name, move.id])
                self.env.cr.execute("UPDATE account_move_line SET move_name = %s WHERE move_id = %s", [new_name, move.id])
                
                if move.payment_reference == old_name:
                    self.env.cr.execute("UPDATE account_move SET payment_reference = %s WHERE id = %s", [new_name, move.id])
                if move.ref == old_name:
                    self.env.cr.execute("UPDATE account_move SET ref = %s WHERE id = %s", [new_name, move.id])
                    
            # 5. Traslado de Diario (Move + Lines)
            self.env.cr.execute("UPDATE account_move SET journal_id = %s WHERE id = %s", [new_journal.id, move.id])
            self.env.cr.execute("UPDATE account_move_line SET journal_id = %s WHERE move_id = %s", [new_journal.id, move.id])
            
            # 6. Actualización de Cuenta Contable Predeterminada (Liquidez)
            if old_journal.default_account_id and new_journal.default_account_id and old_journal.default_account_id != new_journal.default_account_id:
                self.env.cr.execute("""
                    UPDATE account_move_line 
                    SET account_id = %s 
                    WHERE move_id = %s AND account_id = %s
                """, [new_journal.default_account_id.id, move.id, old_journal.default_account_id.id])
                
            # 7. Rastro de Auditoría
            msg = f"Este asiento fue trasladado forzosamente desde el diario <b>{old_journal.name}</b> al diario <b>{new_journal.name}</b>."
            if new_name != old_name:
                msg += f"<br/>Además, su secuencia fue reescrita de {old_name} a {new_name}."
            move.message_post(body=msg)

        return {'type': 'ir.actions.act_window_close'}
