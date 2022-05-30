$(function(){
    $('.btn-sandwich').click(function(){
        $('#header').toggleClass('show-menu');
        $('.menu').first().toggleClass('show-menu');
    });
    $('.last_use-field').forEach((e) => {
        e.innerText = new Date(parseInt(e.innerText)*1000).toUTCString();
    })
});