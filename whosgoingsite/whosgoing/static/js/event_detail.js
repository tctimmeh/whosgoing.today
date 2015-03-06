var whosgoing = whosgoing || {};

whosgoing.NotifyAddressCheckbox = function(element) {
    this.element = element;
    this.address = this.element.data('address');

    var self = this;
    this.element.click(function(e){ self.clicked(e); });
};

whosgoing.NotifyAddressCheckbox.prototype.clicked = function(event) {
    event.stopPropagation();
    this.showWaitIndicator();
    this.sendToggleRequest();
};

whosgoing.NotifyAddressCheckbox.prototype.showWaitIndicator = function() {
    var indicator = this.element.find('.indicator');
    indicator.removeClass('glyphicon-ok glyphicon-remove text-success text-danger');
    indicator.addClass('glyphicon-time');
};

whosgoing.NotifyAddressCheckbox.prototype.sendToggleRequest = function() {
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

function setupInviteForm() {
    dcbase.createUserTypeahead('#id_address');
    $('#invite-form').ajaxForm({
        target: '#invite-dialog-body',
        success: function () {
            setupInviteForm();
        },
        error: function (xhr, response, status) {
            $('#invite-messages').html('<div class="text-danger">Failed to submit invitation: ' + status + '</div>')
        }
    });
}

function windowResized() {
    var width = $(window).width();
    if (width < 768) {
        $('#event-action-buttons').removeClass('btn-group-vertical').addClass('btn-group');
    }
    else {
        $('#event-action-buttons').removeClass('btn-group').addClass('btn-group-vertical');
    }
}

$(document).ready(function () {
    $('.notify-address').each(function(index, obj) {
        new whosgoing.NotifyAddressCheckbox($(obj));
    });

    setupInviteForm();
    windowResized();
    $(window).resize(windowResized);

    $('#kick-form').ajaxForm(function (response, status) {
        window.location.reload();
    });

    $('.kick-button').click(function (event) {
        var element = $(event.target);
        var userId = element.data('user-id');
        var userName = element.data('user-name');
        $('#kick-user-input').val(userId);
        $('#kick-user-name').html(userName);
        $('#kick-dialog').modal();
    });
});
