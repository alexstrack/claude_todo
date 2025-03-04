document.addEventListener('DOMContentLoaded', function() {
    // Validate form submission
    const taskForm = document.getElementById('task-form');
    if (taskForm) {
        taskForm.addEventListener('submit', function(event) {
            const description = document.getElementById('description').value.trim();
            const dueDate = document.getElementById('due-date').value;
            
            if (!description) {
                event.preventDefault();
                alert('Please enter a task description');
                return false;
            }
            
            if (!dueDate) {
                event.preventDefault();
                alert('Please select a due date');
                return false;
            }
            
            return true;
        });
    }
    
    // Confirm task deletion
    const deleteButtons = document.querySelectorAll('.delete-task');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this task?')) {
                event.preventDefault();
            }
        });
    });
    
    // Set minimum date for due date input to today
    const dueDateInput = document.getElementById('due-date');
    if (dueDateInput) {
        const today = new Date();
        const year = today.getFullYear();
        let month = today.getMonth() + 1;
        let day = today.getDate();
        
        // Format date as YYYY-MM-DD for input[type="date"]
        month = month < 10 ? '0' + month : month;
        day = day < 10 ? '0' + day : day;
        
        const formattedDate = `${year}-${month}-${day}`;
        dueDateInput.setAttribute('min', formattedDate);
    }
});