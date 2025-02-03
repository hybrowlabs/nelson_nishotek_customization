from frappe import _
def get_dashboard_data(data):
    data["non_standard_fieldnames"]["Project"] = "custom_quotation"
    
   
    for transaction in data.get("transactions", []):
        if transaction.get("label") == _("Reference"):
            transaction["items"].append("Project")
            break
    else:
        data["transactions"].append({
            "label": _("Reference"),
            "items": ["Project"],
        })
    
    return data

