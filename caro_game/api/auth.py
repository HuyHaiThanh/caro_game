import frappe
from frappe import _
from frappe.utils import cint, validate_email_address
import time
import re

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        # Chuẩn hóa email
        usr = usr.strip().lower() if usr else usr
        
        # Kiểm tra xem người dùng có tồn tại không
        if not frappe.db.exists("User", {"email": usr}):
            return {"success": False, "error": _("Email này chưa được đăng ký")}
        
        # Đảm bảo cơ sở dữ liệu đã commit tất cả các thay đổi trước đó
        frappe.db.commit()
        
        # Chờ một chút để đảm bảo người dùng đã được tạo hoàn toàn
        time.sleep(0.5)
        
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
    except frappe.DoesNotExistError:
        return {"success": False, "error": _("Email này chưa được đăng ký")}
    except Exception as e:
        frappe.log_error(f"Lỗi đăng nhập: {str(e)}", "Login Error")
        return {"success": False, "error": _("Đã xảy ra lỗi khi đăng nhập. Vui lòng thử lại.")}

@frappe.whitelist(allow_guest=True)
def register(email, password, display_name):
    try:
        # Kiểm tra email hợp lệ
        if not validate_email_address(email):
            return {"success": False, "error": _("Email không hợp lệ")}
            
        # Chuẩn hóa email
        email = email.strip().lower()
        
        # Đảm bảo rằng transaction hiện tại đã được xử lý
        frappe.db.commit()
        
        # Kiểm tra xem email đã tồn tại chưa
        user_exists = None
        try:
            user_exists = frappe.db.get_value("User", {"email": email}, ["name", "creation"])
        except:
            pass
            
        if user_exists:
            user_name, creation_time = user_exists if isinstance(user_exists, (list, tuple)) else (user_exists, None)
            
            # Kiểm tra xem người dùng đã được tạo gần đây chưa (trong vòng 5 phút)
            if creation_time:
                time_diff = frappe.utils.time_diff_in_seconds(frappe.utils.now(), creation_time)
                if time_diff < 300:  # 5 phút
                    # Kiểm tra xem đã có hồ sơ người chơi chưa
                    player = frappe.db.exists("Player", {"user": email})
                    
                    if not player:
                        # Tạo hồ sơ người chơi nếu chưa có
                        try:
                            player = create_player_profile(email, display_name)
                        except:
                            pass
                            
                    # Báo thành công để frontend tự đăng nhập
                    return {
                        "success": True,
                        "message": _("Tài khoản của bạn đã được tạo. Đang đăng nhập..."),
                        "already_registered": True
                    }
            
            # Nếu không phải người dùng tạo gần đây, thông báo email đã tồn tại
            return {"success": False, "error": _("Email này đã được sử dụng bởi tài khoản khác")}
                
        # Kiểm tra tên hiển thị
        if not display_name or len(display_name.strip()) < 3:
            return {"success": False, "error": _("Tên hiển thị phải có ít nhất 3 ký tự")}
            
        # Kiểm tra độ mạnh mật khẩu
        if len(password) < 6:
            return {"success": False, "error": _("Mật khẩu phải có ít nhất 6 ký tự")}
            
        # Tạo người dùng mới với cơ chế phòng chống race condition
        auto_commit_was_on = frappe.db.auto_commit_on_many_writes
        frappe.db.auto_commit_on_many_writes = True
        
        try:
            # Tạo người dùng mới
            user = frappe.new_doc("User")
            user.email = email
            user.first_name = display_name
            user.send_welcome_email = 0
            user.new_password = password
            user.user_type = "Website User"
            user.flags.no_welcome_mail = True
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
            
            # Đảm bảo mọi thay đổi đã được lưu
            frappe.db.commit()
            
            # Trì hoãn một chút để đảm bảo dữ liệu đã được lưu hoàn toàn
            time.sleep(1)
            
            return {
                "success": True,
                "message": _("Đăng ký thành công"),
                "user": user.name,
                "email": email,
                "pwd": password  # Trả về mật khẩu để frontend tự động đăng nhập
            }
            
        except frappe.DuplicateEntryError:
            # Xử lý trường hợp email đã tồn tại (do race condition)
            frappe.db.rollback()
            return {
                "success": True,
                "message": _("Tài khoản đã tồn tại"),
                "already_registered": True,
                "email": email
            }
            
        except Exception as e:
            frappe.db.rollback()
            frappe.log_error(f"Lỗi khi đăng ký: {str(e)}", "Registration Error")
            return {"success": False, "error": str(e)}
            
        finally:
            frappe.db.auto_commit_on_many_writes = auto_commit_was_on
            
    except Exception as e:
        frappe.log_error(f"Lỗi ngoài cùng khi đăng ký: {str(e)}", "Registration Outer Error")
        return {"success": False, "error": _("Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.")}

def create_player_profile(user, display_name=None):
    """Tạo hồ sơ người chơi mới"""
    try:
        if not display_name:
            try:
                user_doc = frappe.get_doc("User", user)
                display_name = user_doc.first_name
            except:
                display_name = "Player"
        
        # Kiểm tra xem hồ sơ người chơi đã tồn tại chưa
        existing_player = frappe.db.exists("Player", {"user": user})
        if existing_player:
            return frappe.get_doc("Player", existing_player)
        
        # Tạo mới hồ sơ người chơi
        player = frappe.new_doc("Player")
        player.user = user
        player.display_name = display_name
        player.rating = 1500
        player.coins = 1000
        player.country = "🇻🇳"
        player.flags.ignore_permissions = True
        player.insert()
        frappe.db.commit()
        return player
        
    except Exception as e:
        frappe.log_error(f"Lỗi khi tạo hồ sơ người chơi: {str(e)}", "Player Profile Error")
        frappe.db.rollback()
        # Không làm gián đoạn luồng đăng ký nếu không tạo được hồ sơ người chơi
        return None