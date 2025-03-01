# import frappe
# import json
# from collections import defaultdict

# @frappe.whitelist()
# def create_purchase_orders(material_request, items):
#     """
#     Creates consolidated purchase orders from a Material Request by grouping items per supplier.
#     """
#     try:
#         items = json.loads(items)
#         created = []
#         existing = []
#         supplier_items_map = defaultdict(list)

#         # Group items by supplier
#         for item in items:
#             # Check if a PO already exists for this material request and item
#             existing_po = frappe.get_all('Purchase Order Item', 
#                                          filters={'material_request': material_request, 'item_code': item['item_code']}, 
#                                          fields=['parent'])
#             if existing_po:
#                 existing.append({'supplier': item['supplier'], 'po_name': existing_po[0]['parent']})
#                 continue

#             supplier_items_map[item['supplier']].append({
#                 'item_code': item['item_code'],
#                 'schedule_date': frappe.utils.nowdate(),
#                 'qty': item['qty'],
#                 'uom': 'Nos',
#                 'material_request': material_request
#             })

#         # Create POs for each supplier with multiple items
#         for supplier, items_list in supplier_items_map.items():
#             po = frappe.get_doc({
#                 'doctype': 'Purchase Order',
#                 'supplier': supplier,
#                 'schedule_date': frappe.utils.nowdate(),
#                 'items': items_list,
#             })
#             po.insert()
#             created.append({'name': po.name, 'supplier': supplier})

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
    Ensures suppliers have a Payment Terms Template before creating POs.
    """
    try:
        items = json.loads(items)
        created = []
        existing = []
        supplier_items_map = defaultdict(list)

        # Fetch the custom_project from the Material Request
        material_request_doc = frappe.get_doc("Material Request", material_request)
        custom_project = material_request_doc.custom_project if hasattr(material_request_doc, 'custom_project') else None

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
                'material_request': material_request,
                'project': custom_project  # Assign custom_project to item as project
            })

        # Create POs for each supplier with multiple items
        for supplier, items_list in supplier_items_map.items():
            # Check if the supplier has a Payment Terms Template
            supplier_doc = frappe.get_doc("Supplier", supplier)
            if not supplier_doc.payment_terms:
                frappe.throw(f"Supplier {supplier} does not have a Payment Terms Template. Cannot create Purchase Order.")

            # Create the Purchase Order
            po = frappe.get_doc({
                'doctype': 'Purchase Order',
                'supplier': supplier,
                'schedule_date': frappe.utils.nowdate(),
                'project': custom_project,  # Assign custom_project to PO as project
                'items': items_list,
            })
            po.insert()
            created.append({'name': po.name, 'supplier': supplier})

        return {'created': created, 'existing': existing}

    except Exception as e:
        frappe.log_error(f"Error in create_purchase_orders: {str(e)}", "Purchase Order Error")
        return {'error': str(e)}
