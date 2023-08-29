document.addEventListener("DOMContentLoaded", function(event) {
    const taskSelect = document.getElementById('taskSelect');

    taskSelect.addEventListener('change', function () {
        const selectedTaskId = this.value;
        if (selectedTaskId) {
            window.location.href = `/editTask?taskId = ${selectedTaskId}`;
        }
    });
});