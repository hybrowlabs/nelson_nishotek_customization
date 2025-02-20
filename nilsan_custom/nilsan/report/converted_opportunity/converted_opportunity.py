# Copyright (c) 2025, Hybrowlabs and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import formatdate

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns_for_converted_opportunity()
    data = get_converted_opportunity_data()
    
    return columns, data

def get_columns_for_converted_opportunity():
    return [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
        {"label": "Sales Person", "fieldname": "owner", "fieldtype": "Data", "width": 150},
        {"label": "Balance Enquiry", "fieldname": "balance_enquiry", "fieldtype": "Currency", "width": 150},
        {"label": "Outgoing", "fieldname": "outgoing", "fieldtype": "Currency", "width": 150},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 150}
    ]

def get_converted_opportunity_data():
    converted_data = frappe.db.sql("""
        SELECT DATE_FORMAT(o.creation, '%M') AS month, 
               o.custom_sales_person AS owner,
               SUM(o.total) AS balance_enquiry,
               COALESCE((SELECT SUM(q.base_total) FROM `tabQuotation` q WHERE q.opportunity = o.name AND q.docstatus != 2), 0) AS outgoing,
               SUM(o.total) + COALESCE((SELECT SUM(q.base_total) FROM `tabQuotation` q WHERE q.opportunity = o.name AND q.docstatus != 2), 0) AS grand_total
        FROM `tabOpportunity` o
        WHERE o.status = 'Converted' 
        AND o.custom_sales_person IS NOT NULL
        GROUP BY month, owner
    """, as_dict=True)
    
    return converted_data
