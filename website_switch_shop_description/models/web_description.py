from odoo import api, fields, models


class Products(models.Model):
    _inherit = 'product.template'

    website_description_text = fields.Text(string='Website description text',
                                           translate=True)

    x_website_description_text = fields.Html(string='Website description',
                                             translate=True)

    x_product_detail_uom_meter = fields.Selection(
        [('MM', ' mm'), ('CM', ' cm'), ('M', ' m')],
        default="CM", string="Afmeting")
    x_product_detail_uom_weight = fields.Selection(
        [('G', ' g'), ('KG', ' kg')],
        default="G",
        string="Gewicht type")
    x_product_detail_uom_weight_2 = fields.Selection(
        [('G', ' g'), ('KG', ' kg')], default="G",
        string="Draagvermogen type")
    x_product_detail_uom_liter = fields.Selection(
        [('ML', ' ml'), ('CL', ' cl')], default="ML",
        string="Inhoud type")
    x_product_detail_uom_m2 = fields.Selection(
        [('CM', ' cm'), ('CM2', ' cm2'), ('M2', ' m2')],
        default="CM2", string="Oppervlakte type")

    x_product_detail_length = fields.Float("Lengte", digits=(12, 2))
    x_product_detail_width = fields.Float("Breedte", digits=(12, 2))
    x_product_detail_height = fields.Float("Hoogte", digits=(12, 2))
    x_product_detail_lxbxh = fields.Char("LxBxH", compute="calculate_area")

    x_product_detail_diameter = fields.Float("Diameter", digits=(12, 2))
    x_product_detail_width_adjust = fields.Float("Verstelbare breedte")
    x_product_detail_width_adjust_max = fields.Float("Verstelbare breedte max")
    x_product_detail_height_adjust = fields.Float("Verstelbare hoogte")
    x_product_detail_height_adjust_max = fields.Float("Verstelbare hoogte max")
    x_product_detail_diameter_inner = fields.Float("Binnen diameter")

    x_product_detail_weight = fields.Float("Gewicht", digits=(12, 2))
    x_product_detail_max_weight = fields.Integer("Draagvermogen")
    x_product_detail_amount = fields.Integer("Inhoud")
    x_product_detail_surface = fields.Float("Oppervlakte")
    x_product_detail_surface_2 = fields.Float("Oppervlakte 2")

    x_product_detail_usage = fields.Many2many('product.group.usage',
                                              string='Productsoort',
                                              help="Sorteer volgende voor het gebruik van het product.")
    x_product_detail_private = fields.Many2one('product.template',
                                               string='SKU2',
                                               help="Product private")

    x_product_detail_opening = fields.Char("Tuit opening", translate=True)
    x_product_detail_elastic = fields.Char("Elastisch", translate=True)
    x_product_detail_point = fields.Char("Punt", translate=True)
    x_product_detail_function = fields.Char("Hand functie", translate=True)
    x_product_detail_angle = fields.Char("Hoek", translate=True)
    x_product_detail_enlarge = fields.Char("Vergroot", translate=True)
    x_product_detail_one_size = fields.Selection([('ja', 'Ja'), ('nee', 'Nee')],
                                                 string="Een maatvoering")
    x_product_detail_assemble = fields.Selection([('ja', 'Ja'), ('nee', 'Nee')],
                                                 string="Assemblage met schroeven")

    x_product_detail_dishwasher = fields.Selection(
        [('Ja', 'Ja'), ('Nee', 'Nee')],
        string="Vaatwasser")
    x_product_detail_dishwashertemp = fields.Selection(
        [('10', '10'), ('15', '15'), ('20', '20'),
         ('25', '25'), ('30', '30'), ('35', '35'),
         ('40', '40'), ('45', '45'), ('50', '50'),
         ('55', '55'), ('60', '60'), ('65', '65'),
         ('70', '70'), ('75', '75'), ('80', '80'),
         ('90', '90'), ('100', '100'), ('105', '105'),
         ('110', '110'), ('115', '115'), ('120', '120'),
         ('125', '125'), ('130', '130')],
        string="Temperatuur")
    x_product_detail_freezer = fields.Selection([('Ja', 'Ja'), ('Nee', 'Nee')],
                                                string="Vriezer")
    x_product_detail_freezertemp = fields.Integer("Temperatuur")
    x_product_detail_microwave = fields.Selection(
        [('Ja', 'Ja'), ('Nee', 'Nee')], string="Magnetron")
    x_product_detail_microwavetemp = fields.Integer(string="Temperatuur")
    x_product_detail_oven = fields.Selection([('Ja', 'Ja'), ('Nee', 'Nee')],
                                             string="Oven")
    x_product_detail_oventemp = fields.Integer("Temperatuur")
    x_product_detail_washer = fields.Selection([('Ja', 'Ja'), ('Nee', 'Nee')],
                                               string="Wasmachine")
    x_product_detail_washertemp = fields.Selection(
        [('10', '10'), ('15', '15'), ('20', '20'),
         ('25', '25'), ('30', '30'), ('35', '35'),
         ('40', '40'), ('45', '45'), ('50', '50'),
         ('55', '55'), ('60', '60'), ('65', '65'),
         ('70', '70'), ('75', '75'), ('80', '80'),
         ('90', '90'), ('100', '100'), ('105', '105'),
         ('110', '110'), ('115', '115'), ('120', '120'),
         ('125', '125'), ('130', '130')],
        string="Temperatuur")
    x_product_detail_food_safe = fields.Char("Voedselveilig", translate=True)
    x_product_detail_warning = fields.Char("Waarschuwing", translate=True)
    x_product_detail_foldable = fields.Selection([('Ja', 'Ja'), ('Nee', 'Nee')],
                                                 string="Opvouwbaar")
    x_product_detail_bendable = fields.Selection([('Ja', 'Ja'), ('Nee', 'Nee')],
                                                 string="Buigbaar")
    x_product_detail_mount = fields.Selection(
        [('Schroeven', 'Schroeven'), ('Zuignappen', 'Zuignappen')],
        string="Bevestiging")
    x_product_detail_autoclaaf = fields.Selection(
        [('Ja', 'Ja'), ('Nee', 'Nee')], string="Autoclaaf")
    x_product_detail_autoclaaftemp = fields.Selection(
        [('10', '10'), ('15', '15'), ('20', '20'),
         ('25', '25'), ('30', '30'), ('35', '35'),
         ('40', '40'), ('45', '45'), ('50', '50'),
         ('55', '55'), ('60', '60'), ('65', '65'),
         ('70', '70'), ('75', '75'), ('80', '80'),
         ('90', '90'), ('100', '100'), ('105', '105'),
         ('110', '110'), ('115', '115'), ('120', '120'),
         ('125', '125'), ('130', '130')],
        string="Temperatuur")
    x_product_detail_lying_down = fields.Selection(
        [('Ja', 'Ja'), ('Nee', 'Nee')], string="Liggend")
    x_product_detail_certificate = fields.Char("Certificaat", translate=True)
    x_product_detail_link_CE = fields.Char("Link CE Markering")
    x_product_detail_link_grune_punkt = fields.Char("Link Grune Punkt")
    x_product_detail_link_pap20 = fields.Char("Link PAP20")
    x_product_detail_link_pap21 = fields.Char("Link PAP21")

    x_product_detail_free_label_1 = fields.Char("UBR beschrijving 1",
                                                translate=True)
    x_product_detail_free_label_2 = fields.Char("UBR beschrijving 2",
                                                translate=True)
    x_product_detail_free_label_3 = fields.Char("UBR beschrijving 3",
                                                translate=True)
    x_product_detail_free_label_4 = fields.Char("UBR beschrijving 4",
                                                translate=True)
    x_product_detail_free_label_5 = fields.Char("UBR beschrijving 5",
                                                translate=True)
    x_product_detail_free_label_6 = fields.Char("UBR beschrijving 6",
                                                translate=True)
    x_product_detail_free_field_1 = fields.Char("UBR Waarde veld 1",
                                                translate=True)
    x_product_detail_free_field_2 = fields.Char("UBR Waarde veld 2",
                                                translate=True)
    x_product_detail_free_field_3 = fields.Char("UBR Waarde veld 3",
                                                translate=True)
    x_product_detail_free_field_4 = fields.Char("UBR Waarde veld 4",
                                                translate=True)
    x_product_detail_free_field_5 = fields.Char("UBR Waarde veld 5",
                                                translate=True)
    x_product_detail_free_field_6 = fields.Char("UBR Waarde veld 6",
                                                translate=True)
    x_product_detail_free_long_text_1 = fields.Text("UBR tekst 1",
                                                    translate=True)
    x_product_detail_free_long_text_2 = fields.Text("UBR tekst 2",
                                                    translate=True)
    x_product_detail_free_long_text_3 = fields.Text("UBR tekst 3",
                                                    translate=True)
    x_product_detail_free_long_text_4 = fields.Text("UBR tekst 4",
                                                    translate=True)
    x_product_detail_free_long_text_5 = fields.Text("UBR tekst 5",
                                                    translate=True)
    x_product_detail_free_long_text_6 = fields.Text("UBR tekst 6",
                                                    translate=True)

    x_product_detail_package_inhoudps = fields.Float(string="Inhoud P/S",
                                                     compute="calculate_vol",
                                                     digits=(15, 5))
    x_product_detail_package_length = fields.Float(string="Verpakking lengte",
                                                   digits=(15, 0))
    x_product_detail_package_width = fields.Float("Verpakking breedte",
                                                  digits=(15, 0))
    x_product_detail_package_height = fields.Float("Verpakking hoogte",
                                                   digits=(15, 0))
    x_product_detail_package_netto_weight = fields.Integer(
        "Verpakking netto gewicht")
    x_product_detail_package_gross_weight = fields.Integer(
        "Verpakking gross gewicht")
    x_product_detail_package_type = fields.Selection(
        [('bag', 'Bag'), ('box', 'Box'), ('card', 'Card'),
         ('label', 'Label'), ('sleeve', 'Sleeve'), ('sticker', 'Sticker')],
        string="Type")
    x_product_detail_package_stansmes = fields.Char("Stansmes")

    x_product_detail_carton_inhoudps = fields.Float(
        string="Omdoos: volume in m3", compute="calculate_carton",
        digits=(15, 5))
    x_product_detail_carton_length = fields.Float(string="Omdoos: lengte in mm",
                                                  digits=(15, 0))
    x_product_detail_carton_width = fields.Float("Omdoos: breedte in mm",
                                                 digits=(15, 0))
    x_product_detail_carton_height = fields.Float("Omdoos: hoogte in mm",
                                                  digits=(15, 0))

    x_product_detail_marketing_qr_link_internal = fields.Char(
        "QR link code intern")
    x_product_detail_marketing_qr_link = fields.Char("QR link web")
    x_product_detail_marketing_ean_link = fields.Char("EAN Link")
    x_product_detail_marketing_extra_info = fields.Char("Extra info")
    x_product_detail_marketing_image_p = fields.Char("Image P")
    x_product_detail_marketing_image_3d = fields.Char("Image 3d")
    x_product_detail_marketing_image_1 = fields.Char("Image 1")
    x_product_detail_marketing_image_2 = fields.Char("Image 2")
    x_product_detail_marketing_image_3 = fields.Char("Image 3")
    x_product_detail_marketing_image_4 = fields.Char("Image 4")
    x_product_detail_marketing_image_5 = fields.Char("Image 5")
    x_product_detail_marketing_image_6 = fields.Char("Image 6")
    x_product_detail_marketing_extra = fields.Text("Extra informatie")
    x_product_detail_marketing_video_status = fields.Char("Video status")

    x_product_detail_uom_meter_uk = fields.Char(string="Engelse maatvoering",
                                                compute="length_calc_uk")
    x_product_detail_uom_weight_uk = fields.Char(string="Engelse maatvoering",
                                                 compute="weight_calc_uk")
    x_product_detail_uom_weight_uk_2 = fields.Char(string="Engelse maatvoering",
                                                   compute="weight_max_calc_uk")
    x_product_detail_uom_liter_uk = fields.Char(string="Engelse maatvoering",
                                                compute="liter_calc_uk")
    x_product_detail_uom_m2_uk = fields.Char(string="Engelse maatvoering",
                                             compute="surface_calc_uk")

    x_product_detail_length_uk = fields.Float(string="Lengte uk",
                                              compute="length_calc_uk",
                                              digits=(12, 2))
    x_product_detail_width_uk = fields.Float(string="Breedte uk",
                                             compute="width_calc_uk",
                                             digits=(12, 2))
    x_product_detail_height_uk = fields.Float(string="Hoogte uk",
                                              compute="height_calc_uk",
                                              digits=(12, 2))
    x_product_detail_lxbxh_uk = fields.Char("LxBxH uk",
                                            compute="calculate_area")

    x_product_detail_diameter_uk = fields.Float(string="Diameter uk",
                                                compute="diameter_calc_uk",
                                                digits=(12, 2))
    x_product_detail_width_adjust_uk = fields.Float(
        string="Verstelbare breedte uk", compute="width_adjust_calc_uk",
        digits=(12, 2))
    x_product_detail_width_adjust_max_uk = fields.Float(
        string="Verstelbare breedte max uk",
        compute="width_adjust_calc_max_uk", digits=(12, 2))
    x_product_detail_height_adjust_uk = fields.Float(
        string="Verstelbare hoogte uk",
        compute="height_adjust_calc_uk", digits=(12, 2))
    x_product_detail_height_adjust_max_uk = fields.Float(
        string="Verstelbare hoogte max uk",
        compute="height_adjust_calc_max_uk", digits=(12, 2))
    x_product_detail_diameter_inner_uk = fields.Float(
        string="Binnen diameter uk",
        compute="diameter_inner_calc_uk", digits=(12, 2))

    x_product_detail_weight_uk = fields.Float(string="Engelse maat",
                                              compute="weight_calc_uk",
                                              digits=(12, 2))
    x_product_detail_max_weight_uk = fields.Float(string="Engelse maat",
                                                  compute="weight_max_calc_uk",
                                                  digits=(12, 2))
    x_product_detail_amount_uk = fields.Float(string="in Inches",
                                              compute="liter_calc_uk",
                                              digits=(12, 2))
    x_product_detail_surface_uk = fields.Float(string="in Inches",
                                               compute="surface_calc_uk",
                                               digits=(12, 2))
    x_product_detail_surface_2_uk = fields.Float(string="in Inches",
                                                 compute="surface_calc_2_uk",
                                                 digits=(12, 2))

    @api.onchange('x_product_detail_package_length',
                  'x_product_detail_package_width',
                  'object.x_product_detail_package_height')
    def calculate_vol(self):
        for object in self:
            object.x_product_detail_package_inhoudps = 0
            object.x_product_detail_package_inhoudps = object.x_product_detail_package_length * \
                                                       object.x_product_detail_package_width * \
                                                       object.x_product_detail_package_height / 1000000000

    @api.onchange('x_product_detail_carton_length',
                  'x_product_detail_carton_width',
                  'object.x_product_detail_carton_height')
    def calculate_carton(self):
        for object in self:
            object.x_product_detail_carton_inhoudps = 0
            object.x_product_detail_carton_inhoudps = object.x_product_detail_carton_length * \
                                                      object.x_product_detail_carton_width * \
                                                      object.x_product_detail_carton_height / 1000000000

    @api.model
    @api.depends('x_product_detail_length', 'x_product_detail_width',
                 'x_product_detail_height')
    def calculate_area(self):
        x_product_detail_lxbxh = " "
        for product_tmpl_rec in self:
            # print("HUiii")
            product_tmpl_rec.x_product_detail_lxbxh = False
            product_tmpl_rec.x_product_detail_lxbxh_uk = False
            if product_tmpl_rec.x_product_detail_length and\
                    product_tmpl_rec.x_product_detail_width and \
                    product_tmpl_rec.x_product_detail_height:
                # print("hihiihi")
                # print("lllll")
                product_tmpl_rec.x_product_detail_lxbxh = str(
                    product_tmpl_rec.x_product_detail_length) + "x" + str(
                    product_tmpl_rec.x_product_detail_width) + "x" + str(
                    product_tmpl_rec.x_product_detail_height)
                product_tmpl_rec.x_product_detail_lxbxh_uk = str(
                    product_tmpl_rec.x_product_detail_length_uk) + "x" + str(
                    product_tmpl_rec.x_product_detail_width_uk) + "x" + str(
                    product_tmpl_rec.x_product_detail_height_uk)

    @api.onchange('x_product_detail_length', 'x_product_detail_uom_meter')
    def length_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_length_uk = object.x_product_detail_length / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_length_uk = object.x_product_detail_length / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_length_uk = object.x_product_detail_length * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_width', 'x_product_detail_uom_meter')
    def width_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_width_uk = object.x_product_detail_width / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_width_uk = object.x_product_detail_width / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_width_uk = object.x_product_detail_width * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_height', 'x_product_detail_uom_meter')
    def height_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_height_uk = object.x_product_detail_height / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_height_uk = object.x_product_detail_height / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_height_uk = object.x_product_detail_height * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_diameter', 'x_product_detail_uom_meter')
    def diameter_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_diameter_uk = object.x_product_detail_diameter / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_diameter_uk = object.x_product_detail_diameter / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_diameter_uk = object.x_product_detail_diameter * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_width_adjust', 'x_product_detail_uom_meter')
    def width_adjust_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_width_adjust_uk = object.x_product_detail_width_adjust / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_width_adjust_uk = object.x_product_detail_width_adjust / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_width_adjust_uk = object.x_product_detail_width_adjust * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_width_adjust_max',
                  'x_product_detail_uom_meter')
    def width_adjust_calc_max_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_width_adjust_max_uk = object.x_product_detail_width_adjust_max / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_width_adjust_max_uk = object.x_product_detail_width_adjust_max / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_width_adjust_max_uk = object.x_product_detail_width_adjust_max * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_height_adjust',
                  'x_product_detail_uom_meter')
    def height_adjust_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_height_adjust_uk = object.x_product_detail_height_adjust / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_height_adjust_uk = object.x_product_detail_height_adjust / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_height_adjust_uk = object.x_product_detail_height_adjust * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_height_adjust_max',
                  'x_product_detail_uom_meter')
    def height_adjust_calc_max_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_height_adjust_max_uk = object.x_product_detail_height_adjust_max / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_height_adjust_max_uk = object.x_product_detail_height_adjust_max / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_height_adjust_max_uk = object.x_product_detail_height_adjust_max * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_diameter_inner',
                  'x_product_detail_uom_meter')
    def diameter_inner_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_meter == 'MM':
                object.x_product_detail_diameter_inner_uk = object.x_product_detail_diameter_inner / 25.4
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'CM':
                object.x_product_detail_diameter_inner_uk = object.x_product_detail_diameter_inner / 2.54
                object.x_product_detail_uom_meter_uk = ' inch'
            if object.x_product_detail_uom_meter == 'M':
                object.x_product_detail_diameter_inner_uk = object.x_product_detail_diameter_inner * 3.281
                object.x_product_detail_uom_meter_uk = ' feet'

    @api.onchange('x_product_detail_weight', 'x_product_detail_uom_weight')
    def weight_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_weight == 'G':
                object.x_product_detail_weight_uk = object.x_product_detail_weight / 28.35
                object.x_product_detail_uom_weight_uk = ' ounce'
            if object.x_product_detail_uom_weight == 'KG':
                object.x_product_detail_weight_uk = object.x_product_detail_weight * 2.204
                object.x_product_detail_uom_weight_uk = ' lbs'

    @api.onchange('x_product_detail_max_weight',
                  'x_product_detail_uom_weight_2')
    def weight_max_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_weight_2 == 'G':
                object.x_product_detail_max_weight_uk = object.x_product_detail_max_weight / 28.35
                object.x_product_detail_uom_weight_uk_2 = ' ounce'
            if object.x_product_detail_uom_weight_2 == 'KG':
                object.x_product_detail_max_weight_uk = object.x_product_detail_max_weight * 2.204
                object.x_product_detail_uom_weight_uk_2 = ' lbs'

    @api.onchange('x_product_detail_amount', 'x_product_detail_uom_liter')
    def liter_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_liter == 'ML':
                object.x_product_detail_amount_uk = object.x_product_detail_amount / 28.413
                object.x_product_detail_uom_liter_uk = ' fl oz'
            if object.x_product_detail_uom_liter == 'CL':
                object.x_product_detail_uom_amount_uk = object.x_product_detail_amount / 2.841
                object.x_product_detail_uom_liter_uk = ' fl oz'

    @api.onchange('x_product_detail_surface', 'x_product_detail_uom_m2_uk')
    def surface_calc_uk(self):
        for object in self:
            if object.x_product_detail_uom_m2 == 'CM':
                object.x_product_detail_surface_uk = object.x_product_detail_surface / 2.54
                object.x_product_detail_uom_m2_uk = ' inch'
            if object.x_product_detail_uom_m2 == 'CM2':
                object.x_product_detail_surface_uk = object.x_product_detail_surface * 15.5
                object.x_product_detail_uom_m2_uk = ' in2'
            if object.x_product_detail_uom_m2 == 'M2':
                object.x_product_detail_surface_uk = object.x_product_detail_surface * 1550
                object.x_product_detail_uom_m3_uk = ' in2'

    @api.onchange('x_product_detail_surface_2', 'x_product_detail_uom_m2_uk')
    def surface_calc_2_uk(self):
        for object in self:
            if object.x_product_detail_uom_m2 == 'CM':
                object.x_product_detail_surface_2_uk = object.x_product_detail_surface_2 / 2.54
            if object.x_product_detail_uom_m2 == 'CM2':
                object.x_product_detail_surface_2_uk = object.x_product_detail_surface_2 * 15.5
            if object.x_product_detail_uom_m2 == 'M2':
                object.x_product_detail_surface_2_uk = object.x_product_detail_surface_2 * 1550


class ProductGroupUsage(models.Model):
    _name = "product.group.usage"
    _description = "Productsoort"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(help="Sorteer volgende voor rapportage gebruik.")
