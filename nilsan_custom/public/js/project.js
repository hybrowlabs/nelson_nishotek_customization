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
        // frm.add_custom_button(__('Material Request'), function () {
        //     create_new_doc("Material Request", "custom_project");
        // }, __("Create"));

        // frm.add_custom_button(__('Sales Order'), function () {
        //     create_new_doc("Sales Order", "project");
        // }, __("Create"));

        // frm.add_custom_button(__('Production Plan'), function () {
        //     create_new_doc("Production Plan", "project");
        // }, __("Create"));

        frm.add_custom_button(__('Task'), function () {
            create_new_doc("Task", "project");
        }, __("Create"));
    },

    status: function (frm) {
        if (frm.doc.status === 'On Hold') {
            if (!frm.doc.custom_on_hold_from || !frm.doc.custom_on_hold_to) {
                frappe.prompt([
                    {
                        fieldname: 'from_date',
                        label: 'On Hold From',
                        fieldtype: 'Date',
                        reqd: 1
                    },
                    {
                        fieldname: 'to_date',
                        label: 'On Hold To',
                        fieldtype: 'Date',
                        reqd: 1
                    }
                ],
                function (values) {
                    frm.set_value('custom_on_hold_from', values.from_date);
                    frm.set_value('custom_on_hold_to', values.to_date);
                    frm.set_value('status', 'On Hold'); // Ensure status stays "On Hold"
                    frm.refresh_field('custom_on_hold_from');
                    frm.refresh_field('custom_on_hold_to');
                    frm.refresh_field('status');
                },
                'Enter On Hold Dates',
                'Set');
            }
        } else {
            // If status is changed to anything other than 'On Hold', remove the dates
            frm.set_value('custom_on_hold_from', '');
            frm.set_value('custom_on_hold_to', '');
            frm.refresh_field('custom_on_hold_from');
            frm.refresh_field('custom_on_hold_to');
        }
    },

    before_save: function (frm) {
        // Prevent status from changing if it's on hold
        if (frm.doc.custom_on_hold_from && frm.doc.custom_on_hold_to) {
            frm.set_value('status', 'On Hold');
        }
    },

    after_save: function (frm) {
        // Ensure status remains "On Hold" after saving
        if (frm.doc.custom_on_hold_from && frm.doc.custom_on_hold_to) {
            frappe.db.set_value(frm.doctype, frm.doc.name, 'status', 'On Hold');
        }
    }
});
