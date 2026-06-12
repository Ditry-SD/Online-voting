/**
 * Система онлайн голосования — клиентская логика
 * Автор: Морозов Д.В., ПИН-б-з-22-1
 */

// Хранилище текущих голосов для сравнения изменений
let currentVotes = {};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    await loadCandidates();
    // Автообновление каждые 3 секунды
    setInterval(updateVotes, 3000);
});

/**
 * Загрузка списка кандидатов с сервера
 */
async function loadCandidates() {
    try {
        const response = await fetch('/api/candidates');
        if (!response.ok) throw new Error('Ошибка загрузки');
        const candidates = await response.json();
        // Сохраняем начальные значения голосов
        candidates.forEach(c => { currentVotes[c.id] = c.votes; });
        displayCandidates(candidates);
    } catch (error) {
        showMessage('Не удалось загрузить список кандидатов.', 'danger');
    }
}

/**
 * Обновление счётчиков голосов без перезагрузки страницы
 * Сравнивает текущие значения с сохранёнными, обновляет только изменившиеся
 */
async function updateVotes() {
    try {
        const response = await fetch('/api/candidates');
        if (!response.ok) return;
        const candidates = await response.json();
        
        candidates.forEach(candidate => {
            const oldVotes = currentVotes[candidate.id] || 0;
            const newVotes = candidate.votes;
            
            // Обновляем только если количество изменилось
            if (newVotes !== oldVotes) {
                const badge = document.querySelector(`.vote-count[data-id="${candidate.id}"] .badge`);
                if (badge) {
                    // Анимация: увеличиваем и плавно возвращаем
                    badge.style.transform = 'scale(1.3)';
                    badge.style.transition = 'transform 0.2s ease';
                    badge.textContent = newVotes;
                    setTimeout(() => { badge.style.transform = 'scale(1)'; }, 200);
                }
                currentVotes[candidate.id] = newVotes;
            }
        });
    } catch(e) {}
}

/**
 * Отображение карточек кандидатов на странице
 */
function displayCandidates(candidates) {
    const container = document.getElementById('candidates-container');
    container.innerHTML = '';
    
    candidates.forEach(candidate => {
        const cardHTML = `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">${escapeHTML(candidate.name)}</h5>
                        <p class="card-text">${escapeHTML(candidate.description)}</p>
                        <div class="vote-count" data-id="${candidate.id}">
                            Голосов: <span class="badge bg-primary">${candidate.votes}</span>
                        </div>
                        <button class="btn btn-primary vote-btn" 
                                data-id="${candidate.id}"
                                data-name="${escapeHTML(candidate.name)}">
                            Голосовать
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', cardHTML);
    });
    
    // Назначаем обработчики на все кнопки голосования
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', handleVote);
    });
}

/**
 * Обработка нажатия кнопки "Голосовать"
 * Отправляет POST-запрос к API, блокирует кнопки при успехе
 */
async function handleVote(event) {
    const button = event.target;
    const candidateId = button.dataset.id;
    const candidateName = button.dataset.name;
    
    try {
        const response = await fetch(`/api/vote/${candidateId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        
        if (response.ok) {
            showMessage(`✅ ${data.message}`, 'success');
            disableAllButtons();
            await loadCandidates();
            // Через 3 секунды разблокируем кнопки
            setTimeout(() => {
                enableAllButtons();
                document.getElementById('message').style.display = 'none';
            }, 3000);
        } else {
            showMessage(`⚠️ ${data.detail}`, 'warning');
        }
    } catch (error) {
        showMessage('Ошибка при голосовании.', 'danger');
    }
}

/**
 * Блокировка всех кнопок после голосования
 */
function disableAllButtons() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.disabled = true;
        btn.textContent = '✓ Голос учтен';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');
    });
}

/**
 * Разблокировка кнопок голосования
 */
function enableAllButtons() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.disabled = false;
        btn.textContent = 'Голосовать';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-primary');
    });
}

/**
 * Отображение уведомлений пользователю
 */
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.className = `alert alert-${type} alert-dismissible fade show`;
    messageDiv.innerHTML = `${text}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    messageDiv.style.display = 'block';
}

/**
 * Защита от XSS-атак — экранирование HTML
 */
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}