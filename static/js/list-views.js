
var vueData = {
    
    products: PRODUCTS,
    
    productSearch: '',
    
    filters: {
        brands: [],
        colors: [],
        frameTypes: []
    },
    
    ordering: 'default'
};

var vueMethods = {
    
};

var vueComputed = {
    
    searchedAndFilteredProducts () {
        
        var filters = this.filters;
        
        var products = this.products.filter(product => {
            return (
                (!filters.brands.length || filters.brands.includes(product.brand)) &&
                (!filters.colors.length || filters.colors.includes(product.color)) &&
                (!filters.frameTypes.length || filters.frameTypes.includes(product.frame_type))
            );
        });
        
        var search = this.productSearch.toLowerCase();
        
        products = products.filter(product => {
            return !search || (
                product.name.toLowerCase().includes(search) ||
                product.type.toLowerCase().includes(search) ||
                product.brand.toLowerCase().includes(search)
            )
        });
        
        if (this.ordering === 'latest') {
            products = products.sort((a, b) => b.created_timestamp - a.created_timestamp);
        }
        
        else if (this.ordering === 'price ascending') {
            products = products.sort((a, b) => a.price - b.price);
        }
        
        else if (this.ordering === 'price descending') {
            products = products.sort((a, b) => b.price - a.price);
        }
        
        return products;
        
    },
    
    brands () {
        return this.getFilterData('brand');
    },
    
    colors () {
        return this.getFilterData('color');
    },
    
    frameTypes () {
        return this.getFilterData('frame_type');
    },
    
};
