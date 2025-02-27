import frappe
import json

@frappe.whitelist()
def create_purchase_orders(material_request, items):
    """
    Creates purchase orders from a Material Request.
    """
    try:
        items = json.loads(items)
        created = []
        existing = []

        for item in items:
            # Check if PO already exists for this material request and item
            existing_po = frappe.get_all('Purchase Order Item', 
                                         filters={'material_request': material_request, 'item_code': item['item_code']}, 
                                         fields=['parent'])
            if existing_po:
                existing.append({'supplier': item['supplier'], 'po_name': existing_po[0]['parent']})
                continue

            # Create a new Purchase Order
            po = frappe.get_doc({
                'doctype': 'Purchase Order',
                'supplier': item['supplier'],
                'schedule_date': frappe.utils.nowdate(),
                'items': [{
                    'item_code': item['item_code'],
                    'schedule_date': frappe.utils.nowdate(),
                    'qty': item['qty'],
                    'uom': 'Nos',
                    'material_request': material_request
                }]
            })
            po.insert()
            po.submit()
            created.append({'name': po.name, 'supplier': po.supplier})

        return {'created': created, 'existing': existing}

    except Exception as e:
        frappe.log_error(f"Error in create_purchase_orders: {str(e)}", "Purchase Order Error")
        return {'error': str(e)}
