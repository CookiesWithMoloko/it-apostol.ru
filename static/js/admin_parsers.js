$(function(){
    $('.btn-sandwich').click(function(){
        $('#header').toggleClass('show-menu');
        $('.menu').first().toggleClass('show-menu');
    });
    $('.last_use-field').map((index,e) => {
        let d = new Date(parseInt(e.innerText)*1000);
        e.innerText =
            d.getHours() + ":" +
            d.getMinutes() + " " +
            d.getDate()  + "." +
            (d.getMonth()+1) + "." +
            d.getFullYear();

    });


});