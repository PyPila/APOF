$('#menu-toggle').click(function(event) {
    event.preventDefault();
    $('.row').toggleClass('toggled');
});

$(document).ready(function () {
    var topNav = $('.navbar fixed-top');

    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('#top-nav').addClass('fades');
        } else {
            $('#top-nav').removeClass('fades');
        }
    });
});
