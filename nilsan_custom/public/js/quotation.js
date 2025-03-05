frappe.ui.form.on("Quotation", {
    refresh: function (frm) {
        // Check if a project already exists for this quotation
        frappe.db.get_value("Project", {"custom_quotation": frm.doc.name}, "name")
            .then(response => {
                let project_exists = response.message.name ? true : false;

                // Hide "Project" button if a project exists or if Quotation is Cancelled
                if (!project_exists && frm.doc.status !== "Cancelled") {
                    frm.add_custom_button(__('Project'), function () {
                        frappe.route_options = {
                            custom_quotation: frm.doc.name,  // Pass Quotation name
                            custom_industry: frm.doc.custom_industry,
                            custom_product_type: frm.doc.custom_product_type,
                            custom_product_segment: frm.doc.custom_product_segment,
                            custom_sub_industry: frm.doc.custom_sub_industry
                            
                        };
                        frappe.new_doc("Project");  // Open new Project form
                    }, __("Create"));
                }
            });

        // Apply filter only when navigating from the "Reference" section
        if (frappe.route_options && frappe.route_options.from_dashboard) {
            frm.set_query("project", function () {
                return {
                    filters: {
                        custom_quotation: frm.doc.name
                    }
                };
            });

            // Reset route options after applying the filter
            delete frappe.route_options.from_dashboard;
        }
    }
});
