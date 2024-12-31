const tabs = document.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll('.tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs and tab contents
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(tc => tc.classList.remove('active'));

                // Add active class to the selected tab and corresponding tab content
                tab.classList.add('active');
                const contentId = tab.getAttribute('data-tab');
                document.getElementById(contentId).classList.add('active');
            });
        });

function openRoleForm(userId) {
    // Populate user_id in the hidden input
    document.getElementById("user_id").value = userId;

    // Display the modal
    const modal = document.getElementById("roleModal");
    modal.style.display = "block";
}

function closeRoleForm() {
    // Hide the modal
    const modal = document.getElementById("roleModal");
    modal.style.display = "none";
}

// Optional: Close modal when clicking outside of it
window.onclick = function (event) {
    const modal = document.getElementById("roleModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};
