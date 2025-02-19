# Copyright (c) 2025, Hybrowlabs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate

def execute(filters=None):
    if not filters:
        filters = {}
    
    show_grand_total = filters.get("show_grand_total", 0)
    show_status_wise = filters.get("show_status_wise", 0)
    show_owner_wise = filters.get("show_owner_wise", 0)
    
    if not show_grand_total and not show_status_wise and not show_owner_wise:
        return [], []
    
    columns = get_columns(show_status_wise, show_owner_wise)
    data = get_data(filters, show_grand_total, show_status_wise, show_owner_wise)
    return columns, data

def get_columns(show_status_wise, show_owner_wise):
    if show_status_wise:
        return [
            {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
            {"label": "Open", "fieldname": "open", "fieldtype": "Currency", "width": 120},
            {"label": "Quotation", "fieldname": "quotation", "fieldtype": "Currency", "width": 120},
            {"label": "Converted", "fieldname": "converted", "fieldtype": "Currency", "width": 120},
            {"label": "Lost", "fieldname": "lost", "fieldtype": "Currency", "width": 120},
            {"label": "Closed", "fieldname": "closed", "fieldtype": "Currency", "width": 120},
            {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 150}
        ]
    elif show_owner_wise:
        return [
            {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
            {"label": "Owner", "fieldname": "owner", "fieldtype": "Data", "width": 150},
            {"label": "Balance Enquiry", "fieldname": "balance_enquiry", "fieldtype": "Currency", "width": 150},
            {"label": "Outgoing", "fieldname": "outgoing", "fieldtype": "Currency", "width": 150},
            {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 150}
        ]
    else:
        return [
            {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
            {"label": "Balance Enquiry", "fieldname": "balance_enquiry", "fieldtype": "Currency", "width": 150},
            {"label": "Outgoing", "fieldname": "outgoing", "fieldtype": "Currency", "width": 150},
            {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 150}
        ]

def get_data(filters, show_grand_total, show_status_wise, show_owner_wise):
    sales_person = filters.get("sales_person")
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    if show_owner_wise:
        owner_data = frappe.db.sql("""
            SELECT DATE_FORMAT(o.creation, '%M') AS month, o.custom_sales_person AS owner,
                   SUM(o.total) AS balance_enquiry,
                   COALESCE(SUM(q.base_total), 0) AS outgoing
            FROM `tabOpportunity` o
            LEFT JOIN `tabQuotation` q ON o.name = q.opportunity
            WHERE o.custom_sales_person IS NOT NULL
            GROUP BY month, owner
        """, as_dict=True)
        
        report_data = []
        for row in owner_data:
            row["grand_total"] = row["balance_enquiry"] + row["outgoing"]
            report_data.append(row)
        
        return sorted(report_data, key=lambda x: month_order.index(x["month"]))
    
    opportunity_filters = {}
    if sales_person:
        opportunity_filters["custom_sales_person"] = sales_person
    
    opportunity_data = frappe.db.sql("""
        SELECT DATE_FORMAT(creation, '%%M') AS month, SUM(total) AS balance_enquiry
        FROM `tabOpportunity`
        WHERE {condition}
        GROUP BY month
    """.format(condition=" AND ".join(["1=1"] + [f"{key}=%({key})s" for key in opportunity_filters])),
    opportunity_filters, as_dict=True)
    
    opportunity_dict = {row["month"]: row["balance_enquiry"] for row in opportunity_data}
    
    quotation_filters = {}
    if sales_person:
        quotation_filters["o.custom_sales_person"] = sales_person
    
    quotation_data = frappe.db.sql("""
        SELECT DATE_FORMAT(q.creation, '%%M') AS month, SUM(q.base_total) AS outgoing
        FROM `tabQuotation` q
        LEFT JOIN `tabOpportunity` o ON q.opportunity = o.name
        WHERE {condition}
        GROUP BY month
    """.format(condition=" AND ".join(["1=1"] + [f"{key}=%({key})s" for key in quotation_filters])),
    quotation_filters, as_dict=True)
    
    quotation_dict = {row["month"]: row["outgoing"] for row in quotation_data}
    all_months = set(opportunity_dict.keys()).union(set(quotation_dict.keys()))
    report_data = []
    
    for month in sorted(all_months, key=lambda m: month_order.index(m) if m in month_order else 12):
        balance_enquiry = opportunity_dict.get(month, 0)
        outgoing = quotation_dict.get(month, 0)
        grand_total = balance_enquiry + outgoing
        
        report_data.append({
            "month": month,
            "balance_enquiry": balance_enquiry,
            "outgoing": outgoing,
            "grand_total": grand_total
        })
    
    return report_data
