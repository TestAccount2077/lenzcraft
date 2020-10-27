Vue.component('home-product', {
    
    props: ['product'],
    
    template: `<li class="col-md-6 product-item product-item__card mb-2 remove-divider pr-md-2 border-bottom-0">
        <div class="product-item__outer h-100 w-100">
            <div class="product-item__inner p-md-3 row no-gutters bg-white max-width-334">
                <div class="col col-lg-auto product-media-left">
                    <a href="shop/single-product-fullwidth.html" class="max-width-120 d-block"><img class="img-fluid" :src="product.image_url" alt="Image Description"></a>
                </div>
                <div class="col product-item__body pl-2 pl-lg-3 mr-xl-2 mr-wd-1 pr-3 pr-md-0 pt-1 pt-md-0">
                    <div class="mb-2">
                        <div class="mb-2"><a href="shop/product-categories-7-column-full-width.html" class="font-size-12 text-gray-5" v-text='product.type'></a></div>
                        <h5 class="product-item__title"><a href="shop/single-product-fullwidth.html" class="text-blue font-weight-bold" v-text='product.name'></a></h5>
                    </div>
                    <div class="flex-center-between mb-2">
                        <div class="prodcut-price">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <add-to-cart-btn :product='product'></add-to-cart-btn>
                    </div>
                    <div class="product-item__footer bg-white">
                        <div class="border-top pt-2 flex-center-between flex-wrap">
                            <add-to-wishlist-btn :product='product'></add-to-wishlist-btn>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>`
});

Vue.component('list-view-product-1', {
    
    props: ['product'],
    
    template: `<li class="col-6 col-md-3 col-wd-2gdot4 product-item">
        <div class="product-item__outer h-100">
            <div class="product-item__inner px-xl-4 p-3">
                <div class="product-item__body pb-xl-2">
                    <h5 class="mb-1 product-item__title"><a :href='product.url' class="text-blue font-weight-bold" v-text='product.name'></a></h5>
                    <div class="mb-2">
                        <a :href='product.url' class="d-block text-center"><img class="img-fluid" :src="product.image_url" alt="Image Description"></a>
                    </div>
                    <div class="flex-center-between mb-1">
                        <div class="prodcut-price">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <add-to-cart-btn :product='product'></add-to-cart-btn>
                    </div>
                    <div class="pt-2 flex-center-between flex-wrap">
                        <add-to-wishlist-btn :product='product'></add-to-wishlist-btn>
                    </div>
                </div>
                <div class="product-item__footer">
                    <div class="border-top pt-2 flex-center-between flex-wrap">
                        <div class="prodcut-price">
                            <div class="font-size-12 text-gray-5"><i class="fa fa-hashtag mr-2"></i><span v-text='product.model_number'></span></div>
                        </div>
                        <div class="d-none d-xl-block font-size-12 text-gray-5">
                            <div>Model Number</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>`
});

Vue.component('list-view-product-2', {
    
    props: ['product'],
    
    template: `<li class="col-6 col-md-3 col-wd-2gdot4 product-item">
        <div class="product-item__outer h-100">
            <div class="product-item__inner px-xl-4 p-3">
                <div class="product-item__body pb-xl-2">
                    <h5 class="mb-1 product-item__title"><a :href="product.url" class="text-blue font-weight-bold" v-text='product.name'></a></h5>
                    <div class="mb-2">
                        <a :href="product.url" class="d-block text-center"><img class="img-fluid" :src="product.image_url" alt="Image Description"></a>
                    </div>
                    <div class="mb-3">
                        <a class="d-inline-flex align-items-center small font-size-14" href="#">
                            <div class="text-warning mr-2">
                                <small class="fas fa-star" v-for='star in product.total_rating'></small>
                                <small class="far fa-star text-muted" v-for='star in 5 - product.total_rating'></small>
                            </div>
                            <span class="text-secondary" v-text='"(" + product.reviews.length + ")"'></span>
                        </a>
                    </div>
                    <ul class="font-size-12 p-0 text-gray-110 mb-4">
                        <li class="line-clamp-1 mb-1 list-bullet">Lorem ipsum dolor sit amet</li>
                        <li class="line-clamp-1 mb-1 list-bullet">consectetur adipisicing elit, sed do eiusmod tempor incididunt.</li>
                        <li class="line-clamp-1 mb-1 list-bullet">consectetur adipisicing elit, sed do eiusmod tempor incididunt</li>
                    </ul>
                    <div class="text-gray-20 mb-2 font-size-12">SKU: FW511948218</div>
                    <div class="flex-center-between mb-1">
                        <div class="prodcut-price">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <add-to-cart-btn :product='product'></add-to-cart-btn>
                    </div>
                    <div class="pt-2 flex-center-between flex-wrap">
                        <add-to-wishlist-btn :product='product'></add-to-wishlist-btn>
                    </div>
                </div>
                <div class="product-item__footer">
                    <div class="border-top pt-2 flex-center-between flex-wrap">
                        <div class="prodcut-price">
                            <div class="font-size-12 text-gray-5"><i class="fa fa-hashtag mr-2"></i><span v-text='product.model_number'></span></div>
                        </div>
                        <div class="d-none d-xl-block font-size-12 text-gray-5">
                            <div>Model Number</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>`
});

