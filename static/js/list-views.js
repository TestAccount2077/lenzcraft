

var pageInfo = JSON.parse(localStorage[LIST_FILTER_CATEGORY] || '{}'),
    filters = pageInfo.filters || {
        brands: [],
        colors: [],
        frameTypes: []
    };


var vueData = {
        
    productSearch: '',
    pageNum: 1,
    filters: $.extend({}, filters),
    
    ordering: 'default'
};

var vueMethods = {
    
    updatePageNum(action) {
        
        var pageNum = this.pageNum;
        
        if (action === 'increment' && pageNum + 1 <= this.pageCount) {
            this.pageNum++;
        }
        
        if (action === 'decrement' && pageNum - 1 > 0) {
            this.pageNum--;
        }
    }
};

var vueComputed = {
    
    pageFilteredProducts() {
        
        var products = this.nonCartProducts;
        
        if (LIST_FILTER_CATEGORY === 'Sunglasses') {
            return products.filter(product => product.type === LIST_FILTER_CATEGORY);
        }
        return products.filter(product => product.category === LIST_FILTER_CATEGORY);
    },
    
    searchedAndFilteredProducts () {
        
        var filters = this.filters;
        
        var start = this.startIndex,
            end = start + 25;
        
        var products = this.pageFilteredProducts;
        
        var products = products.filter(product => {
            
            var colorMatches = Boolean(product.colors.filter(color => filters.colors.includes(color)).length);

            return (
                (!filters.brands.length || filters.brands.includes(product.brand)) &&
                (!filters.colors.length || colorMatches) &&
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
    
    displayedProducts() {
        return this.searchedAndFilteredProducts.slice(this.startIndex, this.endIndex);
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
    
    startIndex() {
        return (this.pageNum - 1) * 25;
    },
    
    readableStartIndex() {
        return this.searchedAndFilteredProducts.length ? this.startIndex + 1 : 0;
    },
    
    endIndex() {
        
        var endIndex = this.startIndex + 25;
        
        if (endIndex > this.searchedAndFilteredProducts.length) return this.searchedAndFilteredProducts.length;
        return endIndex;
    },
    
    pageCount() {
        return Math.ceil(this.searchedAndFilteredProducts.length / 25);
    }
    
};

function updateFilters() {
    setTimeout(() => {
        var pageInfo = JSON.parse(localStorage[LIST_FILTER_CATEGORY] || '{}');
        pageInfo.filters = app.filters;
        // localStorage.setItem(LIST_FILTER_CATEGORY, JSON.stringify(pageInfo));
    }, 100);
}

var vueWatch = {
    'filters.brands': updateFilters,
    'filters.colors': updateFilters,
    'filters.frameTypes': updateFilters,
}
