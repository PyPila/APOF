$('#menu-toggle').click(function(event) {
    event.preventDefault();
    $('#wrapper').toggleClass('toggled');
});

$(document).ready(function () {
    var topNav = $('#top-nav');

    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('#top-nav').addClass('fades');
        } else {
            $('#top-nav').removeClass('fades');
        }
    });
});
