// static/js/common.js

/**
 * Toast Notification Logic with Shatter Effect
 */
document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast-item');

    toasts.forEach(toast => {
        let dismissTimeout;
        let shattered = false;

        const removeToast = () => {
            if (shattered) return;
            toast.classList.add('toast-leaving');
            setTimeout(() => toast.remove(), 300);
        };

        const shatterToast = (e) => {
            if (shattered) return;
            shattered = true;
            clearTimeout(dismissTimeout);

            const rect = toast.getBoundingClientRect();
            // Spawn particles
            for (let i = 0; i < 25; i++) {
                const p = document.createElement('div');
                p.className = 'butterfly-particle';

                // Start point near click
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                p.style.left = x + 'px';
                p.style.top = y + 'px';

                // Trajectories spreading out and floating up
                const angle = Math.random() * Math.PI * 2;
                const velocity = 40 + Math.random() * 80;
                const tx = Math.cos(angle) * velocity;
                const ty = Math.sin(angle) * velocity - 40;
                const rot = (Math.random() - 0.5) * 500;

                p.style.setProperty('--tx', `${tx}px`);
                p.style.setProperty('--ty', `${ty}px`);
                p.style.setProperty('--rot', `${rot}deg`);

                p.style.animation = `flutterAway ${0.5 + Math.random() * 0.5}s cubic-bezier(0.25, 1, 0.5, 1) forwards`;
                toast.appendChild(p);
            }

            // Hide main content
            Array.from(toast.children).forEach(c => {
                if (!c.classList.contains('butterfly-particle')) c.style.opacity = '0';
            });
            toast.style.background = 'transparent';
            toast.style.boxShadow = 'none';
            toast.style.border = 'none';

            setTimeout(() => toast.remove(), 1000);
        };

        // Click to shatter
        toast.addEventListener('click', shatterToast);

        // Auto dismiss
        dismissTimeout = setTimeout(removeToast, 5000);
    });
});
