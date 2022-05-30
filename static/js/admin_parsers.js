$(function(){
    $('.btn-sandwich').click(function(){
        $('#header').toggleClass('show-menu');
        $('.menu').first().toggleClass('show-menu');
    });
});