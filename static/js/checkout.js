

function placeOrder() {
    
    $.ajax({
        
        url: '/ajax/place-order/',
        type: 'POST',
        
        data: {
            
        },
        
        success(data) {
            
        },
        
        error: generateAlerts
    });
}
