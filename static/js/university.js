function toggle_display_university(element){
    function toggle_display_university_block(element, status){
        element.classList.toggle('active-directions', status);
        element.children[0].children[3].children[0].children[1].innerText =
            status ? 'скрыть направления' : 'показать направления';
    }
    let univ = element.parentElement.parentElement.parentElement;
    let status = univ.classList.contains('active-directions');
    let r = $('.university');
    for (let i = 0; i < r.length; i++)
        if (r[i] != univ)
            toggle_display_university_block(r[i], false);
    toggle_display_university_block(univ, !status);
}
