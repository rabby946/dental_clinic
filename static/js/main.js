document.addEventListener("DOMContentLoaded", function(){
            setTimeout(function() {
                let alerts = document.querySelectorAll('.alert-dismissible');
                alerts.forEach(function(alert) {
                    let bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                });
            }, 5000);
        });