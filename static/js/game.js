// Game state
let gameState = {
    gameId: null,
    circles: [],
    startTime: null,
    timerInterval: null,
    currentNumber: 1,
    playerName: '',
    numbersCount: 10
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadLeaderboard('leaderboard-start');
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('start-btn').addEventListener('click', startGame);
    document.getElementById('quit-btn').addEventListener('click', quitGame);
    document.getElementById('play-again-btn').addEventListener('click', playAgain);
    document.getElementById('menu-btn').addEventListener('click', backToMenu);
    
    // Setup canvas
    const canvas = document.getElementById('game-canvas');
    canvas.addEventListener('click', handleCanvasClick);
    
    // Resize canvas to fill available space
    window.addEventListener('resize', resizeCanvas);
}

// Resize canvas to fill screen
function resizeCanvas() {
    const canvas = document.getElementById('game-canvas');
    const header = document.querySelector('.game-header');
    const footer = document.querySelector('.game-footer');
    
    // Canvas fills the entire viewport
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Redraw circles if game is active
    if (gameState.gameId && gameState.circles.length > 0) {
        drawCircles();
    }
}

// Calculate safe play area boundaries
function getSafePlayArea() {
    const header = document.querySelector('.game-header');
    const footer = document.querySelector('.game-footer');
    
    // Get actual heights
    const headerHeight = header ? header.offsetHeight : 0;
    // Footer is positioned absolutely in corner, so we need padding for it
    const footerPadding = 80; // Height from bottom to avoid footer button
    
    // Add extra padding for safety
    const topPadding = headerHeight + 40; // 40px extra padding below header
    const bottomPadding = footerPadding + 40; // 40px extra padding above footer area
    const sidePadding = 40; // 40px padding from sides
    
    return {
        minX: sidePadding,
        maxX: window.innerWidth - sidePadding,
        minY: topPadding,
        maxY: window.innerHeight - bottomPadding
    };
}

// Start a new game
async function startGame() {
    const playerName = document.getElementById('player-name').value.trim() || 'Player';
    const numbersCount = parseInt(document.getElementById('circle-count').value);
    
    gameState.playerName = playerName;
    gameState.numbersCount = numbersCount;
    
    // Switch to game screen first to ensure DOM elements are rendered and measurable
    // This allows getSafePlayArea() to accurately calculate header/footer dimensions
    switchScreen('game-screen');
    
    // Get canvas dimensions
    const canvas = document.getElementById('game-canvas');
    resizeCanvas();
    
    // Calculate safe play area
    const safeArea = getSafePlayArea();
    
    try {
        const response = await fetch('/api/game/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                player_name: playerName,
                numbers_count: numbersCount,
                canvas_width: canvas.width,
                canvas_height: canvas.height,
                safe_area: safeArea
            })
        });
        
        const data = await response.json();
        
        gameState.gameId = data.game_id;
        gameState.circles = data.circles;
        gameState.currentNumber = 1;
        gameState.startTime = Date.now();
        
        // Update UI
        document.getElementById('player-display').textContent = playerName;
        document.getElementById('next-number').textContent = '1';
        
        // Draw circles
        drawCircles();
        
        // Start timer
        startTimer();
        
    } catch (error) {
        console.error('Error starting game:', error);
        alert('Failed to start game. Please check your connection and try again.\n\nError: ' + error.message);
    }
}

// Draw circles on canvas
function drawCircles() {
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw each circle
    gameState.circles.forEach(circle => {
        // Circle color based on state - minimal styling
        const fillColor = circle.clicked ? '#3f3f46' : '#27272a'; // Dark gray tones
        const strokeColor = circle.clicked ? '#eab308' : '#52525b'; // Mustard yellow when clicked, steel gray otherwise
        
        // Draw circle
        ctx.beginPath();
        ctx.arc(circle.x, circle.y, circle.radius, 0, 2 * Math.PI);
        ctx.fillStyle = fillColor;
        ctx.fill();
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 2; // Thinner border
        ctx.stroke();
        
        // Draw number
        ctx.fillStyle = circle.clicked ? '#eab308' : '#fafaf9'; // Mustard yellow when clicked, off-white otherwise
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(circle.number, circle.x, circle.y);
    });
}

