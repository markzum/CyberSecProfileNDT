// AR Team Management Script
document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startAR');
    const instructions = document.getElementById('instructions');
    const arScene = document.getElementById('arScene');
    const arStats = document.getElementById('arStats');
    const markerCount = document.getElementById('markerCount');
    const foundMarkersContainer = document.getElementById('foundMarkers');
    
    // Отслеживание найденных маркеров
    const foundMarkers = new Set();
    const totalMarkers = 10;
    
    // Инициализация точек маркеров
    function initMarkerDots() {
        for (let i = 1; i <= totalMarkers; i++) {
            const dot = document.createElement('div');
            dot.className = 'marker-dot';
            dot.id = `marker-dot-${i}`;
            dot.title = `Marker ${i}`;
            foundMarkersContainer.appendChild(dot);
        }
    }
    
    // Запуск AR
    if (startButton) {
        startButton.addEventListener('click', function() {
            console.log('Запуск AR режима...');
            
            // Скрыть инструкции
            instructions.style.display = 'none';
            
            // Показать AR сцену - AR.js сам запросит камеру
            arScene.style.display = 'block';
            
            // Показать статистику
            arStats.style.display = 'block';
            
            console.log('AR режим активирован - ожидание камеры...');
            
            // Ждём инициализации AR.js
            waitForARInit();
        });
    }
    
    // Ожидание инициализации AR
    function waitForARInit() {
        let checkCount = 0;
        const maxChecks = 50;
        
        const checkInterval = setInterval(() => {
            checkCount++;
            
            const sceneEl = document.querySelector('a-scene');
            if (sceneEl && sceneEl.hasLoaded) {
                clearInterval(checkInterval);
                console.log('✓ AR инициализирована');
                initMarkerTracking();
            } else if (checkCount >= maxChecks) {
                clearInterval(checkInterval);
                console.warn('Таймаут инициализации AR');
                alert('AR не инициализировался. Попробуйте обновить страницу.');
            }
        }, 200);
    }
    
    // Инициализация отслеживания маркеров
    function initMarkerTracking() {
        // Получаем все маркеры
        const markers = document.querySelectorAll('a-marker');
        
        console.log(`Найдено маркеров: ${markers.length}`);
        
        markers.forEach((marker, index) => {
            const markerId = index + 1;
            
            // Событие при обнаружении маркера
            marker.addEventListener('markerFound', function() {
                console.log(`Маркер ${markerId} обнаружен`);
                markMarkerAsFound(markerId);
                
                // Звуковое уведомление (опционально)
                playFoundSound();
                
                // Вибрация на мобильных устройствах
                if (navigator.vibrate) {
                    navigator.vibrate(100);
                }
            });
            
            // Событие при потере маркера
            marker.addEventListener('markerLost', function() {
                console.log(`Маркер ${markerId} потерян`);
            });
        });
        
        console.log('✓ Отслеживание маркеров настроено');
    }
    
    // Отметить маркер как найденный
    function markMarkerAsFound(markerId) {
        if (!foundMarkers.has(markerId)) {
            foundMarkers.add(markerId);
            
            // Обновить UI
            const dot = document.getElementById(`marker-dot-${markerId}`);
            if (dot) {
                dot.classList.add('found');
            }
            
            // Обновить счетчик
            updateMarkerCount();
            
            // Проверить, все ли маркеры найдены
            if (foundMarkers.size === totalMarkers) {
                showCompletionMessage();
            }
        }
    }
    
    // Обновить счетчик маркеров
    function updateMarkerCount() {
        markerCount.textContent = `${foundMarkers.size} / ${totalMarkers}`;
    }
    
    // Показать сообщение о завершении
    function showCompletionMessage() {
        setTimeout(() => {
            const completionDiv = document.createElement('div');
            completionDiv.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
                color: #000;
                padding: 2rem 3rem;
                border-radius: 20px;
                font-size: 1.5rem;
                font-weight: bold;
                z-index: 10000;
                box-shadow: 0 20px 60px rgba(0, 255, 136, 0.6);
                animation: slideIn 0.5s ease-out;
            `;
            completionDiv.innerHTML = `
                <div style="text-align: center;">
                    🎉 Поздравляем! 🎉<br>
                    <span style="font-size: 1.2rem;">Вы нашли всю команду!</span>
                </div>
            `;
            document.body.appendChild(completionDiv);
            
            // Добавляем анимацию
            const style = document.createElement('style');
            style.textContent = `
                @keyframes slideIn {
                    from {
                        transform: translate(-50%, -50%) scale(0);
                        opacity: 0;
                    }
                    to {
                        transform: translate(-50%, -50%) scale(1);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(style);
            
            // Вибрация
            if (navigator.vibrate) {
                navigator.vibrate([100, 50, 100, 50, 100]);
            }
            
            // Удалить сообщение через 5 секунд
            setTimeout(() => {
                completionDiv.style.animation = 'slideIn 0.5s ease-out reverse';
                setTimeout(() => completionDiv.remove(), 500);
            }, 5000);
        }, 500);
    }
    
    // Звук при обнаружении (опционально)
    function playFoundSound() {
        // Создаем простой звуковой сигнал
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    }
    
    // Инициализация при загрузке
    initMarkerDots();
    
    // Обработка ориентации экрана
    function handleOrientation() {
        const isPortrait = window.innerHeight > window.innerWidth;
        if (isPortrait && arScene.style.display === 'block') {
            console.log('Портретная ориентация обнаружена');
        }
    }
    
    window.addEventListener('orientationchange', handleOrientation);
    window.addEventListener('resize', handleOrientation);
    
    // Обработка ошибок AR.js
    window.addEventListener('arjs-video-loaded', function() {
        console.log('AR.js: Видео загружено');
    });
    
    // Информация о производительности
    let lastLog = Date.now();
    setInterval(() => {
        if (arScene.style.display === 'block' && Date.now() - lastLog > 30000) {
            console.log(`AR статистика: ${foundMarkers.size}/${totalMarkers} маркеров найдено`);
            lastLog = Date.now();
        }
    }, 30000);
});

// Функция для создания скриншота AR (бонус)
function captureARScreenshot() {
    const scene = document.querySelector('a-scene');
    if (scene) {
        scene.components.screenshot.capture('perspective');
    }
}

// Экспорт для использования в других скриптах
window.ARTeam = {
    captureScreenshot: captureARScreenshot
};
