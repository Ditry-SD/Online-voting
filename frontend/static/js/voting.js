// Ждем полной загрузки страницы
document.addEventListener('DOMContentLoaded', async () => {
    await loadCandidates();
});

// Функция загрузки списка кандидатов с сервера
async function loadCandidates() {
    try {
        // Отправляем GET-запрос к API
        const response = await fetch('/api/candidates');
        
        // Проверяем, успешен ли запрос
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }
        
        // Преобразуем ответ в JSON
        const candidates = await response.json();
        
        // Отображаем кандидатов на странице
        displayCandidates(candidates);
        
    } catch (error) {
        console.error('Ошибка:', error);
        showMessage('Не удалось загрузить список кандидатов. Попробуйте обновить страницу.', 'danger');
    }
}

// Функция отображения карточек кандидатов
function displayCandidates(candidates) {
    const container = document.getElementById('candidates-container');
    
    // Очищаем контейнер
    container.innerHTML = '';
    
    // Если кандидатов нет
    if (candidates.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center">
                <p class="text-muted">Нет доступных кандидатов для голосования.</p>
            </div>
        `;
        return;
    }
    
    // Создаем карточку для каждого кандидата
    candidates.forEach(candidate => {
        const cardHTML = `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">${escapeHTML(candidate.name)}</h5>
                        <p class="card-text">${escapeHTML(candidate.description)}</p>
                        <div class="vote-count">
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
    
    // Добавляем обработчики событий для всех кнопок
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', handleVote);
    });
}

// Функция обработки голосования
async function handleVote(event) {
    const button = event.target;
    const candidateId = button.dataset.id;
    const candidateName = button.dataset.name;
    
    try {
        // Отправляем POST-запрос для голосования
        const response = await fetch(`/api/vote/${candidateId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Получаем ответ от сервера
        const data = await response.json();
        
        if (response.ok) {
            // Успешное голосование
            showMessage(`✅ ${data.message} Вы проголосовали за "${candidateName}".`, 'success');
            
            // Делаем все кнопки неактивными
            disableAllButtons();
            
            // Обновляем страницу через 2 секунды
            setTimeout(() => {
                location.reload();
            }, 2000);
            
        } else {
            // Ошибка от сервера (например, повторное голосование)
            showMessage(`⚠️ ${data.detail}`, 'warning');
        }
        
    } catch (error) {
        console.error('Ошибка:', error);
        showMessage('Произошла ошибка при голосовании. Попробуйте позже.', 'danger');
    }
}

// Функция отключения всех кнопок голосования
function disableAllButtons() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.disabled = true;
        btn.textContent = '✓ Голос учтен';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');
    });
}

// Функция показа сообщений пользователю
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    
    // Устанавливаем класс и текст сообщения
    messageDiv.className = `alert alert-${type} alert-dismissible fade show`;
    messageDiv.innerHTML = `
        ${text}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Показываем сообщение
    messageDiv.style.display = 'block';
    
    // Автоматически скрываем через 5 секунд (если это успех)
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

// Функция для безопасного отображения HTML (защита от XSS)
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}