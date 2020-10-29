


$(document).on('click', '#confirm-add-review', function (e) {

    var btn = $(this),
        content = $('#descriptionTextarea').val(),
        name = $('#inputName').val(),
        email = $('#emailAddress').val();
        
    if (!(name && email)) return;
    
    btn.disable();
    
    $.ajax({
        
        url: '/ajax/add-review/',
        type: 'POST',
        
        data: {
            productId: PRODUCT_ID,
            rating: app.reviewRating,
            content,
            name,
            email
        },
        
        success (data) {
            
            btn.enable();
            notify('success', 'Thank you for your review. Your feedback was submitted successfully');
            $('#Jpills-four-example1').resetModal();
            
            $.extend(app.product, data.product);
        },
        
        error (error) {
            btn.enable();
            generateAlerts(error);
        }
    });
    
    e.preventDefault();
});
