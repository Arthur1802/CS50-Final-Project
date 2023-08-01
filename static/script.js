document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_profile_data')
        .then(response => response.json())
        .then(data => {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');

            nameInput.value = data.name;
            emailInput.value = data.email;

            nameInput.addEventListener('focus', selectContent);
            emailInput.addEventListener('focus', selectContent);

            nameInput.addEventListener('blur', restoreOriginalData);
            emailInput.addEventListener('blur', restoreOriginalData);

            nameInput.dataset.originalValue = data.name;
            emailInput.dataset.originalValue = data.email;
        })
        .catch(error => console.error('Error fetching profile data:', error));
});

function selectContent(event) {
    event.target.select();
}

function restoreOriginalData(event) {
    const inputField = event.target;
    if (!inputField.value.trim()) {
        inputField.value = inputField.dataset.originalValue;
    }
}
document.addEventListener('DOMContentLoaded', function () {
    // Get references to the eye icons
    const seePasswdIcon = document.getElementById('see_passwd');
    const notSeePasswdIcon = document.getElementById('not_see_passwd');

    seePasswdIcon.addEventListener('click', function () {
        const passwdInput = document.getElementById('confPasswd');
        const inputType = passwdInput.getAttribute('type');
        passwdInput.setAttribute('type', inputType === 'text' ? 'password' : 'text');

        seePasswdIcon.classList.toggle('fa-eye');
        seePasswdIcon.classList.toggle('fa-eye-slash');
    });

    notSeePasswdIcon.addEventListener('click', function () {
        const passwdInput = document.getElementById('confPasswd');
        const inputType = passwdInput.getAttribute('type');
        passwdInput.setAttribute('type', inputType === 'text' ? 'password' : 'text');

        notSeePasswdIcon.classList.toggle('fa-eye');
        notSeePasswdIcon.classList.toggle('fa-eye-slash');
    });
});