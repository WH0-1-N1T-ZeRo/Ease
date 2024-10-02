# -*- coding: utf-8 -*-
from odoo import http
from requests import request


class CustomQRCodeController(http.Controller):
  @http.route('/shop/add_product_and_checkout/<model("product.template"):product>', type='http', auth="public", website=True)
  def add_product_and_checkout(self, product, **kwargs):
    # Ambil keranjang belanja (cart) pengguna saat ini
    order = request.website.sale_get_order(force_create=1)

    # Tambahkan produk ke keranjang
    order._cart_update(product_id=product.id, add_qty=1)

    # Arahkan langsung ke halaman checkout
    return request.redirect('/shop/cart')
