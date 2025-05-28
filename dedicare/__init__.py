# -*- coding: utf-8 -*-

from erpnext.utilities import product

__version__ = '0.0.1'


import frappe

from erpnext.stock.doctype.batch.batch import get_batch_qty






def get_qty_in_stock(item_code, item_warehouse_field, warehouse=None):
	in_stock, stock_qty = 0, ''
	template_item_code, is_stock_item = frappe.db.get_value("Item", item_code, ["variant_of", "is_stock_item"])

	if not warehouse:
		warehouse = frappe.db.get_value("Item", item_code, item_warehouse_field)

	if not warehouse and template_item_code and template_item_code != item_code:
		warehouse = frappe.db.get_value("Item", template_item_code, item_warehouse_field)
	if warehouse:
		w_list=[warehouse]
		warehouses=frappe.db.get_all("Warehouse",{"parent_warehouse":warehouse},"name")
		for i in warehouses:
			w_list.append(i.name)

		stock_qty = frappe.db.sql("""
			select GREATEST(S.actual_qty - S.reserved_qty - S.reserved_qty_for_production - S.reserved_qty_for_sub_contract, 0) / IFNULL(C.conversion_factor, 1)
			from tabBin S
			inner join `tabItem` I on S.item_code = I.Item_code
			left join `tabUOM Conversion Detail` C on I.sales_uom = C.uom and C.parent = I.Item_code
			where S.item_code=%s and S.warehouse in %s""", (item_code, set(w_list)))
		stock_qt=0
		if stock_qty:
			stock_qty = adjust_qty_for_expired_items(item_code, stock_qty, w_list)
			for i in stock_qty:
				stock_qt+=i

			in_stock = stock_qt> 0 and 1 or 0

	return frappe._dict({"in_stock": in_stock, "stock_qty": stock_qty, "is_stock_item": is_stock_item})


def adjust_qty_for_expired_items(item_code, stock_qty, warehouse):
	batches = frappe.get_all('Batch', filters=[{'item': item_code}], fields=['expiry_date', 'name'])
	expired_batches = product.get_expired_batches(batches)
	it=0
	for item in stock_qty:
		it+=item[0] 
	stock_qty=list([it])


	for batch in expired_batches:
		if warehouse:
			for kj in warehouse:
				stock_qty[0][0] = max(0, stock_qty[0][0] - get_batch_qty(batch, kj))
		else:
			stock_qty[0][0] = max(0, stock_qty[0][0] - product.qty_from_all_warehouses(get_batch_qty(batch)))

		if not stock_qty[0][0]:
			break

	return stock_qty


product.get_qty_in_stock=get_qty_in_stock

product.adjust_qty_for_expired_items=adjust_qty_for_expired_items