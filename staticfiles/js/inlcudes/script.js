document.addEventListener('DOMContentLoaded', function () {
    const dropdownButtons = document.querySelectorAll('.dropdown-btn');

    dropdownButtons.forEach(button => {
        button.addEventListener('click', function () {
            const dropdownContent = this.nextElementSibling;

            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            } else {
                dropdownContent.style.display = 'block';
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    // Get the current URL path
    const currentPath = window.location.pathname;

    // Loop through all nav links
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const linkPath = link.getAttribute("href");
        if (currentPath === linkPath) {
            link.classList.add("active"); // Add the active class to the matching link
        } else {
            link.classList.remove("active"); // Remove active class from other links
        }
    });
});
