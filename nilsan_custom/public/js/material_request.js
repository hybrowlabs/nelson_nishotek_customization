frappe.ui.form.on('Material Request', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Auto Create PO'), function() {
                frappe.call({
                    method: 'frappe.client.get',  // ✅ Fetch entire Material Request
                    args: {
                        doctype: 'Material Request',
                        name: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message) {
                            let items = response.message.items;  // ✅ Access child table properly
                            let fields = [
                                {
                                    fieldname: 'items_table',
                                    fieldtype: 'Table',
                                    label: 'Select Suppliers',
                                    fields: [
                                        { fieldname: 'item_code', fieldtype: 'Data', label: 'Item Code', read_only: 1, in_list_view: 1 },
                                        { fieldname: 'item_name', fieldtype: 'Data', label: 'Item Name', read_only: 1, in_list_view: 1 },
                                        { fieldname: 'qty', fieldtype: 'Float', label: 'Qty', read_only: 1, in_list_view: 1 },
                                        { fieldname: 'supplier', fieldtype: 'Link', label: 'Supplier', options: 'Supplier', reqd: 1, in_list_view: 1 }
                                    ]
                                }
                            ];

                            let dialog = new frappe.ui.Dialog({
                                title: __('Select Supplier for Each Item'),
                                fields: fields,
                                primary_action_label: __('Create PO'),
                                primary_action: function() {
                                    let data = dialog.get_values();
                                    if (!data || !data.items_table || data.items_table.length === 0) {
                                        frappe.msgprint(__('Please select at least one supplier.'));
                                        return;
                                    }

                                    frappe.call({
                                        method: 'nilsan_custom.override.material_request.create_purchase_orders',
                                        args: {
                                            material_request: frm.doc.name,
                                            items: JSON.stringify(data.items_table)  // ✅ Ensure items are JSON formatted
                                        },
                                        callback: function(response) {
                                            let message = '';
                                            if (response.message.created.length > 0) {
                                                message += '<b>' + __('Purchase Orders Created Successfully:') + '</b><br>';
                                                response.message.created.forEach(po => {
                                                    message += `<a href='/app/purchase-order/${po.name}'>${po.name}</a> (Supplier: ${po.supplier})<br>`;
                                                });
                                            }
                                            if (response.message.existing.length > 0) {
                                                message += '<br><b>' + __('Existing Purchase Orders:') + '</b><br>';
                                                response.message.existing.forEach(po => {
                                                    message += `A purchase order for supplier ${po.supplier} has already been created: <a href='/app/purchase-order/${po.po_name}'>${po.po_name}</a><br>`;
                                                });
                                            }
                                            if (response.message.created.length === 0 && response.message.existing.length > 0) {
                                                message = __('All purchase orders for the suppliers have already been created.');
                                            }
                                            frappe.msgprint({
                                                title: __('Purchase Order Creation'),
                                                indicator: 'green',
                                                message: message
                                            });
                                            dialog.hide();
                                        }
                                    });
                                }
                            });

                            // Populate dialog table with items
                            let table = dialog.fields_dict.items_table.df.data = [];
                            items.forEach(item => {
                                table.push({
                                    item_code: item.item_code,
                                    item_name: item.item_name,
                                    qty: item.qty,
                                    supplier: ''  // User must select a supplier
                                });
                            });
                            dialog.fields_dict.items_table.grid.refresh();
                            dialog.show();
                        }
                    }
                });
            });
        }
    }
});
