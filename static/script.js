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

document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_tasks_data')
        .then(response => response.json())
        .then(data => {
            const titleInput = document.getElementById('title');
            const descriptionInput = document.getElementById('description');
            
            const dateStart = document.getElementById('dateStart');
            const day1 = document.getElementById('day1');
            const month1 = document.getElementById('month1');
            const year1 = document.getElementById('year1');
            
            const [yearStr1, monthStr1, dayStr1] = dateStart.split('-');

            const dateEnd = document.getElementById('dateEnd');
            const day2 = document.getElementById('day2');
            const month2 = document.getElementById('month2');
            const year2 = document.getElementById('year2');
            
            const [yearStr2, monthStr2, dayStr2] = dateEnd.split('-');

            const dateStartDay = parseInt(dayStr1);
            const dateStartMonth = parseInt(monthStr1);
            const dateStartYear = parseInt(yearStr1);

            const dateEndDay = parseInt(dayStr2);
            const dateEndMonth = parseInt(monthStr2);
            const dateEndYear = parseInt(yearStr2);

            titleInput.value = data.title;
            descriptionInput.value = data.description;

            day1.value = dateStartDay;
            month1.value = dateStartMonth;
            year1.value = dateStartYear;
            
            day2.value = dateEndDay;
            month2.value = dateEndMonth;
            year2.value = dateEndYear;

            titleInput.addEventListener('focus', selectContent);
            descriptionInput.addEventListener('focus', selectContent);

            titleInput.addEventListener('blur', restoreOriginalData);
            descriptionInput.addEventListener('blur', restoreOriginalData);

            titleInput.dataset.originalValue = data.title;
            descriptionInput.dataset.originalValue = data.description;
        })
        .catch(error => console.error('Error fetching profile data:', error));
});