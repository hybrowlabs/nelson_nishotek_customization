import frappe
from erpnext.manufacturing.doctype.production_plan.production_plan import ProductionPlan

@frappe.whitelist()
def make_production_plan(sales_order):
    pp_doc = frappe.new_doc("Production Plan")
    pp_doc.get_items_from = "Sales Order"
    pp_doc.append('sales_orders', {
        'sales_order': sales_order,
        'customer': frappe.db.get_value("Sales Order", sales_order, "customer"),
        'sales_order_date': frappe.db.get_value("Sales Order", sales_order, "transaction_date"),
        'grand_total': frappe.db.get_value("Sales Order", sales_order, "grand_total"),
    })

    pp_doc.run_method("get_so_items")
    pp_doc.save(ignore_permissions=True)
    frappe.db.commit()

    # Update Production Plan Items after save
    for item in pp_doc.po_items:
        frappe.db.set_value(
            "Production Plan Item",
            item.name,
            "bom_no",
            item.bom_no,  # Replace with the actual field name you need to update
            # "some_value"   # Replace with the actual value to be set
        )

    frappe.msgprint(f"Production Plan '<a href='/app/production-plan/{pp_doc.name}'>{pp_doc.name}</a>' Created")
