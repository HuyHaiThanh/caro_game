import frappe
from frappe import _
from frappe.utils import cint, validate_email_address

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        frappe.local.login_manager.authenticate(usr, pwd)
        frappe.local.login_manager.post_login()
        
        # Lấy thông tin người chơi
        player = frappe.get_all('Player', filters={'user': frappe.session.user}, fields=['name'])
        
        # Nếu người dùng chưa có hồ sơ người chơi, tạo mới
        if not player:
            create_player_profile(frappe.session.user)
            
        return {"success": True}
    except frappe.AuthenticationError:
        return {"success": False, "error": _("Sai email hoặc mật khẩu")}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist(allow_guest=True)
def register(email, password, display_name):
    try:
        # Kiểm tra email hợp lệ
        if not validate_email_address(email):
            return {"success": False, "error": _("Email không hợp lệ")}
            
        # Kiểm tra email đã tồn tại
        if frappe.db.exists("User", {"email": email}):
            return {"success": False, "error": _("Email đã được sử dụng")}
            
        # Tạo người dùng mới
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": display_name,
            "send_welcome_email": 1,
            "new_password": password,
            "user_type": "Website User"
        })
        user.insert(ignore_permissions=True)
        
        # Thêm vai trò Player
        user.add_roles("Player")
        
        # Tạo hồ sơ người chơi
        create_player_profile(email, display_name)
        
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_player_profile(user, display_name=None):
    """Tạo hồ sơ người chơi mới"""
    if not display_name:
        user_doc = frappe.get_doc("User", user)
        display_name = user_doc.first_name
        
    player = frappe.get_doc({
        "doctype": "Player",
        "user": user,
        "display_name": display_name,
        "rating": 1500,  # Điểm xếp hạng mặc định
        "coins": 1000,   # Số xu ban đầu
        "country": "🇻🇳"  # Quốc gia mặc định
    })
    player.insert(ignore_permissions=True)
    return player