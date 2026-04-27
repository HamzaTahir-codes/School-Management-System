// static/js/timetable/builder.js

const modal = document.getElementById('assignModal');
const form = document.getElementById('assignForm');

function openAssignModal(slotId, day, isEdit = false) {
    document.getElementById('modal_timeslot_id').value = slotId;
    document.getElementById('modal_day').value = day;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeAssignModal() {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    form.reset();
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

if (form) {
    form.onsubmit = function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const btn = document.getElementById('assignBtnText');
        const config = document.getElementById('timetable-config');
        const url = config.getAttribute('data-assign-url');
        
        btn.innerHTML = 'Syncing...';

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert("Error: " + data.error);
                btn.innerHTML = 'Lock Assignment';
            }
        });
    };
}

function removeEntry(pk) {
    if (confirm("Permanently remove this session from the schedule?")) {
        const config = document.getElementById('timetable-config');
        const baseUrl = config.getAttribute('data-remove-url');
        const url = baseUrl.replace('0', pk);
        
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert("Error: " + data.error);
            }
        });
    }
}
