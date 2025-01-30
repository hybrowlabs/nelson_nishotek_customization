frappe.ui.form.on('Project', {
    refresh: function (frm) {
        // Function to create a new document and set the project field
        function create_new_doc(doctype, project_field) {
            frappe.model.with_doctype(doctype, () => {
                let new_doc = frappe.model.get_new_doc(doctype);
                new_doc[project_field] = frm.doc.name;
                frappe.set_route("Form", doctype, new_doc.name);
            });
        }

        // Add custom options under the "Create" dropdown
        frm.add_custom_button(__('Material Request'), function () {
            create_new_doc("Material Request", "custom_project");
        }, __("Create"));

        frm.add_custom_button(__('Sales Order'), function () {
            create_new_doc("Sales Order", "project");
        }, __("Create"));

        frm.add_custom_button(__('Production Plan'), function () {
            create_new_doc("Production Plan", "project");
        }, __("Create"));

        frm.add_custom_button(__('Task'), function () {
            create_new_doc("Task", "project");
        }, __("Create"));
    },
});
