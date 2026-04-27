// static/js/accounts/dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('studentChart');
    if (!canvas) return;

    // Get data from data attributes
    const labels = JSON.parse(canvas.getAttribute('data-labels') || '[]');
    const chartData = JSON.parse(canvas.getAttribute('data-values') || '[]');
    
    if (labels.length === 0) return;

    const ctx = canvas.getContext('2d');
    
    // Create custom gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(99, 102, 241, 0.6)');
    gradient.addColorStop(1, 'rgba(99, 102, 241, 0.05)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Student Count',
                data: chartData,
                backgroundColor: gradient,
                borderColor: '#6366f1',
                borderWidth: 3,
                borderRadius: 12,
                borderSkipped: false,
                maxBarThickness: 50
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    cornerRadius: 12,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.03)', drawBorder: false },
                    ticks: { font: { weight: 'bold' }, color: '#94a3b8', stepSize: 1 }
                },
                x: {
                    grid: { display: false, drawBorder: false },
                    ticks: { font: { weight: 'bold' }, color: '#64748b' }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
});
