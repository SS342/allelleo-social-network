function bg_like() {

    heart = document.getElementById('bg-like');
    if (heart.className == 'bi bi-heart fa-fw pe-1'){
        heart.className = 'bi bi-heart-fill fa-fw pe-1';
        // TODO добавить +1 в бд к лайкнутым бэкграундам

    } else {
        heart.className = 'bi bi-heart fa-fw pe-1';
        // TODO убавить 1 в бд к лайкнутым бэкграундам

    }
}