Vue.component('list-view-product-3', {
    
    props: ['product'],
    
    template: `<li class="product-item remove-divider">
        <div class="product-item__outer w-100">
            <div class="product-item__inner remove-prodcut-hover py-4 row">
                <div class="product-item__header col-6 col-md-4">
                    <div class="mb-2">
                        <a :href='product.url' class="d-block text-center"><img class="img-fluid" :src="product.image_url" alt="Image Description"></a>
                    </div>
                </div>
                <div class="product-item__body col-6 col-md-5">
                    <div class="pr-lg-10">
                        <div class="mb-2"><a :href='product.url' class="font-size-12 text-gray-5" v-text='product.type'></a></div>
                        <h5 class="mb-2 product-item__title"><a :href='product.url' class="text-blue font-weight-bold" v-text='product.name'></a></h5>
                        <div class="prodcut-price mb-2 d-md-none">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <div class="mb-3 d-none d-md-block">
                            <a class="d-inline-flex align-items-center small font-size-14" href="#">
                                <div class="text-warning mr-2">
                                    <small class="fas fa-star" v-for='star in product.total_rating'></small>
                                    <small class="far fa-star text-muted" v-for='star in 5 - product.total_rating'></small>
                                </div>
                                <span class="text-secondary" v-text='"(" + product.reviews.length + ")"'></span>
                            </a>
                        </div>
                        <ul class="font-size-12 p-0 text-gray-110 mb-4 d-none d-md-block">
                            <li class="line-clamp-1 mb-1 list-bullet">Lorem ipsum dolor sit amet</li>
                            <li class="line-clamp-1 mb-1 list-bullet">consectetur adipisicing elit, sed do eiusmod tempor incididunt.</li>
                            <li class="line-clamp-1 mb-1 list-bullet">consectetur adipisicing elit, sed do eiusmod tempor incididunt</li>
                        </ul>
                    </div>
                </div>
                <div class="product-item__footer col-md-3 d-md-block">
                    <div class="mb-3">
                        <div class="prodcut-price mb-2">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <div class="prodcut-add-cart" @click='$root.toggleProductInCart(product, "toggle")'>
                            <a href='#' class="btn btn-sm btn-block btn-primary-dark btn-wide transition-3d-hover" v-text='product.in_cart ? "Remove from cart" : "Add to cart"'></a>
                        </div>
                    </div>
                    <div class="flex-horizontal-center justify-content-between justify-content-wd-center flex-wrap">
                        <add-to-wishlist-btn :product='product'></add-to-wishlist-btn>
                    </div>
                </div>
            </div>
        </div>
    </li>`
});

Vue.component('list-view-product-4', {
    
    props: ['product'],
    
    template: `<li class="product-item remove-divider">
        <div class="product-item__outer w-100">
            <div class="product-item__inner remove-prodcut-hover py-4 row">
                <div class="product-item__header col-6 col-md-2">
                    <div class="mb-2">
                        <a :href='product.url' class="d-block text-center"><img class="img-fluid" :src="product.image_url" alt="Image Description"></a>
                    </div>
                </div>
                <div class="product-item__body col-6 col-md-7">
                    <div class="pr-lg-10">
                        <div class="mb-2"><a :href='product.url' class="font-size-12 text-gray-5" v-text='product.type'></a></div>
                        <h5 class="mb-2 product-item__title"><a :href='product.url' class="text-blue font-weight-bold" v-text='product.name'></a></h5>
                        <div class="prodcut-price d-md-none">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <ul class="font-size-12 p-0 text-gray-110 mb-4 d-none d-md-block">
                            <li class="line-clamp-1 mb-1 list-bullet">Lorem ipsum dolor sit amet</li>
                            <li class="line-clamp-1 mb-1 list-bullet">consectetur adipisicing elit, sed do eiusmod tempor incididunt.</li>
                            <li class="line-clamp-1 mb-1 list-bullet">consectetur adipisicing elit, sed do eiusmod tempor incididunt</li>
                        </ul>
                        <div class="mb-3 d-none d-md-block">
                            <a class="d-inline-flex align-items-center small font-size-14" href="#">
                                <div class="text-warning mr-2">
                                    <small class="fas fa-star" v-for='star in product.total_rating'></small>
                                    <small class="far fa-star text-muted" v-for='star in 5 - product.total_rating'></small>
                                </div>
                                <span class="text-secondary" v-text='"(" + product.reviews.length + ")"'></span>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="product-item__footer col-md-3 d-md-block">
                    <div class="mb-2 flex-center-between">
                        <div class="prodcut-price">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <div class="prodcut-add-cart">
                            <a :href='product.url' class="btn-add-cart btn-primary transition-3d-hover"><i class="ec ec-add-to-cart"></i></a>
                        </div>
                    </div>
                    <div class="flex-horizontal-center justify-content-between justify-content-wd-center flex-wrap border-top pt-3">
                        <add-to-wishlist-btn :product='product'></add-to-wishlist-btn>
                    </div>
                </div>
            </div>
        </div>
    </li>`
});