// Handle canvas click
async function handleCanvasClick(event) {
    if (!gameState.gameId) return;
    
    const canvas = document.getElementById('game-canvas');
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    try {
        const response = await fetch('/api/game/click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: gameState.gameId,
                x: x,
                y: y
            })
        });
        
        const data = await response.json();
        
        if (data.result === 'empty') {
            // Empty space click - do nothing
            return;
        } else if (data.result === 'correct') {
            // Update circles
            gameState.circles = data.circles;
            gameState.currentNumber = data.current_number;
            
            // Update UI
            document.getElementById('next-number').textContent = data.current_number;
            
            // Redraw
            drawCircles();
            
        } else if (data.result === 'complete') {
            // Game complete
            stopTimer();
            gameState.circles = data.circles;
            drawCircles();
            
            setTimeout(() => {
                showResult(true, data.time, null, null);
            }, 500);
            
        } else if (data.result === 'wrong') {
            // Wrong click - game over
            stopTimer();
            
            setTimeout(() => {
                showResult(false, data.time, data.expected, data.clicked);
            }, 300);
        }
        
    } catch (error) {
        console.error('Error handling click:', error);
        alert('An error occurred. Please refresh the page and try again.\n\nError: ' + error.message);
    }
}

// Start timer
function startTimer() {
    gameState.timerInterval = setInterval(() => {
        const elapsed = (Date.now() - gameState.startTime) / 1000;
        document.getElementById('timer').textContent = elapsed.toFixed(2) + 's';
    }, 50);
}

// Stop timer
function stopTimer() {
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
        gameState.timerInterval = null;
    }
}

// Show result screen
function showResult(success, time, expectedNumber, clickedNumber) {
    const messageDiv = document.getElementById('result-message');
    
    if (success) {
        messageDiv.className = 'result-message success';
        messageDiv.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 20px;">Congratulations!</div>
            <div>You completed all ${gameState.numbersCount} numbers in ${time} seconds!</div>
        `;
    } else {
        messageDiv.className = 'result-message failure';
        messageDiv.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 20px;">Game Over</div>
            <div>You clicked the wrong number.</div>
            <div style="margin-top: 15px;">You needed: <strong>${expectedNumber}</strong></div>
            <div>You clicked: <strong>${clickedNumber}</strong></div>
            <div style="margin-top: 15px;">Time: ${time} seconds</div>
        `;
    }
    
    switchScreen('result-screen');
    loadLeaderboard('leaderboard-result');
}

// Load leaderboard
async function loadLeaderboard(elementId) {
    const leaderboardDiv = document.getElementById(elementId);
    
    try {
        // Fetch grouped leaderboard
        const response = await fetch('/api/leaderboard?grouped=true');
        const data = await response.json();
        
        // Check if there are any leaderboards
        if (Object.keys(data).length === 0) {
            leaderboardDiv.innerHTML = '<div class="loading">No records yet. Be the first!</div>';
            return;
        }
        
        let html = '';
        
        // Sort circle counts (5, 10, 15, 20)
        const circleCounts = Object.keys(data).map(Number).sort((a, b) => a - b);
        
        // Display each circle count group
        circleCounts.forEach(circleCount => {
            const entries = data[circleCount];
            
            html += `<div class="leaderboard-group">`;
            html += `<h3 class="leaderboard-group-title">${circleCount} Circles</h3>`;
            
            if (entries.length === 0) {
                html += `<div class="leaderboard-empty">No records yet</div>`;
            } else {
                entries.forEach((entry, index) => {
                    const rank = index + 1;
                    
                    html += `
                        <div class="leaderboard-entry">
                            <div class="leaderboard-rank">#${rank}</div>
                            <div class="leaderboard-name">${entry.name}</div>
                            <div class="leaderboard-time">${entry.time}s</div>
                        </div>
                    `;
                });
            }
            
            html += `</div>`;
        });
        
        leaderboardDiv.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        leaderboardDiv.innerHTML = '<div class="loading">Failed to load leaderboard</div>';
    }
}

// Switch between screens
function switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    
    // Resize canvas if switching to game screen
    if (screenId === 'game-screen') {
        setTimeout(resizeCanvas, 100);
    }
}

// Quit game
function quitGame() {
    if (confirm('Are you sure you want to quit? Your progress will be lost.')) {
        stopTimer();
        gameState.gameId = null;
        gameState.circles = [];
        backToMenu();
    }
}

// Play again
function playAgain() {
    startGame();
}

// Back to menu
function backToMenu() {
    stopTimer();
    gameState.gameId = null;
    gameState.circles = [];
    switchScreen('start-screen');
    loadLeaderboard('leaderboard-start');
}