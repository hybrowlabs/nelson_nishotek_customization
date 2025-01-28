frappe.ui.form.on('Project', {
    refresh: function (frm) {
        // Add custom options under the "Create" dropdown
        frm.add_custom_button(__('Material Request'), function () {
            frappe.new_doc("Material Request");
        }, __("Create"));

        frm.add_custom_button(__('Sales Order'), function () {
            frappe.new_doc("Sales Order");
        }, __("Create"));

        frm.add_custom_button(__('Production Plan'), function () {
            frappe.new_doc("Production Plan");
        }, __("Create"));

        frm.add_custom_button(__('Task'), function () {
            frappe.new_doc("Task");
        }, __("Create"));
    }
});
