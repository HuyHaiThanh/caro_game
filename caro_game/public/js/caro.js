// Caro Game JS
$(document).ready(function() {
    // Timer countdown functionality
    startCountdown();
    
    // Xử lý nút đăng nhập trong header
    $('.login-btn').on('click', function(e) {
        e.preventDefault();
        showLoginModal();
    });
    
    // Login form submission
    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        
        const email = $('#login-email').val();
        const password = $('#login-password').val();
        
        // Hiển thị loading indicator
        frappe.ui.form.states.set_state($(this), 'loading');
        
        frappe.call({
            method: 'caro_game.api.auth.login',
            args: {
                usr: email,
                pwd: password
            },
            callback: function(response) {
                frappe.ui.form.states.clear_state($('#login-form'));
                if (response.message && response.message.success) {
                    // Hiển thị thông báo thành công
                    frappe.show_alert({
                        message: 'Đăng nhập thành công!',
                        indicator: 'green'
                    });
                    // Reload page on successful login
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Show error message
                    const errorMsg = (response.message && response.message.error) || 'Đã xảy ra lỗi khi đăng nhập';
                    frappe.throw(errorMsg);
                }
            }
        });
    });
    
    // Registration form submission
    $('#register-form').on('submit', function(e) {
        e.preventDefault();
        
        const displayName = $('#display-name').val();
        const email = $('#register-email').val();
        const password = $('#register-password').val();
        
        if (!$('#terms').is(':checked')) {
            frappe.throw('Bạn phải đồng ý với điều khoản dịch vụ');
            return;
        }
        
        // Hiển thị loading indicator
        frappe.ui.form.states.set_state($(this), 'loading');
        
        frappe.call({
            method: 'caro_game.api.auth.register',
            args: {
                email: email,
                password: password,
                display_name: displayName
            },
            callback: function(response) {
                frappe.ui.form.states.clear_state($('#register-form'));
                if (response.message && response.message.success) {
                    // Show success message and redirect to login
                    frappe.show_alert({
                        message: 'Đăng ký thành công! Vui lòng đăng nhập.',
                        indicator: 'green'
                    });
                    setTimeout(function() {
                        showLoginModal();
                    }, 2000);
                } else {
                    // Show error message
                    const errorMsg = (response.message && response.message.error) || 'Đã xảy ra lỗi khi đăng ký';
                    frappe.throw(errorMsg);
                }
            }
        });
    });
    
    // Xử lý các nút mạng xã hội
    $('.social-btn').on('click', function() {
        frappe.show_alert({
            message: 'Tính năng đăng nhập bằng mạng xã hội đang được phát triển.',
            indicator: 'yellow'
        });
    });
});

// Show login modal
function showLoginModal() {
    $('#registerModal').modal('hide');
    $('#loginModal').modal('show');
}

// Show register modal
function showRegisterModal() {
    $('#loginModal').modal('hide');
    $('#registerModal').modal('show');
}

// Start countdown timer
function startCountdown() {
    // Set the countdown end time to midnight
    const now = new Date();
    const endTime = new Date();
    endTime.setHours(23, 59, 59, 999);
    
    const timeRemaining = endTime - now;
    
    updateTimer(timeRemaining);
    
    // Update timer every second
    setInterval(function() {
        const currentTime = new Date();
        const remaining = endTime - currentTime;
        
        if (remaining <= 0) {
            // Reset timer at midnight
            const newEndTime = new Date();
            newEndTime.setDate(newEndTime.getDate() + 1);
            newEndTime.setHours(23, 59, 59, 999);
            updateTimer(newEndTime - currentTime);
        } else {
            updateTimer(remaining);
        }
    }, 1000);
}

// Update timer display
function updateTimer(timeRemaining) {
    const hours = Math.floor(timeRemaining / (1000 * 60 * 60));
    const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
    
    $('#hours').text(padZero(hours));
    $('#minutes').text(padZero(minutes));
    $('#seconds').text(padZero(seconds));
}

// Add leading zero to numbers less than 10
function padZero(num) {
    return num < 10 ? '0' + num : num;
}