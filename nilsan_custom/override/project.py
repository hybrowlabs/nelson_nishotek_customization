import frappe
from frappe import _

def create_warehouse_for_main_project(doc, method):
    if doc.project_type == 'Main' and not doc.is_new():
        warehouse_name = f"{doc.name}"  # Naming convention for the warehouse
        if not frappe.db.exists('Warehouse', warehouse_name):  # Check if the warehouse already exists
            warehouse = frappe.get_doc({
                'doctype': 'Warehouse',
                'warehouse_name': warehouse_name,
                'is_group': 0,  # Set as a non-group warehouse
                'company': doc.company,  # Assuming 'company' field is available in the Project
            })
            warehouse.insert()  # Insert the new warehouse into the database
            frappe.db.commit()  # Commit the transaction

            # Show a success message to the user
            frappe.msgprint(_("Warehouse '{0}' successfully created for project {1}.".format(warehouse_name, doc.name)), alert=True)
