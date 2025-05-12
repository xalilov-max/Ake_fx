console.log("Script loaded");
// Navbarni yopish uchun
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
    });
});

// Alertlarni avtomatik yopish
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-dark-mode");
    const body = document.body;

    // Tungi rejimni saqlash uchun localStorage'dan o'qish
    const isDarkMode = localStorage.getItem("dark-mode") === "true";
    if (isDarkMode) {
        body.classList.add("dark-mode");
        toggleButton.textContent = "☀️ Light Mode";
    }

    toggleButton.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        const isDarkMode = body.classList.contains("dark-mode");
        localStorage.setItem("dark-mode", isDarkMode); // Tungi rejimni saqlash
        toggleButton.textContent = isDarkMode ? "☀️ Light Mode" : "🌙 Night Mode";
    });

    console.log("Night Mode script initialized");
});