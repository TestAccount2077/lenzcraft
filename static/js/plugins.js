(function ( $ ) {
    $.fn.resetModal = function (options) {
        
        this.find('input:text, input[type=email], input:password, textarea').val('');

        var settings = $.extend(
            {
                defaultValues: {},
                redactorFields: []
            },
            options
        );
        
        var This = this;
        
        $.each(settings.defaultValues, (selector, value) => {
            This.find(selector).val(value);
        });
        
        $.each(settings.redactorFields, (index, selector) => $R(selector, 'source.setCode', ''));
        
        return this;
        
    }

    $.fn.disable = function (options) {
        
        var settings = $.extend(
            {
                changeText: true
            },
            options
        );
        
        this.prop('disabled', true);
        
        if (settings.changeText){
            this.text(this.attr('data-loading-text'));
        }
        
        return this;
        
    }

    $.fn.enable = function (options) {
        
        var settings = $.extend(
            {
                changeText: true
            },
            options
        );
        
        this.prop('disabled', false);
        
        if (settings.changeText) {
            this.text(this.attr('data-normal-text'));
        }
        
        return this;
        
    }
}( jQuery ));
