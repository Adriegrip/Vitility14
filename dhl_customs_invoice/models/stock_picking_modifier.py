# coding=utf-8
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPickingModifier(models.Model):
    _inherit = "stock.picking"

    tracker_code_ids = fields.One2many("dhl.tracker.code", "picking_id",
                                       string="Tracker Code")
    reason_export = fields.Selection([('permanent/sold', 'Permanent/Sold'), (
        'temporary/tradeshow', 'Temporary/Tradeshow'),
                                      ('unsolicited gift', 'Unsolicited Gift'),
                                      ('for repair', 'For Repair'),
                                      ('warranty', 'Warranty'), (
                                          'commercial sample',
                                          'Commercial Sample'),
                                      ('personal effects', 'Personal Effects'),
                                      ('return shipment', 'Return Shipment')],
                                     string="Reson of Export",
                                     default='permanent/sold')
    export_doc_text = fields.Text(string="Export Document Text")

    def x_button_print_dhl_label(self):
        self.ensure_one()
        res = super(StockPickingModifier, self).button_print_dhl_label()
        if self and self.tracker_code:
            raw_trackers = self.tracker_code.split(';')
            trackers = []
            tracker_lst = []
            if len(raw_trackers > 1):
                for track in raw_trackers:
                    trackers.append(track.replace(" ", ""))
            else:
                trackers.extend(raw_trackers)
            for tracker in trackers:
                tracker_lst.append((0, 0, {
                    'tracker_code': tracker,
                    'picking_id': self.id
                }))
            self.write({
                'tracker_code_ids': tracker_lst
            })
        return res

    def button_print_custom_invoice(self):
        self.ensure_one()
        report_data = {}
        invoice = self.env['account.invoice'].search(
            [('origin', 'ilike', self.origin)])
        if not self.origin or not invoice:
            raise UserError(_(
                "There is no Reference or Invoice provided for this Delivery Order"))

        return self.env['report'].get_action(
            self,
            'dhl_customs_invoice.report_customer_invoice_dhl',
            data=report_data)


class DHLTrackerCode(models.Model):
    _name = "dhl.tracker.code"

    picking_id = fields.Many2one("stock.picking", string="Picking")
    tracker_code = fields.Char("Tracker Code")
    extra_details = fields.Char("Dimensions Colli")
