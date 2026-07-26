from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    crumges_direct_payment = fields.Boolean(
        string='Pagos directos (Sin cuenta puente)',
        help='Si está marcado, se fuerza a que todos los métodos de pago usen la cuenta principal del diario en lugar de cuentas puente.',
        tracking=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Activar por defecto si es diario de efectivo
        if 'crumges_direct_payment' in fields_list and res.get('type') == 'cash':
            res['crumges_direct_payment'] = True
        return res

    def _get_default_outstanding_account(self, company, is_inbound):
        # 1. Fallback estándar (Odoo 16 hacia atrás)
        if is_inbound and hasattr(company, 'account_journal_payment_debit_account_id') and company.account_journal_payment_debit_account_id:
            return company.account_journal_payment_debit_account_id
        if not is_inbound and hasattr(company, 'account_journal_payment_credit_account_id') and company.account_journal_payment_credit_account_id:
            return company.account_journal_payment_credit_account_id
        
        # 2. Fallback moderno (Odoo 17+ Chart of Accounts Templates)
        xml_id = f"account.{company.id}_base_outstanding_receipts" if is_inbound else f"account.{company.id}_base_outstanding_payments"
        return self.env.ref(xml_id, raise_if_not_found=False)

    @api.onchange('crumges_direct_payment', 'default_account_id')
    def _onchange_crumges_direct_payment(self):
        for journal in self:
            if journal.crumges_direct_payment and journal.default_account_id:
                # Sincronizar métodos de pago entrantes
                for line in journal.inbound_payment_method_line_ids:
                    line.payment_account_id = journal.default_account_id.id
                # Sincronizar métodos de pago salientes
                for line in journal.outbound_payment_method_line_ids:
                    line.payment_account_id = journal.default_account_id.id
            elif not journal.crumges_direct_payment:
                # Revertir usando el fallback estándar de la compañía
                fallback_in = journal._get_default_outstanding_account(journal.company_id, True)
                fallback_out = journal._get_default_outstanding_account(journal.company_id, False)
                for line in journal.inbound_payment_method_line_ids:
                    if line.payment_account_id == journal.default_account_id:
                        line.payment_account_id = fallback_in.id if fallback_in else False
                for line in journal.outbound_payment_method_line_ids:
                    if line.payment_account_id == journal.default_account_id:
                        line.payment_account_id = fallback_out.id if fallback_out else False

    def write(self, vals):
        res = super().write(vals)
        
        # Forzar sincronización al guardar si el switch está activo o inactivo
        if 'crumges_direct_payment' in vals or 'default_account_id' in vals:
            for journal in self:
                if journal.crumges_direct_payment and journal.default_account_id:
                    for line in journal.inbound_payment_method_line_ids:
                        if line.payment_account_id != journal.default_account_id:
                            line.payment_account_id = journal.default_account_id.id
                    for line in journal.outbound_payment_method_line_ids:
                        if line.payment_account_id != journal.default_account_id:
                            line.payment_account_id = journal.default_account_id.id
                elif not journal.crumges_direct_payment:
                    fallback_in = journal._get_default_outstanding_account(journal.company_id, True)
                    fallback_out = journal._get_default_outstanding_account(journal.company_id, False)
                    for line in journal.inbound_payment_method_line_ids:
                        if line.payment_account_id == journal.default_account_id:
                            line.payment_account_id = fallback_in.id if fallback_in else False
                    for line in journal.outbound_payment_method_line_ids:
                        if line.payment_account_id == journal.default_account_id:
                            line.payment_account_id = fallback_out.id if fallback_out else False
        return res
