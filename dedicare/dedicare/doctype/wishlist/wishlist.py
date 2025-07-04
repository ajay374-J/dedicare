# -*- coding: utf-8 -*-
# Copyright (c) 2025, Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


class Wishlist(Document):
    pass


@frappe.whitelist(allow_guest=True)
def toggle_wishlist_item(item):
    """
    Adds or removes an item from the user's wishlist.
    :param item: The item code (website_item) to be added/removed.
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to add items to your wishlist."))

    # A user's wishlist is a document of DocType "Wishlist" with its name being the user's ID
    wishlist_name = frappe.session.user

    if not frappe.db.exists("Wishlist", wishlist_name):
        # Create a new wishlist for the user if it doesn't exist
        wishlist = frappe.new_doc("Wishlist")
        wishlist.user = wishlist_name
        # A Website User role does not have permission to create a Wishlist doc, so ignore permissions
        wishlist.insert(ignore_permissions=True)
    else:
        wishlist = frappe.get_doc("Wishlist", wishlist_name)

    # Get a list of item codes already in the wishlist
    wishlist_items = [d.item_code for d in wishlist.get("wishlist_items", [])]

    if item in wishlist_items:
        # Item is in wishlist, so remove it
        wishlist.wishlist_items = [
            d for d in wishlist.wishlist_items if d.item_code != item
        ]
        action = "removed"
    else:
        # Item is not in wishlist, so add it
        wishlist.append("wishlist_items", {"item_code": item})
        action = "added"

    wishlist.save(ignore_permissions=True)
    frappe.db.commit()  # Commit to see changes reflected immediately

    return {"action": action}


@frappe.whitelist(allow_guest=True)
def get_wishlist_items():
    if frappe.session.user == "Guest":
        return

    # A user's wishlist is a document of DocType "Wishlist" with its name being the user's ID
    wishlist_name = frappe.session.user

    if frappe.db.exists("Wishlist", wishlist_name):
        wishlist = frappe.db.get_list(
            "Wishlist Item",
            filters={"parent": wishlist_name},
            fields=[
                "item_code",
                "item_name",
                "item_route",
                "item_website_image",
                "item_image",
                "item_website_description",
                "item_description",
            ],
        )
        return wishlist
    else:
        return []
