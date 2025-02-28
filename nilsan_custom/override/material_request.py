# import frappe
# import json

# @frappe.whitelist()
# def create_purchase_orders(material_request, items):
#     """
#     Creates purchase orders from a Material Request.
#     """
#     try:
#         items = json.loads(items)
#         created = []
#         existing = []

#         for item in items:
#             # Check if PO already exists for this material request and item
#             existing_po = frappe.get_all('Purchase Order Item', 
#                                          filters={'material_request': material_request, 'item_code': item['item_code']}, 
#                                          fields=['parent'])
#             if existing_po:
#                 existing.append({'supplier': item['supplier'], 'po_name': existing_po[0]['parent']})
#                 continue

#             # Create a new Purchase Order
#             po = frappe.get_doc({
#                 'doctype': 'Purchase Order',
#                 'supplier': item['supplier'],
#                 'schedule_date': frappe.utils.nowdate(),
#                 'items': [{
#                     'item_code': item['item_code'],
#                     'schedule_date': frappe.utils.nowdate(),
#                     'qty': item['qty'],
#                     'uom': 'Nos',
#                     'material_request': material_request
#                 }]
#             })
#             po.insert()
#             created.append({'name': po.name, 'supplier': po.supplier})

#         return {'created': created, 'existing': existing}

#     except Exception as e:
#         frappe.log_error(f"Error in create_purchase_orders: {str(e)}", "Purchase Order Error")
#         return {'error': str(e)}


import frappe
import json
from collections import defaultdict

@frappe.whitelist()
def create_purchase_orders(material_request, items):
    """
    Creates consolidated purchase orders from a Material Request by grouping items per supplier.
    """
    try:
        items = json.loads(items)
        created = []
        existing = []
        supplier_items_map = defaultdict(list)

        # Group items by supplier
        for item in items:
            # Check if a PO already exists for this material request and item
            existing_po = frappe.get_all('Purchase Order Item', 
                                         filters={'material_request': material_request, 'item_code': item['item_code']}, 
                                         fields=['parent'])
            if existing_po:
                existing.append({'supplier': item['supplier'], 'po_name': existing_po[0]['parent']})
                continue

            supplier_items_map[item['supplier']].append({
                'item_code': item['item_code'],
                'schedule_date': frappe.utils.nowdate(),
                'qty': item['qty'],
                'uom': 'Nos',
                'material_request': material_request
            })

        # Create POs for each supplier with multiple items
        for supplier, items_list in supplier_items_map.items():
            po = frappe.get_doc({
                'doctype': 'Purchase Order',
                'supplier': supplier,
                'schedule_date': frappe.utils.nowdate(),
                'items': items_list
            })
            po.insert()
            created.append({'name': po.name, 'supplier': supplier})

        return {'created': created, 'existing': existing}

    except Exception as e:
        frappe.log_error(f"Error in create_purchase_orders: {str(e)}", "Purchase Order Error")
        return {'error': str(e)}
