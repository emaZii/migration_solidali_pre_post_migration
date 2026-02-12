from odoo import api, fields, models

class Contract(models.Model):
    _inherit = 'hr.contract'

    #subscription_id = fields.Many2one('sale.order', string="Abbonamento")

    
    @api.constrains('employee_id', 'state', 'kanban_state', 'date_start', 'date_end')
    def _check_current_contract(self):
        return True

    def _generate_work_entries(self, date_start, date_stop, force=False):
        for contract in self:
            res = super(Contract, contract)._generate_work_entries(date_start, date_stop, force)
            for work_entry in res:
                work_entry.contract_id = contract.id
                work_entry.subscription_id = contract.subscription_id.id    
        return res
