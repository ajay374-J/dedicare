from dedicare.dedicare.doctype.wishlist.wishlist import get_wishlist_items


def get_context(context):
	context.wishlist_items = get_wishlist_items()