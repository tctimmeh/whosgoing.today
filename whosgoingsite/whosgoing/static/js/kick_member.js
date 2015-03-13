(function($) {
    KickMemberButton = function(element) {
        this.element = element;
        this.inviteId = this.element.data('user-id');
        this.userName = this.element.data('user-name');

        var self = this;
        this.element.click(function(e) { self.clicked(e); });
    };

    KickMemberButton.prototype.clicked = function(event) {
        var self = this;
        dcbase.popupAjaxForm({
            url: dcbase.createUrl(kickMemberUrl, this.userName),
            small: true,
            afterLoad: function(content) { self.setupForm(content); }
        });
    };

    KickMemberButton.prototype.setupForm = function(content) {
        content.find('#id_kick_user').val(this.inviteId);
        content.find('.kick-user-name').html(this.userName);
    };

    $.fn.kickMemberButton = function() {
        return this.each(function(index, obj) {
            new KickMemberButton($(obj));
        });
    };
}(jQuery));
