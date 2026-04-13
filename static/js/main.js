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

    // Password Visibility Toggle Feature
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'relative flex items-center w-full';
        
        // Insert wrapper before input, then move input inside wrapper
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        // Add padding to prevent text flowing under the icon
        input.style.paddingRight = '2.5rem';

        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'absolute right-3 text-slate-400 hover:text-indigo-500 transition-colors focus:outline-none';
        
        // Eye SVG (Open)
        const eyeOpenSVG = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>`;
        // Eye SVG (Closed)
        const eyeClosedSVG = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path></svg>`;
        
        toggleBtn.innerHTML = eyeOpenSVG;
        
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (input.type === 'password') {
                input.type = 'text';
                toggleBtn.innerHTML = eyeClosedSVG;
            } else {
                input.type = 'password';
                toggleBtn.innerHTML = eyeOpenSVG;
            }
        });

        wrapper.appendChild(toggleBtn);
    });
});
