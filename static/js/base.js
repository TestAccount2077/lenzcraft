var app = new Vue ({
    
    el: "#app",
    delimiters: ['[[', ']]'],
    
    data: $.extend(window.vueData || {}, {
        productSearch: '',
        products: PRODUCTS
    }),
    
    methods: $.extend(window.vueMethods || {}, {
        
        getFilterData(productAttributeName) {
            
            var array = this.products.map(product => product[productAttributeName]);
                object = {};
            
            array.forEach((item, index) => {
                if (item && !Object.keys(object).includes(item)) {
                    
                    var products = this.products.filter(product => product[productAttributeName] === item);
                    
                    object[item] = {
                        index,
                        name: item,
                        count: products.length
                    };
                }
            });
            
            return Object.values(object);
        },
        
        toggleProductInWishlist(product) {
            
            $.ajax({
                
                url: '/ajax/toggle-product-in-wishlist/',
                type: 'POST',
                
                data: {
                    productId: product.id
                },
                
                success (data) {
                    notify('success', data.message);
                    product.in_wishlist = !product.in_wishlist;
                },
                
                error: generateAlerts
            });
        },
        
        toggleProductInCart(product, callback) {
            
            $.ajax({
                
                url: '/ajax/toggle-product-in-cart/',
                type: 'POST',
                
                data: {
                    productId: product.id
                },
                
                success (data) {
                    
                    notify('success', data.message);
                    
                    $.extend(product, data.product);
                    
                    if (callback) callback(product);
                },
                
                error: generateAlerts
            });
        },
        
        getProductById(id) {
            
            var product = this.products.filter(product => id === product.id)[0];
            
            if (product) return product;
            
            return null;
        },
        
        addProduct(product) {
            
            var p = this.getProductById(product.id);
            
            if (p) {
                this.products[this.products.indexOf(p)] = product;
            }
            
            else {
                this.products.push(product);
            }
        },
        
        removeProduct(product) {
            
            var p = this.getProductById(product.id);
            
            if (p) {
                this.products.splice(p, 1);
            }
        }
    }),
    
    computed: $.extend(window.vueComputed, {
        
        productsInCart() {
            return this.products.filter(product => product.in_cart);
        },
        
        totalCartCost() {
            
            if (this.productsInCart.length) {
                var totalCost = this.productsInCart.map(product => product.price * product.qty).reduce((p1, p2) => p1 + p2);
                // do some formatting here
                return totalCost.toFixed(2);
            }
            
            return 0.00;
        }
    })
});


$(document).on('click', '#confirm-login', function () {
    
    var email = $('#signinEmail').val(),
        password = $('#signinPassword').val();
        
    $.ajax({
        url: '/ajax/validate-login/',
        type: 'POST',
        
        data: {
            email,
            password
        },
        
        success (data) {
            location.reload();
        },
        
        error: generateAlerts
    })
    
});

function logout() {
    
    $.ajax({
        
        url: '/ajax/logout/',
        type: 'POST',
        
        success (data) {
            location.reload();
        },
        
        error: generateAlerts
    });
}

function generateAlerts(error, data, toastSettings, type='error') {
        
    var data,
        message = '',
        _4xxCodes = [400, 402, 403, 404];
    
    if (!error) {
        
        $.each(data, (e, errorMessage) => {
            message += '&bull; ' + errorMessage + '<br>';
        });
        
        notify(type, message, toastSettings);
        return;
    }
    
    if (_4xxCodes.includes(error.status)) {
        
        data = error.responseJSON;
        
        $.each(data, function (e, errorMessage) {
            message += '&bull; ' + errorMessage + '<br>';
        });
        
        notify(type, message,toastSettings);
        
    } else if (error.status === 500) {
        notify(type, 'Something went wrong. Please try again', toastSettings);
    }
}

function notify(type, message, settings) {
    
    settings = settings || {};
    
    var data = $.extend(
        {
            title: capitalize(type),
            message,
            position: 'topRight',
            zindex: 99999
        },
        settings
    );
    
    if (type === 'error') {
        iziToast.error(data);
    }
    
    else if (type === 'warning') {
        iziToast.warning(data);
    }
    
    else if (type === 'info') {
        iziToast.info(data);
    }
    
    else if (type === 'success') {
        iziToast.success(data);
    }
}

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function getCookie(name) {
    
    'use strict';
    
    var cookieValue = null,
        i,
        cookies,
        cookie;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = 0; i < cookies.length; i += 1) {
            cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    
    'use strict';
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        
        'use strict';
        
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
