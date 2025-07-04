import frappe
from erpnext.portal.product_configurator.utils import (get_products_for_website, get_product_settings,
	get_field_filter_data, get_attribute_filter_data)

sitemap = 1

def get_context(context):

	if frappe.form_dict:
		search = frappe.form_dict.search
		field_filters = frappe.parse_json(frappe.form_dict.field_filters)
		attribute_filters = frappe.parse_json(frappe.form_dict.attribute_filters)
	else:
		search = field_filters = attribute_filters = None

	context.items = get_products_for_website(field_filters, attribute_filters, search)

	context.wishlist_items = get_wishlist_items()

	product_settings = get_product_settings()
	context.field_filters = get_field_filter_data() \
		if product_settings.enable_field_filters else []

	context.attribute_filters = get_attribute_filter_data() \
		if product_settings.enable_attribute_filters else []

	context.product_settings = product_settings
	context.page_length = product_settings.products_per_page

	context.no_cache = 1

def get_wishlist_items():
    if frappe.session.user == "Guest":
        return

    # A user's wishlist is a document of DocType "Wishlist" with its name being the user's ID
    wishlist_name = frappe.session.user
    if frappe.db.exists("Wishlist", wishlist_name):
        wishlist = frappe.get_doc("Wishlist", wishlist_name)

        # Get a list of item codes already in the wishlist
        wishlist_items = [d.item_code for d in wishlist.get("wishlist_items", [])]
        return wishlist_items
    else:
        return []