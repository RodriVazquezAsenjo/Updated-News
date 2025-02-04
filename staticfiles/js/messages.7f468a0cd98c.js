document.addEventListener("DOMContentLoaded", function () {
    // Automatically hide the messages after 5 seconds
    setTimeout(function() {
        const messageContainer = document.querySelector('.messages');
        if (messageContainer) {
            messageContainer.style.opacity = 0; // Fade out the container
            setTimeout(function() {
                messageContainer.style.display = 'none'; // Hide the container after fading out
            }, 500); // Delay the hiding to match the fade-out transition
        }
    }, 5000); // Hide after 5 seconds

    // Dismiss messages manually when clicked
    const dismissButtons = document.querySelectorAll('.dismiss-message');
    dismissButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const message = button.closest('.alert');
            message.style.opacity = 0; // Fade out the message
            setTimeout(function() {
                message.style.display = 'none'; // Hide the message after fade-out
            }, 500); // Delay the hiding to match the fade-out transition
        });
    });
});