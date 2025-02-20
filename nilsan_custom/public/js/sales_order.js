frappe.ui.form.on("Sales Order", {
        refresh: function(frm) {
            setTimeout(() => {
                frm.remove_custom_button("Material Request", "Create");
                frm.remove_custom_button("Request for Raw Materials", "Create");
                frm.remove_custom_button("Project", "Create");
            }, 100);
        // Add custom button only if the status is "To Deliver and Bill"
        if (frm.doc.status == "To Deliver and Bill") {
            frm.add_custom_button(
                __("Generate Production Plan"),
                () => {
                    generate_production_plan(frm);
                },
            );
        }
    }
});

function generate_production_plan(frm) {
    frappe.call({
        method: "nilsan_custom.override.sales_order.make_production_plan",
        args: {
            sales_order: frm.doc.name
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint(__("Production Plan Created Successfully"));
            }
        }
    });
}
