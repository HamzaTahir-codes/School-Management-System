// static/js/attendance/mark_students.js

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

function updateStats() {
    const cards = document.querySelectorAll('.student-card');
    const total = cards.length;
    let present = 0;
    let absent = 0;
    let marked = 0;

    cards.forEach(card => {
        const state = card.getAttribute('data-marked');
        if (state === 'present') {
            present++;
            marked++;
        } else if (state === 'absent') {
            absent++;
            marked++;
        }
    });

    const countPresentEl = document.getElementById('count-present');
    const countAbsentEl = document.getElementById('count-absent');
    const progressPercentEl = document.getElementById('progress-percent');

    if (countPresentEl) countPresentEl.innerText = present;
    if (countAbsentEl) countAbsentEl.innerText = absent;
    if (progressPercentEl) progressPercentEl.innerText = Math.round((marked / total) * 100) + '%';
}

function toggleAttendance(studentId) {
    const config = document.getElementById('attendance-config');
    const url = config.getAttribute('data-toggle-url');
    
    const card = document.getElementById(`student-${studentId}`);
    const badge = card.querySelector('.absolute.top-4.right-4 div');
    const currentState = card.getAttribute('data-marked');
    
    // Toggle Logic: none -> present -> absent -> present ...
    let nextState = 'present';
    if (currentState === 'present') nextState = 'absent';
    else if (currentState === 'absent') nextState = 'present';

    // Optimistic UI Update
    card.setAttribute('data-marked', nextState);
    card.classList.remove('border-slate-100', 'border-emerald-500', 'border-rose-500', 'bg-emerald-50/30', 'bg-rose-50/30');
    badge.classList.remove('bg-slate-100', 'bg-emerald-500', 'bg-rose-500', 'text-slate-300', 'text-white');
    
    if (nextState === 'present') {
        card.classList.add('border-emerald-500', 'bg-emerald-50/30');
        badge.classList.add('bg-emerald-500', 'text-white');
        badge.innerHTML = document.getElementById('icon-present').innerHTML;
    } else {
        card.classList.add('border-rose-500', 'bg-rose-50/30');
        badge.classList.add('bg-rose-500', 'text-white');
        badge.innerHTML = document.getElementById('icon-absent').innerHTML;
    }

    updateStats();

    // Backend Sync
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: new URLSearchParams({
            'student_id': studentId,
            'is_present': nextState === 'present'
        })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            alert("Error updating attendance: " + data.error);
            window.location.reload();
        }
    })
    .catch(err => {
        console.error(err);
        window.location.reload();
    });
}

document.addEventListener('DOMContentLoaded', updateStats);
