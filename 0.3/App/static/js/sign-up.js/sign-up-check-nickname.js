let nickname_input = document.getElementById('nickname');
let nickname_status = document.getElementById('nickname_status');
let button = document.getElementById('sign-up');
const API_URL = '/api/v1/unique_nickname/';

nickname_input.oninput = function () {
    if (nickname_input.value) {
        fetch(`${API_URL}${nickname_input.value}`)
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                if (data.unique_nickname === 1) {
                    nickname_status.innerHTML = "Этот никнейм свободен!"
                    nickname_status.style.color = "#03ea03";
                    button.disabled = false;
                } else {
                    nickname_status.innerHTML = "Этот никнейм Занят!"
                    nickname_status.style.color = "#ea0303";
                    button.disabled = true;
                }
            });
    } else {
        nickname_status.innerHTML = "Ваш уникальный ник";
        nickname_status.style.color = "";
    }

};