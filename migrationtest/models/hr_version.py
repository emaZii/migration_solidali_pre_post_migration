from odoo import api, fields, models


class HrVersion(models.Model):
    _name = 'hr.version'
    
    contract_id = fields.Many2one('hr.contract', string="Contratto")
    subscription_id = fields.Many2one('sale.order', string="Abbonamento")
