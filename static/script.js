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
        passwdInput.setAttribute('type', inputType === 'password' ? 'text' : 'password');

        notSeePasswdIcon.classList.toggle('fa-eye');
        notSeePasswdIcon.classList.toggle('fa-eye-slash');
    });
    seePasswdIcon.addEventListener('click', function () {
        const passwdInput = document.getElementById('passwd');
        const inputType = passwdInput.getAttribute('type');
        passwdInput.setAttribute('type', inputType === 'text' ? 'password' : 'text');

        seePasswdIcon.classList.toggle('fa-eye');
        seePasswdIcon.classList.toggle('fa-eye-slash');
    });

    notSeePasswdIcon.addEventListener('click', function () {
        const passwdInput = document.getElementById('passwd');
        const inputType = passwdInput.getAttribute('type');
        passwdInput.setAttribute('type', inputType === 'password' ? 'text' : 'password');

        notSeePasswdIcon.classList.toggle('fa-eye');
        notSeePasswdIcon.classList.toggle('fa-eye-slash');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const descInput = document.getElementById('description');

    origValue = descInput.value;

    descInput.addEventListener('focus', selectContent);
    descInput.addEventListener('blur', restoreOriginalData);
    descInput.dataset.originalValue = origValue;
});