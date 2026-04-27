const canvas = document.getElementById('particle-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    
    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    // Smooth mouse tracking
    const mouse = { x: width / 2, y: height / 2, targetX: width / 2, targetY: height / 2, isActive: false };
    
    window.addEventListener('mousemove', (e) => {
        mouse.targetX = e.x;
        mouse.targetY = e.y;
        mouse.isActive = true;
    });
    
    window.addEventListener('mouseout', () => {
        mouse.isActive = false;
    });

    let time = 0;

    // Generate elegant silk threads
    const numThreads = 35;
    const threads = [];
    
    // SchoolOS Theme Colors (Translucent for overlapping blend)
    const colors = [
        'rgba(99, 102, 241, 0.15)',   // Indigo
        'rgba(168, 85, 247, 0.12)',   // Purple
        'rgba(236, 72, 153, 0.10)',   // Pink
        'rgba(56, 189, 248, 0.15)'    // Sky Blue
    ];

    for(let i = 0; i < numThreads; i++) {
        threads.push({
            color: colors[i % colors.length],
            freq: 0.001 + Math.random() * 0.0015,
            speed: 0.004 + Math.random() * 0.008,
            amp: 150 + Math.random() * 200,
            yOffset: 0.2 + Math.random() * 0.6, // Spread across 20% to 80% of screen height
            phase: Math.random() * Math.PI * 2,
            weight: 0.5 + Math.random() * 2.5
        });
    }

    function draw() {
        ctx.clearRect(0, 0, width, height);
        time += 1;

        // Smoothly interpolate mouse position for elegant fluid feeling
        if (mouse.isActive) {
            mouse.x += (mouse.targetX - mouse.x) * 0.06;
            mouse.y += (mouse.targetY - mouse.y) * 0.06;
        } else {
            // Drift to center when inactive
            mouse.x += (width/2 - mouse.x) * 0.02;
            mouse.y += (height/2 - mouse.y) * 0.02;
        }

        // Draw each silk thread
        threads.forEach((thread) => {
            ctx.beginPath();
            
            let baseY = height * thread.yOffset;
            let resolution = 30; // pixels per segment
            let segments = Math.ceil(width / resolution);
            
            for (let i = 0; i <= segments; i++) {
                let x = i * resolution;
                
                // Natural organic wave movement (combining two sine waves for complexity)
                let wave1 = Math.sin(x * thread.freq + time * thread.speed + thread.phase);
                let wave2 = Math.cos(x * thread.freq * 0.5 - time * thread.speed * 0.5);
                let waveY = wave1 * wave2 * thread.amp;
                
                let naturalY = baseY + waveY;
                
                // Cursor attraction logic
                let dx = mouse.x - x;
                let dy = mouse.y - naturalY;
                let dist = Math.sqrt(dx*dx + dy*dy);
                
                // Gravity well size (affects how wide the cursor pull is)
                let pullRadius = 700;
                let pullForce = Math.max(0, pullRadius - dist) / pullRadius; 
                
                // Ease the force for a smooth, non-linear bending effect (cubic curve)
                pullForce = Math.pow(pullForce, 3); 
                
                // Apply the pull - thread bends gracefully towards the cursor
                let finalY = naturalY + (mouse.y - naturalY) * pullForce * 0.85;
                
                // Add a very subtle horizontal pinch towards the cursor
                let finalX = x + (mouse.x - x) * pullForce * 0.15;
                
                if (i === 0) {
                    ctx.moveTo(finalX, finalY);
                } else {
                    // Using lineTo with high resolution creates a smooth curve automatically
                    ctx.lineTo(finalX, finalY);
                }
            }
            
            ctx.strokeStyle = thread.color;
            ctx.lineWidth = thread.weight;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.stroke();
        });

        requestAnimationFrame(draw);
    }
    
    // Start animation
    draw();
}
