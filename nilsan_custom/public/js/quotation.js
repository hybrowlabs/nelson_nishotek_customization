frappe.ui.form.on('Quotation', {
    refresh: function (frm) {
        // Add custom options under the "Create" dropdown
        frm.add_custom_button(__('Project'), function () {
            frappe.new_doc("Project");
        }, __("Create"));
    }
});
