$(document).ready(function () {
    $('.menu-toggle').click(function(event) {
        event.preventDefault();
        $('.row').toggleClass('toggled');
    });

    $('.btn-info').on('click', function(){
        var ammount = $(this).parent().siblings('.ammount'),
            form = ammount.children('.form');
        form.submit();
    });

    $('.btn.btn-danger').on('click', function(){
        var modal = $(this).siblings('.modal');
        modal.modal('toggle');
    });

    $('.btn.btn-success.btn-block').on('click', function(){
        var modal = $(this).siblings('.modal');
        modal.modal('toggle');
    });
});
