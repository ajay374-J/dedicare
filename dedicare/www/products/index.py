import frappe

def get_context(context):
    context.cats = fetch_categories()
    homepage = frappe.get_doc("Homepage", "Homepage")
    context.tag_line = homepage.tag_line
    context.description = homepage.description


def fetch_categories():
    return frappe.db.get_all(
        "Item Group",
        filters={
            "show_in_website": 1,
            "is_group": 1,
            "parent_item_group": "Products",
        },
        fields=[
            "name",
            "image",
            "route",
            "show_in_website",
            "is_group",
            "parent_item_group",
        ],
    )
