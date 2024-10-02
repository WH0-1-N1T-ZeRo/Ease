from odoo import models, fields
import qrcode
import base64
from io import BytesIO


class ProductTemplate(models.Model):
    _inherit = "product.template"

    qr_code = fields.Binary("QR Code", compute="generate_qr_code")

    def generate_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data("Product Name : ")
                qr.add_data(rec.name)
                qr.add_data(", Price : ")
                qr.add_data(rec.list_price)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.qr_code = qr_image
