// static/js/accounts/teacher_portal.js

let attendanceTimer;

function triggerConfetti() {
    const duration = 3 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

    const randomInRange = (min, max) => Math.random() * (max - min) + min;

    const interval = setInterval(function() {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            return clearInterval(interval);
        }

        const particleCount = 50 * (timeLeft / duration);
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
    }, 250);
}


function startAttendanceTimer(durationS) {
    const display = document.getElementById('otp-timer');
    const progress = document.getElementById('otp-progress');
    const resendBtn = document.getElementById('resend-btn');
    let timer = durationS;
    
    clearInterval(attendanceTimer);
    display.classList.remove('text-rose-500');
    if(resendBtn) resendBtn.classList.add('hidden');
    
    attendanceTimer = setInterval(() => {
        const seconds = parseInt(timer % 60, 10);
        display.textContent = seconds + 's';
        
        const percent = (timer / durationS) * 100;
        progress.style.width = percent + '%';

        if (--timer < 0) {
            clearInterval(attendanceTimer);
            display.textContent = "Expired";
            display.classList.add('text-rose-500');
            progress.style.width = '0%';
            if(resendBtn) resendBtn.classList.remove('hidden');
        }
    }, 1000);
}

// UI Helper for Toasts
function showToast(title, message, type = 'success') {
    const container = document.getElementById('floating-toasts');
    if (!container) {
        alert(title + ": " + message);
        return;
    }
    
    const toast = document.createElement('div');
    toast.className = `toast-item pointer-events-auto relative glass-panel p-4 rounded-xl text-slate-800 flex items-start gap-3 shadow-2xl border-l-4 ${type === 'error' ? 'border-rose-500' : 'border-indigo-500'} overflow-hidden cursor-pointer`;
    toast.style.animation = "slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards";
    
    toast.innerHTML = `
        <div class="flex-grow pt-0.5 font-medium text-sm">
            <strong class="block text-xs uppercase opacity-70">${title}</strong>
            ${message}
        </div>
        <button class="toast-close flex-shrink-0 text-slate-400 hover:text-slate-600 transition-colors p-1" onclick="this.parentElement.remove()">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
    `;
    
    toast.addEventListener('click', () => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    });

    container.appendChild(toast);
    setTimeout(() => {
        if(toast.parentElement) toast.remove();
    }, 5000);
}

function getDeviceID() {
    let deviceId = localStorage.getItem('schoolos_device_id');
    if (!deviceId) {
        deviceId = crypto.randomUUID ? crypto.randomUUID() : 'dev-' + Math.random().toString(36).substr(2, 9) + '-' + Date.now();
        localStorage.setItem('schoolos_device_id', deviceId);
    }
    return deviceId;
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

function initiateAttendance(isResend = false) {
    const config = document.getElementById('attendance-config');
    const url = config.getAttribute('data-initiate-url');
    
    const btn = document.querySelector('#attendance-default-state button');
    const resendBtn = document.getElementById('resend-btn');
    const originalText = btn.innerText;
    
    if (!isResend) {
        btn.disabled = true;
        btn.innerText = "Checking Network...";
    } else {
        resendBtn.disabled = true;
        resendBtn.innerText = "Sending...";
    }

    fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() }
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok && data.success) {
            document.getElementById('attendance-default-state').classList.add('hidden');
            document.getElementById('attendance-otp-state').classList.remove('hidden');
            document.getElementById('otp-display').innerText = data.otp;
            
            startAttendanceTimer(60);
            showToast("OTP Generated", "Please enter the code shown on the screen.");
        } else {
            throw new Error(data.error || "Establishment failed.");
        }
    })
    .catch(err => {
        showToast("Access Denied", err.message, "error");
        if (!isResend) {
            btn.disabled = false;
            btn.innerText = originalText;
        } else {
            resendBtn.disabled = false;
            resendBtn.innerText = "Didn't get code? Resend";
        }
    });
}

function verifyAttendance() {
    const config = document.getElementById('attendance-config');
    const url = config.getAttribute('data-verify-url');
    
    const otp = document.getElementById('attendance-otp-input').value;
    const deviceId = getDeviceID();
    const btn = document.querySelector('#attendance-otp-state button');
    
    if (otp.length !== 6) {
        showToast("Invalid Input", "Please enter a 6-digit OTP.", "error");
        return;
    }

    btn.disabled = true;
    btn.innerText = "Verifying...";

    const formData = new URLSearchParams();
    formData.append('otp', otp);
    formData.append('device_id', deviceId);

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok && data.success) {
            document.getElementById('attendance-otp-state').classList.add('hidden');
            document.getElementById('attendance-success-state').classList.remove('hidden');
            showToast("Verified", "Attendance marked successfully.");
            triggerConfetti();
        } else {
            throw new Error(data.error || "Verification failed.");
        }
    })
    .catch(err => {
        showToast("Error", err.message, "error");
        btn.disabled = false;
        btn.innerText = "Verify & Submit";
    });
}

function requestExtension(sectionId) {
    const config = document.getElementById('attendance-config');
    const url = config.getAttribute('data-extension-url');

    if(confirm("Are you sure you want to request an attendance extension from the admin?")) {
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                'section_id': sectionId,
                'duration': 15
            })
        })
        .then(res => res.json())
        .then(data => {
            if(data.success) {
                showToast("Request Sent", data.message);
                location.reload();
            } else {
                showToast("Error", data.error, "error");
            }
        });
    }
}
