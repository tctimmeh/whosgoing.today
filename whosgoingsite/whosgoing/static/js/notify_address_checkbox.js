(function($) {
    NotifyAddressCheckbox = function(element) {
        this.element = element;
        this.address = this.element.data('address');

        var self = this;
        this.element.click(function(e){ self.clicked(e); });
    };

    NotifyAddressCheckbox.prototype.clicked = function(event) {
        event.stopPropagation();
        this.showWaitIndicator();
        this.sendToggleRequest();
    };

    NotifyAddressCheckbox.prototype.showWaitIndicator = function() {
        var indicator = this.element.find('.indicator');
        indicator.removeClass('glyphicon-ok glyphicon-remove text-success text-danger');
        indicator.addClass('glyphicon-time');
    };

    NotifyAddressCheckbox.prototype.sendToggleRequest = function() {
        $('<form />').ajaxSubmit({
            type: 'POST',
            url: toggleNotifyAddressUrl,
            data: {
                csrfmiddlewaretoken: $.cookie('csrftoken'),
                address: this.address
            },
            target: this.element,
            error: function (xhr, status, response, form) {
                console.log('error', xhr, status, response, form);
            }
        });
    };

    $.fn.notifyAddressCheckbox = function() {
        return this.each(function(index, obj) {
            new NotifyAddressCheckbox($(obj));
        });
    };
}(jQuery));

