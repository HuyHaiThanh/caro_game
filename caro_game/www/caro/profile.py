import frappe

def get_context(context):
    context.no_cache = 1
    
    # Initialize default values first to ensure they always exist
    context.title = "Hồ sơ người chơi"
    context.player = {
        'display_name': frappe.session.user.split('@')[0],
        'rating': 1000,
        'coins': 0,
        'avatar': None,
        'country': None,
        'bio': None,
        'date_joined': frappe.utils.today()
    }
    context.stats = {
        'total_games': 0,
        'wins': 0,
        'losses': 0,
        'draws': 0,
        'win_streak': 0,
        'highest_rating': 1000,
        'win_percentage': 0
    }
    context.match_history = []
    context.achievements = []
    context.owned_items = []
    
    try:
        # Redirect to login if user is guest
        if frappe.session.user == 'Guest':
            frappe.local.flags.redirect_location = '/login'
            raise frappe.Redirect
        
        # Get user information
        context.user_info = frappe.get_doc('User', frappe.session.user)
        context.player['display_name'] = context.user_info.full_name or context.player['display_name']
        
        # Check if Player doctype exists and get player data
        if frappe.db.exists('DocType', 'Player'):
            player = frappe.db.get_value('Player', 
                {'user': frappe.session.user}, 
                ['name', 'display_name', 'coins', 'avatar', 'rating', 'country', 'bio', 'date_joined'],
                as_dict=1)
            
            if player:
                # Update player data in context
                context.player.update(player)
                # Set the title with player name
                context.title = f"Hồ sơ người chơi - {context.player['display_name']}"
                
                # Get player statistics if PlayerStats doctype exists
                if frappe.db.exists('DocType', 'PlayerStats'):
                    stats = frappe.db.get_value('PlayerStats', 
                        {'player': player.name}, 
                        ['total_games', 'wins', 'losses', 'draws', 'win_streak', 'highest_rating'],
                        as_dict=1)
                    
                    if stats:
                        context.stats.update(stats)
                        # Calculate win percentage
                        if stats.total_games > 0:
                            context.stats['win_percentage'] = round((stats.wins / stats.total_games) * 100, 1)
                
                # Get match history if GameMatch doctype exists
                if frappe.db.exists('DocType', 'GameMatch'):
                    try:
                        # Get matches where user is player1
                        matches1 = frappe.get_all('GameMatch', 
                            filters=[['player1', '=', player.name], ['status', '=', 'Completed']], 
                            fields=['name', 'player1', 'player2', 'winner', 'player1_score', 'player2_score', 'game_date'],
                            order_by='game_date desc',
                            limit=10)
                            
                        # Get matches where user is player2
                        matches2 = frappe.get_all('GameMatch', 
                            filters=[['player2', '=', player.name], ['status', '=', 'Completed']], 
                            fields=['name', 'player1', 'player2', 'winner', 'player1_score', 'player2_score', 'game_date'],
                            order_by='game_date desc',
                            limit=10)
                            
                        # Combine and sort match history
                        context.match_history = matches1 + matches2
                        if context.match_history:
                            context.match_history.sort(key=lambda x: x.get('game_date', ''), reverse=True)
                            context.match_history = context.match_history[:10]  # Take only 10 latest matches
                    except Exception as e:
                        frappe.log_error(f"Error fetching match history: {str(e)}")
                        
                # Get achievements if PlayerAchievement doctype exists
                if frappe.db.exists('DocType', 'PlayerAchievement'):
                    try:
                        context.achievements = frappe.get_all('PlayerAchievement', 
                            filters={'player': player.name}, 
                            fields=['achievement', 'date_earned'],
                            order_by='date_earned desc')
                    except Exception as e:
                        frappe.log_error(f"Error fetching achievements: {str(e)}")
                        
                # Get owned items if PlayerItem doctype exists
                if frappe.db.exists('DocType', 'PlayerItem'):
                    try:
                        context.owned_items = frappe.get_all('PlayerItem', 
                            filters={'player': player.name, 'is_active': 1}, 
                            fields=['item', 'item_type', 'purchase_date'],
                            order_by='purchase_date desc')
                    except Exception as e:
                        frappe.log_error(f"Error fetching owned items: {str(e)}")
            else:
                # Create a player if it doesn't exist
                try:
                    new_player = frappe.get_doc({
                        'doctype': 'Player',
                        'user': frappe.session.user,
                        'display_name': context.user_info.full_name or frappe.session.user.split('@')[0],
                        'rating': 1000,
                        'coins': 100,
                        'date_joined': frappe.utils.today()
                    })
                    new_player.insert(ignore_permissions=True)
                    frappe.db.commit()
                    
                    # Reload the page to get the new player info
                    frappe.local.flags.redirect_location = '/caro/profile'
                    raise frappe.Redirect
                    
                except Exception as e:
                    frappe.log_error(f"Error creating player: {str(e)}")
                    context.player = {
                        'display_name': context.user_info.full_name or frappe.session.user.split('@')[0],
                        'rating': 1000,
                        'coins': 0,
                        'avatar': None,
                        'country': None,
                        'bio': None,
                        'date_joined': frappe.utils.today()
                    }
    except Exception as e:
        frappe.log_error(f"Error in profile page: {str(e)}", "Profile Page Error")
        # User info fallback
        if not hasattr(context, 'user_info'):
            context.user_info = {'email': frappe.session.user, 'full_name': frappe.session.user}
    
    return context