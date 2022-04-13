$(function(){
    $('input[name=ins_number]').mask('999-999-999 99', {autoclear: false});
    $('form').on('submit', function(e){
        let ins = $('input[name=ins_number]')[0];
        if (!ins.value.match(/[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}/)){
            //ins.value = '';
            $('.error-mark').toggleClass('show', true);
            $('.error').toggleClass('show', true);
            e.preventDefault()
        } else{
            $('.error-mark').toggleClass('show', false);
            $('.error').toggleClass('show', false);
        }
    });
    /*$('input[name=ins_number]').on('focusout', function(e){
       let ins = e.target;
        if (!ins.value.match(/[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}/)){
            $('.error-mark').toggleClass('show', true);
            $('.error').toggleClass('show', true);
        } else{
            $('.error-mark').toggleClass('show', false);
            $('.error').toggleClass('show', false);
        }
    });*/
})