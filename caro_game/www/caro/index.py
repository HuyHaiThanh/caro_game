import frappe

def get_context(context):
    context.no_cache = 1
    
    # Player info section - will be empty for guests
    if frappe.session.user != 'Guest':
        context.user_info = frappe.get_doc('User', frappe.session.user)
        context.player = frappe.get_all('Player', 
            filters={'user': frappe.session.user}, 
            fields=['name', 'display_name', 'coins', 'avatar'])
        if context.player:
            context.player = context.player[0]
    
    # Lấy danh sách người chơi xếp hạng cao nhất
    context.top_players = frappe.get_all('Player', 
        fields=['display_name', 'country', 'rating', 'avatar'],
        order_by='rating desc',
        limit=8)
    
    # Lấy danh sách vật phẩm cửa hàng
    context.shop_powerups = frappe.get_all('ShopItem', 
        filters={'item_type': 'Powerup'},
        fields=['name', 'item_name', 'description', 'price', 'duration', 'image'],
        limit=3)
    
    context.shop_icons = frappe.get_all('ShopItem', 
        filters={'item_type': 'Icon'},
        fields=['name', 'item_name', 'price', 'image'],
        limit=3)
    
    context.shop_avatars = frappe.get_all('ShopItem', 
        filters={'item_type': 'Avatar'},
        fields=['name', 'item_name', 'price', 'image'],
        limit=3)
    
    return context