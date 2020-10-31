var app = new Vue ({
    
    el: "#app",
    delimiters: ['[[', ']]'],
    
    data: $.extend(window.vueData || {}, {
        productSearch: '',
        products: PRODUCTS,
        user: USER
    }),
    
    methods: $.extend(window.vueMethods || {}, {
        
        getFilterData(productAttributeName) {
            
            var products = this.pageFilteredProducts,
                object = {};
            
            if (productAttributeName === 'color') {
                
                var allColors = [];
                
                products.forEach(product => allColors.push(...product.colors));
                console.log(allColors)
                allColors = new Array(...new Set(allColors));
                console.log(allColors)
                array = products.map(product => product.colors);
                
                allColors.forEach((color, index) => {
                    if (color && !Object.keys(object).includes(color)) {
                        
                        var _products = products.filter(product => product.colors.includes(color));
                        
                        object[color] = {
                            index,
                            name: color,
                            count: _products.length
                        };
                    }
                });
                
                return Object.values(object);
            }
            
            var array = products.map(product => product[productAttributeName]);
            
            array.forEach((item, index) => {
                if (item && !Object.keys(object).includes(item)) {
                    
                    var _products = products.filter(product => product[productAttributeName] === item);
                    
                    object[item] = {
                        index,
                        name: item,
                        count: _products.length
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
                    
                    var products = app.products.filter(_product => _product.id == product.id);
                    
                    if (products.length) {
                        products.forEach(product => product.in_wishlist = !product.in_wishlist);
                    }
                },
                
                error: generateAlerts
            });
        },
        
        toggleProductInCart(product, action, qty, callback, silent, colorName) {
            
            var that = this;
            
            $.ajax({
                
                url: '/ajax/toggle-product-in-cart/',
                type: 'POST',
                
                data: {
                    productId: product.id,
                    cartProductId: colorName ? undefined : product.cart_product_id,
                    action,
                    qty,
                    colorName
                },
                
                success (data) {
                    
                    if (!silent) notify('success', data.message);
                    
                    if (!product.is_cart_product) product = that.cartProducts.filter(product => product.id == data.product.id)[0]
                    
                    if (product) $.extend(product, data.product);
                    else (that.products.push(data.product));
                    
                    if (action === 'remove') {
                        var index = that.products.indexOf(product);
                        that.products.splice(index, 1);
                    }
                    
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
        
        cartProducts() {
            return this.products.filter(product => product.is_cart_product);
        },
        
        nonCartProducts() {
            return this.products.filter(product => !product.is_cart_product);
        },
        
        wishlistedProducts() {
            return this.nonCartProducts.filter(product => product.in_wishlist);
        },
        
        totalCartCost() {
            
            if (this.cartProducts.length) {
                var totalCost = this.cartProducts.map(product => product.billing_price * product.qty).reduce((p1, p2) => p1 + p2);
                // do some formatting here
                return totalCost;
            }
            
            return 0.00;
        },
        
        loggedIn() {
            return !$.isEmptyObject(this.user);
        }
    }),
    
    watch: $.extend(window.vueWatch, {}),
    
    filters: {
        currency(number, currency='USD') {
            return number.toLocaleString('en-US', {
              style: 'currency',
              currency,
            });
        }
    },
    
    created: window.vueCreated || function () {}
});

$(document).on('click', '#confirm-signup', function (e) {
    
    var name = $('#signupName').val(),
        email = $('#signupEmail').val(),
        phone = $('#signupPhone').val(),
        password = $('#signupPassword').val(),
        password_confirmation = $('#signupConfirmPassword').val();
        
    if (!(name && email && phone && password && password_confirmation)) return;
    
    $.ajax({
        
        url: '/ajax/validate-signup/',
        type: 'POST',
        
        data: {
            name,
            email,
            phone,
            password,
            password_confirmation
        },
        
        success (data) {
            notify('success', 'Signed up successfully. Please click the link sent to your email to activate your account');
            location.reload();
        },
        
        error: generateAlerts
    });
    
    e.preventDefault();
    
});

$(document).on('click', '#confirm-login', function (e) {
    
    var email = $('#signinEmail').val(),
        password = $('#signinPassword').val();
        
    if (!(email && password)) return;
    
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
    });
    
    e.preventDefault();
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
