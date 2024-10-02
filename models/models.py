# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from odoo import models, fields, api
from odoo.exceptions import UserError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.keys import Keys


class Ease(models.Model):
    _name = "ease.ease"
    _description = "Ease"

    client = fields.Char(string="Client", required=True)
    secret = fields.Char(string="Secret", required=True)
    fs = fields.Char(string="FS", required=True)
    shop = fields.Char(string="Shop", required=True)
    type_name = fields.Selection(
        [("tokopedia", "Tokopedia"), ("shopee", "Shopee"), ("blibli", "Blibli")],
        string="Type Name",
        required=True,
    )

    sandbox = fields.Boolean(string="Sandbox", required=True)

    auth_url = fields.Char(string="Auth Url")
    base_url = fields.Char(string="Base Url")
    header = fields.Char(string="Headers")

    def activate(self):
        if self.sandbox:
            raise UserError(self.Sandbox())
        elif self.sandbox == False:
            if self.type_name == "tokopedia":
                self.auth_url = (
                    "https://api.tokopedia.com/v1/oauth/authorize?client_id=%s&response_type=code&redirect_uri=%s"
                    % (self.client, self.base_url)
                )
                return {
                    "type": "ir.actions.act_url",
                    "name": "Auth Tokopedia",
                    "url": self.auth_url,
                }
            elif self.type_name == "shopee":
                self.auth_url = "https://auth.shopeemall.com/login?return_url=%s" % (
                    self.base_url
                )
                return {
                    "type": "ir.actions.act_url",
                    "name": "Auth Shopee",
                    "url": self.auth_url,
                }
            elif self.type_name == "blibli":
                self.auth_url = "https://auth.blibli.com/login?return_url=%s" % (
                    self.base_url
                )
                return {
                    "type": "ir.actions.act_url",
                    "name": "Auth Blibli",
                    "url": self.auth_url,
                }

    def Sandbox(self):
        # Setup Chrome WebDriver menggunakan Selenium
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.delete_all_cookies()

        # Buka URL login Shopee sandbox
        login_url = "https://seller.test-stable.shopee.co.id"
        driver.get(login_url)

        # Tunggu hingga halaman login termuat
        wait = WebDriverWait(driver, 20)

        try:
            # Cari input dengan placeholder "No. Handphone/Username/Email" dan "Password"
            username_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "input[placeholder='No. Handphone/Username/Email']",
                    )
                )
            )
            password_field = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='Password']")
                )
            )

            # Bersihkan semua cookie
            # Isi field username dan password
            username_field.send_keys("SANDBOX.24b5a2bab7f51edb5677")
            password_field.send_keys("3580f4f8f7b3ec60")

            # Tekan tombol login
            password_field.send_keys(Keys.RETURN)

            # Tunggu proses login dan halaman dashboard
            sleep(5)  # Tingkatkan waktu tunggu jika perlu

            # Arahkan ke halaman produk setelah login berhasil
            product_url = "https://seller.test-stable.shopee.co.id/portal/product/list"
            driver.get(product_url)

            # Tunggu hingga halaman produk termuat
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='product-list']")
                )
            )

            # Ambil data semua produk dari halaman
            products = driver.find_elements(By.XPATH, "//div[@class='product-item']")

            # Simpan data produk dalam list
            product_data = []
            for product in products:
                try:
                    # Ambil ID Produk
                    product_id = product.find_element(
                        By.XPATH, ".//input[@class='shopee-checkbox__input']"
                    ).get_attribute("value")
                    print(f"ID Produk: {product_id}")  # Debugging

                    # Ambil Nama Produk
                    product_name = product.find_element(
                        By.XPATH, ".//a[@class='product-name-wrap']/span"
                    ).text
                    print(f"Nama Produk: {product_name}")  # Debugging

                    # Ambil Harga Produk
                    product_price = product.find_element(
                        By.XPATH, ".//span[contains(@class, 'price')]"
                    ).text
                    print(f"Harga Produk: {product_price}")  # Debugging

                    # Ambil Stok Produk
                    product_stock = product.find_element(
                        By.XPATH, ".//span[@class='stock-text']"
                    ).text
                    print(f"Stok Produk: {product_stock}")  # Debugging

                    # Ambil URL Gambar Produk
                    product_image_url = product.find_element(
                        By.XPATH, ".//img"
                    ).get_attribute("src")
                    print(f"URL Gambar Produk: {product_image_url}")  # Debugging

                    # Tambahkan data produk ke list
                    product_data.append(
                        {
                            "id": product_id,
                            "name": product_name,
                            "price": product_price,
                            "stock": product_stock,
                            "image_url": product_image_url,
                        }
                    )

                except Exception as e:
                    print(
                        f"Error extracting product data: {str(e)}"
                    )  # Log kesalahan untuk setiap produk

            # Tutup browser setelah selesai scraping
            driver.quit()

            # Kembalikan data produk
            return product_data

        except Exception as e:
            driver.quit()  # Pastikan browser ditutup jika terjadi error
            raise UserError(f"Terjadi kesalahan saat scraping: {str(e)}")

    def Sandbox2(self):
        return ""
        # Info akun sandbox Shopee
        shop_id = "124493"
        login_url = "https://seller.test-stable.shopee.co.id"

        # Contoh scraping sederhana menggunakan requests dan BeautifulSoup
        session = requests.Session()

        # Simulasi login ke Shopee sandbox (ini perlu disesuaikan dengan mekanisme Shopee jika ada token/cookie)
        payload = {
            "username": "SANDBOX.24b5a2bab7f51edb5677",
            "password": "3580f4f8f7b3ec60",
        }

        response = session.post(login_url, data=payload)
        if response.status_code != 200:
            raise UserError("Login failed!")

        # Scrape data produk dari halaman Shopee
        product_url = (
            f"https://seller.test-stable.shopee.co.id/api/v1/shop/{shop_id}/products"
        )
        product_response = session.get(product_url)

        if product_response.status_code == 200:
            products = product_response.json().get("products", [])
            # Mengolah data produk yang di-scrape
            for product in products:
                product_name = product.get("name")
                product_stock = product.get("stock")
                product_price = product.get("price")
                # Bisa menyimpan ke Odoo atau logika lainnya
                print(
                    f"Product: {product_name}, Stock: {product_stock}, Price: {product_price}"
                )
        else:
            raise UserError("Failed to retrieve products!")

        # Tambah product baru (ini simulasi, sesuaikan dengan API Shopee sandbox jika diperlukan)
        new_product_payload = {"name": "New Product", "price": 10000, "stock": 50}

        add_product_url = f"https://seller.test-stable.shopee.co.id/api/v1/shop/{shop_id}/products/new"
        add_product_response = session.post(add_product_url, json=new_product_payload)

        if add_product_response.status_code == 200:
            print("New product added successfully!")
        else:
            raise UserError("Failed to add new product!")

        return "Scraping and product addition completed!"


class Order(models.Model):
    _name = "ease.order"
    _description = "Data Order With Client"

    market_place = fields.Many2one("ease.ease", string="Market Place", required=True)
    city = fields.Char(string="City", required=True)
    product = fields.Many2many("product.product", string="Products", required=True)
