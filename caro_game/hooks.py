app_name = "caro_game"
app_title = "Caro Game"
app_publisher = "HuyB"
app_description = "An onlie Website caro game"
app_email = "huyhaithanh51@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "caro_game",
# 		"logo": "/assets/caro_game/logo.png",
# 		"title": "Caro Game",
# 		"route": "/caro_game",
# 		"has_permission": "caro_game.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/caro_game/css/caro_game.css"
# app_include_js = "/assets/caro_game/js/caro_game.js"

# include js, css files in header of web template
web_include_css = "/assets/caro_game/css/caro.css"
web_include_js = "/assets/caro_game/js/caro.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "caro_game/public/scss/website"

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
# app_include_icons = "caro_game/public/icons.svg"

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

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "caro_game.utils.jinja_methods",
# 	"filters": "caro_game.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "caro_game.install.before_install"
# after_install = "caro_game.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "caro_game.uninstall.before_uninstall"
# after_uninstall = "caro_game.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "caro_game.utils.before_app_install"
# after_app_install = "caro_game.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "caro_game.utils.before_app_uninstall"
# after_app_uninstall = "caro_game.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "caro_game.notifications.get_notification_config"

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
# 		"caro_game.tasks.all"
# 	],
# 	"daily": [
# 		"caro_game.tasks.daily"
# 	],
# 	"hourly": [
# 		"caro_game.tasks.hourly"
# 	],
# 	"weekly": [
# 		"caro_game.tasks.weekly"
# 	],
# 	"monthly": [
# 		"caro_game.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "caro_game.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "caro_game.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "caro_game.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["caro_game.utils.before_request"]
# after_request = ["caro_game.utils.after_request"]

# Job Events
# ----------
# before_job = ["caro_game.utils.before_job"]
# after_job = ["caro_game.utils.after_job"]

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
# 	"caro_game.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Website user home page
# --------------------
website_route_rules = [
    {"from_route": "/caro", "to_route": "caro/index"},
]

# allow guest to access caro game homepage without login
website_guest_access = ["/caro", "/caro/index"]

