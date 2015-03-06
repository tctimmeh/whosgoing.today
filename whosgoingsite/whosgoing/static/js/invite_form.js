var whosgoing = whosgoing || {};

whosgoing.setupInviteForm = function() {
    dcbase.createUserTypeahead('#id_address');
    $('#invite-form').ajaxForm({
        target: '#invite-dialog-body',
        success: function () {
            whosgoing.setupInviteForm();
        },
        error: function (xhr, response, status) {
            $('#invite-messages').html('<div class="text-danger">Failed to submit invitation: ' + status + '</div>')
        }
    });
};
