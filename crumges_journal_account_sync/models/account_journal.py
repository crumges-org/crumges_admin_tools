from odoo import models

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def write(self, vals):
        # Primero ejecutamos el write original
        res = super().write(vals)
        
        # Si se cambió el nombre, sincronizamos la cuenta para los diarios de liquidez
        if 'name' in vals:
            liquidity_journals = self.filtered(lambda j: j.type in ('bank', 'cash') and j.default_account_id)
            for journal in liquidity_journals:
                if journal.default_account_id.name != journal.name:
                    journal.default_account_id.name = journal.name
                    
        return res
