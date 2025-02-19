# Copyright (c) 2025, Hybrowlabs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import formatdate, get_first_day, get_last_day

def execute(filters=None):
    if not filters:
        filters = {}
    
    show_grand_total = filters.get("show_grand_total", 0)
    show_status_wise = filters.get("show_status_wise", 0)
    show_owner_wise = filters.get("show_owner_wise", 0)
    
    if not show_grand_total and not show_status_wise and not show_owner_wise:
        return [], []
    
    columns = get_columns(show_status_wise, show_owner_wise)
    
    if show_status_wise:
        data = get_status_wise_data()
    else:
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

def get_status_wise_data():
    data = []
    months = frappe.db.sql("""
        SELECT DISTINCT DATE_FORMAT(creation, '%Y-%m') AS month 
        FROM `tabOpportunity` 
        ORDER BY month DESC
    """, as_dict=True)
    
    for month in months:
        month_name = formatdate(month.month + "-01", "MMMM YYYY")
        first_day = get_first_day(month.month + "-01")
        last_day = get_last_day(month.month + "-01")
        
        status_totals = frappe.db.sql("""
            SELECT status, SUM(total) as total
            FROM `tabOpportunity`
            WHERE creation BETWEEN %s AND %s
            GROUP BY status
        """, (first_day, last_day), as_dict=True)
        
        row = {
            "month": month_name,
            "open": 0,
            "quotation": 0,
            "converted": 0,
            "lost": 0,
            "closed": 0,
            "grand_total": 0
        }
        
        for status_total in status_totals:
            row[status_total.status.lower()] = status_total.total
            row["grand_total"] += status_total.total
        
        data.append(row)
    
    return data

def get_data(filters, show_grand_total, show_status_wise, show_owner_wise):
    sales_person = filters.get("sales_person")
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    if show_owner_wise:
        owner_data = frappe.db.sql("""
            SELECT DATE_FORMAT(o.creation, '%%M') AS month, o.custom_sales_person AS owner,
                   SUM(o.total) AS balance_enquiry,
                   COALESCE(SUM(q.base_total), 0) AS outgoing
            FROM `tabOpportunity` o
            LEFT JOIN `tabQuotation` q ON o.name = q.opportunity
            WHERE o.custom_sales_person IS NOT NULL
            GROUP BY month, owner
        """, as_dict=True)
        
        for row in owner_data:
            row["grand_total"] = row["balance_enquiry"] + row["outgoing"]
        
        return sorted(owner_data, key=lambda x: month_order.index(x["month"]))
    
    opportunity_data = frappe.db.sql("""
        SELECT DATE_FORMAT(creation, '%%M') AS month, SUM(total) AS balance_enquiry
        FROM `tabOpportunity`
        GROUP BY month
    """, as_dict=True)
    
    quotation_data = frappe.db.sql("""
        SELECT DATE_FORMAT(q.creation, '%%M') AS month, SUM(q.base_total) AS outgoing
        FROM `tabQuotation` q
        LEFT JOIN `tabOpportunity` o ON q.opportunity = o.name
        GROUP BY month
    """, as_dict=True)
    
    opportunity_dict = {row["month"]: row["balance_enquiry"] for row in opportunity_data}
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
