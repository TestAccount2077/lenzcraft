
var vueData = {
    
    products: PRODUCTS,
    
    productSearch: '',
    pageNum: 1,
    
    filters: {
        brands: [],
        colors: [],
        frameTypes: []
    },
    
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
        return this.products.filter(product => product.category === LIST_FILTER_CATEGORY);
    },
    
    searchedAndFilteredProducts () {
        
        var filters = this.filters;
        
        var start = this.startIndex,
            end = start + 25;
        
        var products = this.pageFilteredProducts.slice(start, end);
        
        var products = products.filter(product => {
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
    
    startIndex() {
        return (this.pageNum - 1) * 25;
    },
    
    readableStartIndex() {
        return this.startIndex + 1;
    },
    
    endIndex() {
        
        var endIndex = this.startIndex + 25;
        
        if (endIndex > this.pageFilteredProducts.length) return this.pageFilteredProducts.length;
        return endIndex;
    },
    
    pageCount() {
        return Math.ceil(this.pageFilteredProducts.length / 25);
    }
    
};
