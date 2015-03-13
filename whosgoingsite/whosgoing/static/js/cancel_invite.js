(function($) {
    CancelInviteButton = function(element) {
        this.element = element;
        this.inviteId = this.element.data('invite-id');

        var self = this;
        this.element.click(function(e) { self.clicked(e); });
    };

    CancelInviteButton.prototype.clicked = function(event) {
        var self = this;
        dcbase.popupAjaxForm({
            url: dcbase.createUrl(cancelInviteUrl, this.inviteId)
        });
    };

    $.fn.cancelInviteButton = function() {
        return this.each(function(index, obj) {
            new CancelInviteButton($(obj));
        });
    };
}(jQuery));
