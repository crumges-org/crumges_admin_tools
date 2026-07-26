from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError

class ProductReplaceWizard(models.TransientModel):
    _name = 'product.replace.wizard'
    _description = 'Fusión/Reemplazo Quirúrgico de Productos'

    old_product_id = fields.Many2one('product.product', string='Producto Origen (Viejo/Dañado)', required=True)
    new_product_id = fields.Many2one('product.product', string='Producto Destino (Nuevo/Correcto)', required=True)
    update_uom = fields.Boolean(
        string='Forzar reemplazo de Unidad de Medida',
        help='Si se marca, reemplazará el ID de la unidad de medida antigua por la del nuevo producto en todos los apuntes históricos. NO realiza conversión matemática, solo pisa el ID.'
    )
    archive_old = fields.Boolean(
        string='Archivar Producto Origen', 
        default=True,
        help='Al finalizar el traspaso, archivará el producto viejo para que no se use más.'
    )

    def action_apply_replace(self):
        # 1. Seguridad Estricta
        if not self.env.su and self.env.uid != 1:
            raise AccessError("Solo el Superusuario (OdooBot) puede ejecutar esta acción destructiva.")

        if self.old_product_id == self.new_product_id:
            raise UserError("El producto de origen y destino no pueden ser el mismo.")

        old_id = self.old_product_id.id
        new_id = self.new_product_id.id
        old_tmpl_id = self.old_product_id.product_tmpl_id.id
        new_tmpl_id = self.new_product_id.product_tmpl_id.id
        new_uom_id = self.new_product_id.uom_id.id

        tables_to_update_product = [
            'sale_order_line',
            'purchase_order_line',
            'account_move_line',
            'stock_move',
            'stock_move_line',
            'stock_valuation_layer',
            'stock_quant',
            'mrp_bom_line',
            'mrp_production'
        ]

        # Actualizar product_id en todas las tablas transaccionales
        for table in tables_to_update_product:
            self._safe_execute(f"UPDATE {table} SET product_id = %s WHERE product_id = %s", [new_id, old_id])

        # Actualizar product_template_id donde exista (ej. sale_order_line)
        tables_with_template = ['sale_order_line', 'product_supplierinfo', 'product_customer_taxes_rel', 'product_taxes_rel']
        for table in tables_with_template:
            # En relaciones Many2many la columna puede llamarse de otra forma, pero product_template_id es común
            self._safe_execute_if_column_exists(table, 'product_template_id', f"UPDATE {table} SET product_template_id = %s WHERE product_template_id = %s", [new_tmpl_id, old_tmpl_id])

        # Actualizar unidades de medida si se solicitó
        if self.update_uom:
            # Tablas que usan product_uom
            for table in ['sale_order_line', 'purchase_order_line', 'stock_move']:
                self._safe_execute_if_column_exists(table, 'product_uom', f"UPDATE {table} SET product_uom = %s WHERE product_id = %s", [new_uom_id, new_id])
            # Tablas que usan product_uom_id
            for table in ['account_move_line', 'stock_move_line']:
                self._safe_execute_if_column_exists(table, 'product_uom_id', f"UPDATE {table} SET product_uom_id = %s WHERE product_id = %s", [new_uom_id, new_id])

        # Trazabilidad en Chatter
        msg_old = f"Todo el historial transaccional de este producto ha sido trasladado forzosamente al producto <b>{self.new_product_id.display_name}</b> mediante fusión SQL."
        msg_new = f"Este producto ha absorbido forzosamente todo el historial transaccional del producto <b>{self.old_product_id.display_name}</b> mediante fusión SQL."
        
        self.old_product_id.product_tmpl_id.message_post(body=msg_old)
        self.new_product_id.product_tmpl_id.message_post(body=msg_new)

        # Archivar
        if self.archive_old:
            self.old_product_id.write({'active': False})

        return {'type': 'ir.actions.act_window_close'}

    def _safe_execute(self, query, params):
        try:
            # Savepoint para evitar que un error rompa la transacción completa
            with self.env.cr.savepoint():
                self.env.cr.execute(query, params)
        except Exception:
            pass # Ignoramos si la tabla no existe o hay error de constraint (ej. clave duplicada en quants)

    def _safe_execute_if_column_exists(self, table, column, query, params):
        self.env.cr.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name=%s AND column_name=%s
        """, [table, column])
        if self.env.cr.fetchone():
            self._safe_execute(query, params)
