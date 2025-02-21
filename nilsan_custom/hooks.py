app_name = "nilsan_custom"
app_title = "Nilsan"
app_publisher = "Hybrowlabs"
app_description = "Customization of nilsan-nishotech."
app_email = "pragati@mail.hybrowlabs.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "nilsan_custom",
# 		"logo": "/assets/nilsan_custom/logo.png",
# 		"title": "Nilsan",
# 		"route": "/nilsan_custom",
# 		"has_permission": "nilsan_custom.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nilsan_custom/css/nilsan_custom.css"
# app_include_js = "/assets/nilsan_custom/js/nilsan_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/nilsan_custom/css/nilsan_custom.css"
# web_include_js = "/assets/nilsan_custom/js/nilsan_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nilsan_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "nilsan_custom/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "nilsan_custom.utils.jinja_methods",
# 	"filters": "nilsan_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "nilsan_custom.install.before_install"
# after_install = "nilsan_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "nilsan_custom.uninstall.before_uninstall"
# after_uninstall = "nilsan_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "nilsan_custom.utils.before_app_install"
# after_app_install = "nilsan_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "nilsan_custom.utils.before_app_uninstall"
# after_app_uninstall = "nilsan_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nilsan_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"nilsan_custom.tasks.all"
# 	],
# 	"daily": [
# 		"nilsan_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"nilsan_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"nilsan_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"nilsan_custom.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "nilsan_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "nilsan_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "nilsan_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["nilsan_custom.utils.before_request"]
# after_request = ["nilsan_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["nilsan_custom.utils.before_job"]
# after_job = ["nilsan_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"nilsan_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


doctype_js = {
    "Project": "public/js/project.js",
    "Quotation": "public/js/quotation.js",
    "Sales Order": "public/js/sales_order.js",
    }



# app_include_js = "nilsan_custom/js/sales_order.js"



doc_events = {
    "Project": {
        "after_insert": "nilsan_custom.override.project.create_warehouse_for_main_project"
    }
}




override_doctype_class = {
	"Project": "nilsan_custom.override.project.project_on_hold",
}


override_doctype_dashboards = {
    "Quotation": "nilsan_custom.override.quotation_dashboard.get_dashboard_data",
}


# override_whitelisted_methods = {
#     "erpnext.manufacturing.doctype.production_plan.production_plan.ProductionPlan.make_material_request": 
#     "nilsan_custom.override.production_plan.custom_make_material_request"
# }
