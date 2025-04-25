import frappe
from frappe import _
from frappe.utils.password import check_password, update_password

@frappe.whitelist()
def update_player_profile(display_name=None, country=None, bio=None):
    """Update player profile information"""
    if frappe.session.user == 'Guest':
        return {'success': False, 'error': 'Vui lòng đăng nhập để cập nhật hồ sơ'}
    
    try:
        # Get player record for the current user
        player = frappe.get_all('Player', filters={'user': frappe.session.user}, fields=['name'], limit=1)
        
        if not player:
            return {'success': False, 'error': 'Không tìm thấy hồ sơ người chơi'}
        
        # Update player doc
        player_doc = frappe.get_doc('Player', player[0].name)
        
        if display_name:
            player_doc.display_name = display_name
        
        if country:
            player_doc.country = country
            
        if bio:
            player_doc.bio = bio
            
        player_doc.save()
        frappe.db.commit()
        
        return {'success': True}
    except Exception as e:
        frappe.log_error(f"Failed to update player profile: {str(e)}")
        return {'success': False, 'error': str(e)}


@frappe.whitelist()
def change_password(current_password, new_password):
    """Change user password"""
    if frappe.session.user == 'Guest':
        return {'success': False, 'error': 'Vui lòng đăng nhập để đổi mật khẩu'}
    
    try:
        # Check if current password is correct
        if not check_password(frappe.session.user, current_password):
            return {'success': False, 'error': 'Mật khẩu hiện tại không chính xác'}
        
        # Update password
        update_password(frappe.session.user, new_password)
        
        return {'success': True}
    except Exception as e:
        frappe.log_error(f"Failed to change password: {str(e)}")
        return {'success': False, 'error': str(e)}


@frappe.whitelist()
def set_player_avatar(item_id):
    """Set player avatar from owned item"""
    if frappe.session.user == 'Guest':
        return {'success': False, 'error': 'Vui lòng đăng nhập để cập nhật avatar'}
    
    try:
        # Get player record for current user
        player = frappe.get_all('Player', filters={'user': frappe.session.user}, fields=['name'], limit=1)
        
        if not player:
            return {'success': False, 'error': 'Không tìm thấy hồ sơ người chơi'}
            
        # Check if player owns the item
        owned_item = frappe.get_all('PlayerItem', 
            filters={
                'player': player[0].name,
                'item': item_id,
                'item_type': 'Avatar',
                'is_active': 1
            }, 
            limit=1)
            
        if not owned_item:
            return {'success': False, 'error': 'Bạn không sở hữu vật phẩm này'}
            
        # Get avatar image from shop item
        shop_item = frappe.get_doc('ShopItem', item_id)
        
        if not shop_item or not shop_item.image:
            return {'success': False, 'error': 'Không tìm thấy hình ảnh avatar'}
            
        # Update player avatar
        player_doc = frappe.get_doc('Player', player[0].name)
        player_doc.avatar = shop_item.image
        player_doc.save()
        
        return {'success': True}
    except Exception as e:
        frappe.log_error(f"Failed to set avatar: {str(e)}")
        return {'success': False, 'error': str(e)}


@frappe.whitelist()
def set_player_icon(item_id):
    """Set player icon from owned item"""
    if frappe.session.user == 'Guest':
        return {'success': False, 'error': 'Vui lòng đăng nhập để cập nhật icon'}
    
    try:
        # Get player record for current user
        player = frappe.get_all('Player', filters={'user': frappe.session.user}, fields=['name'], limit=1)
        
        if not player:
            return {'success': False, 'error': 'Không tìm thấy hồ sơ người chơi'}
            
        # Check if player owns the item
        owned_item = frappe.get_all('PlayerItem', 
            filters={
                'player': player[0].name,
                'item': item_id,
                'item_type': 'Icon',
                'is_active': 1
            }, 
            limit=1)
            
        if not owned_item:
            return {'success': False, 'error': 'Bạn không sở hữu vật phẩm này'}
            
        # Get icon image from shop item
        shop_item = frappe.get_doc('ShopItem', item_id)
        
        if not shop_item or not shop_item.image:
            return {'success': False, 'error': 'Không tìm thấy hình ảnh icon'}
            
        # Update player icon
        player_doc = frappe.get_doc('Player', player[0].name)
        player_doc.game_icon = shop_item.image
        player_doc.save()
        
        return {'success': True}
    except Exception as e:
        frappe.log_error(f"Failed to set icon: {str(e)}")
        return {'success': False, 'error': str(e)}