Vue.component('homepage-long-product', {
    
    props: ['product'],
    
    template: `<li class="col-6 col-md-4 col-xl product-item">
        <div class="product-item__outer h-100 w-100">
            <div class="product-item__inner px-xl-4 p-3">
                <div class="product-item__body pb-xl-2">
                    <div class="mb-2">
                        <a :href="product.url" class="font-size-12 text-gray-5" v-text='product.type'></a>
                    </div>
                    <h5 class="mb-1 product-item__title"><a :href="product.url" class="text-blue font-weight-bold" v-text='product.name'></a></h5>
                    <div class="mb-2">
                        <a :href="product.url" class="d-block text-center"><img class="img-fluid" :src="product.image_url" alt="Image Description"></a>
                    </div>
                    <div class="flex-center-between mb-1">
                        <div class="prodcut-price">
                            <div class="text-gray-100" v-text='product.formatted_price'></div>
                        </div>
                        <add-to-cart-btn :product='product'></add-to-cart-btn>
                    </div>
                </div>
                <div class="product-item__footer">
                    <div class="border-top pt-2 flex-center-between flex-wrap">
                        <add-to-wishlist-btn :product='product'></add-to-wishlist-btn>
                    </div>
                </div>
            </div>
        </div>
    </li>`
});

Vue.component('filter-item', {
    
    props: ['item', 'type', 'filters'],
    
    template: `<div class="form-group d-flex align-items-center justify-content-between mb-2 pb-1">
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" :id="type + '-' + item.index" :value="item.name" v-model='filters[type]'>
            <label class="custom-control-label" :for="type + '-' + item.index">
                <span v-text='item.name'></span>
                <span class="text-gray-25 font-size-12 font-weight-normal" v-text=' "(" + item.count + ")"'></span>
            </label>
        </div>
    </div>`
})

Vue.component('add-to-cart-btn', {
    
    props: ['product'],
    
    template: `<div class="d-none d-xl-block prodcut-add-cart" @click='$root.toggleProductInCart(product, "increment")'>
        <span class="btn-add-cart lenz-gradient transition-3d-hover pointer">
            <i class="ec ec-add-to-cart"></i>
        </span>
    </div>`
});

Vue.component('add-to-wishlist-btn', {
    
    props: ['product'],
    
    template: `
        <span class="text-gray-6 font-size-13 pointer" @click='$root.toggleProductInWishlist(product, "increment")'>
            <i class="ec ec-favorites mr-1 font-size-15" :class='{"text-red": product.in_wishlist}'></i>
            Wishlist
        </span>
    `
});

Vue.component('toggle-cart-qty-section', {
    
    props: ['product'],
    
    template: `<div class="js-quantity row align-items-center">
        <div class="col">
            <input class="js-result form-control h-auto border-0 rounded p-0 shadow-none" type="text" v-model='product.qty'>
        </div>
        <div class="col-auto pr-1">
            <a class="js-minus btn btn-icon btn-xs btn-outline-secondary rounded-circle border-0" href="javascript:;" @click='$root.toggleProductInCart(product, "decrement", null, null, true)'>
                <small class="fas fa-minus btn-icon__inner"></small>
            </a>
            <a class="js-plus btn btn-icon btn-xs btn-outline-secondary rounded-circle border-0" href="javascript:;" @click='$root.toggleProductInCart(product, "increment", null, null, true)'>
                <small class="fas fa-plus btn-icon__inner"></small>
            </a>
        </div>
    </div>`
});
