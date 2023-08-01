document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_profile_data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('name').value = data.username;
            document.getElementById('email').value = data.email;
        })
        .catch(error => console.error('Error fetching profile data:', error));
});