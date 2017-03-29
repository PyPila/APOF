$('.menu-toggle').click(function(event) {
    event.preventDefault();
    $('.row').toggleClass('toggled');
});

$(document).ready(function () {
    var topNav = $('nav.fixed-top.navbar-light');

    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $(topNav).addClass('fades');
        } else {
            $(topNav).removeClass('fades');
        }
    });
    $('.navbar-toggle').on('click', function(){
        $('.sidebar').hide();
    });
});
