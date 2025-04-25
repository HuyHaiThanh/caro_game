import frappe
from frappe import _
from frappe.utils import cint, validate_email_address
import time

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
        
        # Sử dụng khối try-finally để đảm bảo auto_commit được đặt lại
        frappe.db.begin()
        auto_commit_was_on = frappe.db.auto_commit_on_many_writes
        frappe.db.auto_commit_on_many_writes = True
        
        try:
            # Tạo người dùng mới
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": display_name,
                "send_welcome_email": 0,  # Không gửi email xác nhận ngay lập tức
                "new_password": password,
                "user_type": "Website User"
            })
            user.flags.ignore_permissions = True
            user.flags.ignore_password_policy = True
            user.insert()
            
            # Commit ngay sau khi tạo người dùng để tránh deadlock
            frappe.db.commit()
            
            # Thêm vai trò Player
            user.add_roles("Player")
            frappe.db.commit()
            
            # Tạo hồ sơ người chơi
            player = create_player_profile(email, display_name)
            
            # Gửi email chào mừng nếu ở chế độ developer
            if frappe.conf.get('developer_mode'):
                user.send_welcome_email()
                frappe.db.commit()
            
            return {"success": True, "message": "Đăng ký thành công", "user": user.name, "player": player.name}
            
        except Exception as e:
            frappe.db.rollback()
            frappe.log_error(f"Lỗi khi đăng ký: {str(e)}", "Registration Error")
            return {"success": False, "error": _("Có lỗi xảy ra khi đăng ký. Vui lòng thử lại sau.")}
        
        finally:
            # Đặt lại giá trị auto_commit
            frappe.db.auto_commit_on_many_writes = auto_commit_was_on
    
    except Exception as e:
        frappe.log_error(f"Lỗi ngoài cùng khi đăng ký: {str(e)}", "Registration Outer Error")
        return {"success": False, "error": _("Có lỗi xảy ra khi đăng ký. Vui lòng thử lại sau.")}

def create_player_profile(user, display_name=None):
    """Tạo hồ sơ người chơi mới"""
    try:
        if not display_name:
            user_doc = frappe.get_doc("User", user)
            display_name = user_doc.first_name
        
        # Kiểm tra xem hồ sơ người chơi đã tồn tại chưa
        existing_player = frappe.db.exists("Player", {"user": user})
        if existing_player:
            return frappe.get_doc("Player", existing_player)
            
        player = frappe.get_doc({
            "doctype": "Player",
            "user": user,
            "display_name": display_name,
            "rating": 1500,  # Điểm xếp hạng mặc định
            "coins": 1000,   # Số xu ban đầu
            "country": "🇻🇳"  # Quốc gia mặc định
        })
        player.flags.ignore_permissions = True
        player.insert()
        frappe.db.commit()
        return player
    
    except Exception as e:
        frappe.log_error(f"Lỗi khi tạo hồ sơ người chơi: {str(e)}", "Player Profile Error")
        frappe.db.rollback()
        # Không làm gián đoạn luồng đăng ký nếu không tạo được hồ sơ người chơi
        # Người dùng vẫn được tạo, chỉ thiếu hồ sơ người chơi
        return None