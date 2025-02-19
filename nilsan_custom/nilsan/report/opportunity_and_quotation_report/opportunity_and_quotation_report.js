// Copyright (c) 2025, Hybrowlabs and contributors
// For license information, please see license.txt

frappe.query_reports["Opportunity and Quotation Report"] = {
    "filters": [
        {
            "fieldname": "show_grand_total",
            "label": __("Month-wise Grand Total"),
            "fieldtype": "Check",
            "default": 0,
            "on_change": function (query_report) {
                if (frappe.query_report.get_filter_value("show_grand_total")) {
                    frappe.query_report.set_filter_value("show_status_wise", 0);
                    frappe.query_report.set_filter_value("show_owner_wise", 0);
                    frappe.query_report.toggle_filter_display("sales_person", false);
                }
                query_report.refresh();
            }
        },
        {
            "fieldname": "show_status_wise",
            "label": __("Status-wise Grand Total"),
            "fieldtype": "Check",
            "default": 0,
            "on_change": function (query_report) {
                if (frappe.query_report.get_filter_value("show_status_wise")) {
                    frappe.query_report.set_filter_value("show_grand_total", 0);
                    frappe.query_report.set_filter_value("show_owner_wise", 0);
                    frappe.query_report.toggle_filter_display("sales_person", true);
                }
                query_report.refresh();
            }
        },
        {
            "fieldname": "show_owner_wise",
            "label": __("Owner-wise Grand Total"),
            "fieldtype": "Check",
            "default": 0,
            "on_change": function (query_report) {
                if (frappe.query_report.get_filter_value("show_owner_wise")) {
                    frappe.query_report.set_filter_value("show_grand_total", 0);
                    frappe.query_report.set_filter_value("show_status_wise", 0);
                    frappe.query_report.toggle_filter_display("sales_person", true);
                }
                query_report.refresh();
            }
        },
        {
            "fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "hidden": 1 // Initially hidden, shown when checkbox is checked
        }
    ]
};
