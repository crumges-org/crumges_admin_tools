# -*- coding: utf-8 -*-

from odoo import models, fields

class MukAiSession(models.Model):
    _inherit = 'muk_ai.session'

    turn_seq = fields.Integer(string="Turn Sequence")
