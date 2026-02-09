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
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight - header.offsetHeight - footer.offsetHeight;
    
    // Redraw circles if game is active
    if (gameState.gameId && gameState.circles.length > 0) {
        drawCircles();
    }
}

// Start a new game
async function startGame() {
    const playerName = document.getElementById('player-name').value.trim() || 'Player';
    const numbersCount = parseInt(document.getElementById('circle-count').value);
    
    gameState.playerName = playerName;
    gameState.numbersCount = numbersCount;
    
    // Get canvas dimensions
    const canvas = document.getElementById('game-canvas');
    resizeCanvas();
    
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
                canvas_height: canvas.height
            })
        });
        
        const data = await response.json();
        
        gameState.gameId = data.game_id;
        gameState.circles = data.circles;
        gameState.currentNumber = 1;
        gameState.startTime = Date.now();
        
        // Switch to game screen
        switchScreen('game-screen');
        
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
        // Circle color based on state
        const fillColor = circle.clicked ? '#2ecc71' : '#3498db';
        const strokeColor = circle.clicked ? '#27ae60' : '#2980b9';
        
        // Draw circle
        ctx.beginPath();
        ctx.arc(circle.x, circle.y, circle.radius, 0, 2 * Math.PI);
        ctx.fillStyle = fillColor;
        ctx.fill();
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // Draw number
        ctx.fillStyle = 'white';
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
            <div style="font-size: 3rem; margin-bottom: 20px;">🎉 Congratulations!</div>
            <div>You completed all ${gameState.numbersCount} numbers in ${time} seconds!</div>
        `;
    } else {
        messageDiv.className = 'result-message failure';
        messageDiv.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 20px;">❌ Game Over!</div>
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
        const response = await fetch('/api/leaderboard');
        const data = await response.json();
        
        if (data.length === 0) {
            leaderboardDiv.innerHTML = '<div class="loading">No records yet. Be the first!</div>';
            return;
        }
        
        let html = '';
        data.forEach((entry, index) => {
            const rank = index + 1;
            const medal = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : '';
            
            html += `
                <div class="leaderboard-entry">
                    <div class="leaderboard-rank">${medal} #${rank}</div>
                    <div class="leaderboard-name">${entry.name}</div>
                    <div class="leaderboard-time">${entry.time}s</div>
                    <div class="leaderboard-circles">${entry.circles} circles</div>
                </div>
            `;
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