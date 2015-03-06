(function($) {
    KickMemberButton = function(element) {
        this.element = element;
        this.userId = this.element.data('user-id');
        this.userName = this.element.data('user-name');

        var self = this;
        this.element.click(function(e) { self.clicked(e); });
    };

    KickMemberButton.prototype.clicked = function(event) {
        $('#kick-user-input').val(this.userId);
        $('#kick-user-name').html(this.userName);
        $('#kick-dialog').modal();
    };

    $.fn.kickMemberButton = function() {
        return this.each(function(index, obj) {
            new KickMemberButton($(obj));
        });
    };
}(jQuery));
