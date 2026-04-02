// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // Intersection Observer for Slide Up animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add staggered delay based on index if multiple items appear at once
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                // Stop observing once animated
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-slide-up');
    animatedElements.forEach(el => observer.observe(el));

    // Mobile Sidebar Toggle Logic
    const toggleBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('app-sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (toggleBtn && sidebar && overlay) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.add('open');
            overlay.classList.add('open');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
        });
    }

    // Sidebar Dropdown Toggle Logic
    const dropdownToggles = document.querySelectorAll('.sidebar-dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const menu = toggle.nextElementSibling;
            const caret = toggle.querySelector('.caret-icon');
            
            if (menu.classList.contains('hidden')) {
                menu.classList.remove('hidden');
                // slight delay for fluid slide-down hack with max-height
                setTimeout(() => menu.style.maxHeight = menu.scrollHeight + 'px', 10);
                caret.classList.add('rotate-180');
            } else {
                menu.style.maxHeight = '0px';
                caret.classList.remove('rotate-180');
                setTimeout(() => menu.classList.add('hidden'), 300);
            }
        });
    });
});
