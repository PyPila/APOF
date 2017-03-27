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
    $('.btn-info').on('click', function(){
        var price = $(this).parent().siblings('.price'),
            price_val = price.attr('value'),
            ammount = $(this).parent().siblings('.ammount'),
            ammount_val = ammount.children().val(),
            price = price_val * ammount,
            total_price = $(this).parent().siblings('.total-price');
        total_price.html(price);
    });
});
