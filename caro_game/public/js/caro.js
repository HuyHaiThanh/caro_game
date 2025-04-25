// Caro Game JS
$(document).ready(function() {
    // Timer countdown functionality
    startCountdown();
    
    // Kiểm tra nếu người dùng đã đăng nhập thành công từ phiên đăng ký
    if (localStorage.getItem('registration_success')) {
        showSuccessToast('Đăng ký thành công! Bạn đã được đăng nhập vào hệ thống.');
        localStorage.removeItem('registration_success');
    }
    
    // Login form submission
    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        
        const email = $('#login-email').val();
        const password = $('#login-password').val();
        
        // Hiển thị thông báo đang xử lý
        showProcessingToast('Đang đăng nhập...');
        
        frappe.call({
            method: 'caro_game.api.auth.login',
            args: {
                usr: email,
                pwd: password
            },
            callback: function(response) {
                if (response.message && response.message.success) {
                    // Hiển thị thông báo thành công
                    showSuccessToast('Đăng nhập thành công!');
                    
                    // Reload page on successful login sau 1 giây
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Show error message
                    const errorMsg = (response.message && response.message.error) || 'Đã xảy ra lỗi khi đăng nhập';
                    showErrorToast(errorMsg);
                }
            },
            error: function() {
                showErrorToast('Không thể kết nối đến máy chủ. Vui lòng thử lại sau.');
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
            showErrorToast('Bạn phải đồng ý với điều khoản dịch vụ');
            return;
        }
        
        // Hiển thị thông báo đang xử lý
        showProcessingToast('Đang tiến hành đăng ký...');
        
        // Vô hiệu hóa nút đăng ký để tránh nhấn nhiều lần
        $('#register-form button[type="submit"]').prop('disabled', true);
        
        frappe.call({
            method: 'caro_game.api.auth.register',
            args: {
                email: email,
                password: password,
                display_name: displayName
            },
            callback: function(response) {
                if (response.message && response.message.success) {
                    // Ẩn modal đăng ký
                    $('#registerModal').modal('hide');
                    
                    // Xử lý trường hợp đã đăng ký trước đó
                    if (response.message.already_registered) {
                        showSuccessToast('Tài khoản đã tồn tại, đang đăng nhập...');
                    } else {
                        // Show success message
                        showSuccessToast('Đăng ký thành công! Đang đăng nhập...');
                    }
                    
                    // Lưu trạng thái đăng ký thành công
                    localStorage.setItem('registration_success', 'true');
                    
                    // Đợi một khoảng thời gian trước khi đăng nhập
                    setTimeout(function() {
                        // Đăng nhập tự động sau khi đăng ký
                        frappe.call({
                            method: 'caro_game.api.auth.login',
                            args: {
                                usr: email,
                                pwd: password
                            },
                            callback: function(loginResponse) {
                                if (loginResponse.message && loginResponse.message.success) {
                                    // Reload page after successful login/registration
                                    window.location.reload();
                                } else {
                                    // Nếu đăng nhập thất bại, hiển thị thông báo và chuyển sang form đăng nhập
                                    showErrorToast('Đăng nhập tự động thất bại, vui lòng đăng nhập thủ công.');
                                    setTimeout(function() {
                                        showLoginModal();
                                        // Điền sẵn email vào form đăng nhập
                                        $('#login-email').val(email);
                                    }, 1500);
                                }
                            }
                        });
                    }, 2000);
                } else {
                    // Show error message
                    const errorMsg = (response.message && response.message.error) || 'Đã xảy ra lỗi khi đăng ký';
                    showErrorToast(errorMsg);
                    
                    // Enable the submit button again
                    $('#register-form button[type="submit"]').prop('disabled', false);
                }
            },
            error: function() {
                showErrorToast('Không thể kết nối đến máy chủ. Vui lòng thử lại sau.');
                $('#register-form button[type="submit"]').prop('disabled', false);
            }
        });
    });
});

// Show login modal
function showLoginModal() {
    $('#registerModal').modal('hide');
    $('#loginModal').modal('show');
    
    // Reset form
    $('#login-form')[0].reset();
}

// Show register modal
function showRegisterModal() {
    $('#loginModal').modal('hide');
    $('#registerModal').modal('show');
    
    // Reset form
    $('#register-form')[0].reset();
}

// Show toast messages
function showSuccessToast(message) {
    frappe.show_alert({
        message: message,
        indicator: 'green'
    }, 5);
}

function showErrorToast(message) {
    frappe.show_alert({
        message: message,
        indicator: 'red'
    }, 5);
}

function showProcessingToast(message) {
    frappe.show_alert({
        message: message,
        indicator: 'blue'
    }, 3);
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