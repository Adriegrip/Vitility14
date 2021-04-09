# coding=utf-8
from odoo import api, models, _
from odoo.exceptions import UserError


class DhlCustomerInvoice(models.AbstractModel):
    _name = "report.dhl_customs_invoice.report_customer_invoice_dhl"

    def get_lines_data(self, inv, delivery):
        line_list = []
        for deliv in delivery.move_line_ids_without_package:
            same_product_lines = delivery.move_line_ids_without_package.filtered(
                lambda p: p.product_id.id == deliv.product_id.id)
            total_qty_done = sum([s.qty_done for s in same_product_lines])
            if not any(d['id'] == deliv.product_id.id for d in line_list):
                line = inv.order_line.filtered(
                    lambda l: l.product_id.id == deliv.product_id.id)
                if line:
                    line = line[:1] if len(line) > 1 else line
                    tax = 0.0
                    for tax_line in line.tax_id:
                        amount = tax_line.amount
                        tax += amount
                    total = line.price_subtotal * tax / 100
                    line_list.append({
                        'id': line.product_id.id,
                        'product_id': line.product_id.code,
                        'product_name': line.product_id.name,
                        'qty': total_qty_done,
                        'barcode': line.product_id.barcode,
                        'hs_code': line.product_id.hs_code,
                        'country_of_origin': line.product_id.product_tmpl_id.intrastat_origin_country_id.name,
                        'weight_pr_pc': line.product_id.weight,
                        'price_unit': line.price_unit,
                        'tax': total,
                        'amount_total': line.price_unit * total_qty_done
                    })
        dimension_tmpl_id = self.env.ref('base_dhl.extra_dimension_product')
        weight_tmpl_id = self.env.ref('base_dhl.extra_weight_product')
        product_list = [dimension_tmpl_id.product_variant_id.id,
                        weight_tmpl_id.product_variant_id.id]
        for line_id in inv.order_line:
            if line_id.product_id.id in product_list:
                tax = 0.0
                for tax_line in line_id.tax_id:
                    amount = tax_line.amount
                    tax += amount
                total = line_id.price_subtotal * tax / 100
                line_list.append({
                    'id': line_id.product_id.id,
                    'product_id': line_id.product_id.code,
                    'product_name': line_id.product_id.name,
                    'qty': line_id.qty_delivered,
                    'barcode': line_id.product_id.barcode,
                    'hs_code': line_id.product_id.hs_code,
                    'country_of_origin': line_id.product_id.product_tmpl_id.intrastat_origin_country_id.name,
                    'weight_pr_pc': line_id.product_id.weight,
                    'price_unit': line_id.price_unit,
                    'tax': total,
                    'amount_total': line_id.price_unit * line_id.qty_delivered
                })
        return line_list

    @api.model
    def _get_report_values(self, docids, data=None):
        # report_obj = self.env['report']
        pickings = self.env['stock.picking'].browse(docids)
        delivery_list = []

        for delivery in pickings:
            sale_order = self.env['sale.order'].search(
                [('name', 'ilike', delivery.origin)])
            invoices = sale_order.mapped('invoice_ids')
            if not sale_order:
                raise UserError(
                    _('No Sale Order found as %s order.') % delivery.origin)
            for invoice in sale_order:
                delivery_list.append({
                    'invoice': invoices.name or '',
                    'name': invoice.name,
                    'reference': invoices.name,
                    'due_date': invoices.invoice_date_due,
                    'invoice_date': invoices.invoice_date,
                    'customer_code': invoice.partner_id.ref,
                    'incoterms': invoice.incoterm.code + " - " + delivery.partner_id.city if invoice.incoterm.id else "",
                    'no_of_colli': delivery.number_of_packages,
                    'dimensions': [details.extra_details for details in
                                   delivery.tracker_code_ids],
                    'net_weight': delivery.weight,
                    'gross_weight': delivery.shipping_weight,
                    'lines': self.get_lines_data(invoice, delivery),
                    'currency_id': invoice.currency_id,
                    'reason_export': delivery.reason_export,
                    'export_doc_text': delivery.export_doc_text,

                })

        return {
            'doc_ids': docids,
            'doc_model': self.env['stock.picking'],
            'docs': pickings,
            'datas': delivery_list,
        }
