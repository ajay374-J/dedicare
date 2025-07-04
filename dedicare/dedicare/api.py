import frappe


@frappe.whitelist(allow_guest=True)
def fetch_results(search_string):
    like_query = f"%{search_string}%"
    return frappe.db.sql(
        """
        SELECT name, item_code, item_name, brand, item_group, route, image
        FROM `tabItem`
        WHERE show_in_website = 1
        AND (item_code LIKE %s OR item_name LIKE %s)
        """,
        (like_query, like_query),
        as_dict=True,
    )
