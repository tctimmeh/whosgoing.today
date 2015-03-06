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
