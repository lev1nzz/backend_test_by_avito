// ===== THEME MANAGEMENT =====
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    const icon = document.querySelector('.theme-icon');
    if (icon) {
        icon.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    }
}

// Загрузка темы
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const html = document.documentElement;
    html.setAttribute('data-theme', savedTheme);
    
    const icon = document.querySelector('.theme-icon');
    if (icon) {
        icon.textContent = savedTheme === 'dark' ? '🌙' : '☀️';
    }
}

// ===== DOM REFS =====
const urlInput = document.getElementById('urlInput');
const shortenBtn = document.getElementById('shortenBtn');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const shortUrl = document.getElementById('shortUrl');
const originalUrl = document.getElementById('originalUrl');
const createdAt = document.getElementById('createdAt');
const charCount = document.getElementById('charCount');
const errorText = document.getElementById('errorText');

// ===== MAIN FUNCTION =====
async function shortenUrl() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Пожалуйста, введите ссылку');
        return;
    }
    
    try {
        new URL(url);
    } catch (e) {
        showError('Пожалуйста, введите корректный URL (начинается с http:// или https://)');
        return;
    }
    
    setLoading(true);
    hideAllResults();
    
    try {
        const response = await fetch('/short_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка сервера');
        }
        
        showResult(data, url);
        urlInput.value = '';
        
    } catch (error) {
        showError(error.message || 'Произошла ошибка при сокращении ссылки');
    } finally {
        setLoading(false);
    }
}

// ===== UI FUNCTIONS =====
function showResult(data, original) {
    const fullShortUrl = window.location.origin + '/' + data.short_url;
    
    shortUrl.href = fullShortUrl;
    shortUrl.textContent = fullShortUrl;
    originalUrl.textContent = data.url || original;
    createdAt.textContent = new Date().toLocaleString('ru-RU');
    charCount.textContent = (data.url || original).length;
    
    resultContainer.style.display = 'block';
    errorContainer.style.display = 'none';
}

function showError(message) {
    errorText.textContent = message;
    errorContainer.style.display = 'block';
    resultContainer.style.display = 'none';
}

function hideAllResults() {
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
}

function setLoading(loading) {
    const btnText = shortenBtn.querySelector('.btn-text');
    const spinner = shortenBtn.querySelector('.btn-spinner');
    
    if (loading) {
        btnText.textContent = 'Сокращение...';
        spinner.style.display = 'inline-block';
        shortenBtn.disabled = true;
        urlInput.disabled = true;
    } else {
        btnText.textContent = 'Сократить';
        spinner.style.display = 'none';
        shortenBtn.disabled = false;
        urlInput.disabled = false;
        urlInput.focus();
    }
}

// ===== COPY =====
function copyToClipboard() {
    const url = shortUrl.textContent;
    const copyBtn = document.getElementById('copyBtn');
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => {
            showCopySuccess(copyBtn);
        }).catch(() => {
            fallbackCopy(url, copyBtn);
        });
    } else {
        fallbackCopy(url, copyBtn);
    }
}

function fallbackCopy(text, btn) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(btn);
    } catch (err) {
        alert('Не удалось скопировать ссылку. Пожалуйста, скопируйте вручную.');
    }
    
    document.body.removeChild(textarea);
}

function showCopySuccess(btn) {
    const originalText = btn.querySelector('.copy-text');
    const originalContent = originalText.textContent;
    originalText.textContent = 'Скопировано!';
    btn.classList.add('copied');
    
    setTimeout(() => {
        originalText.textContent = originalContent;
        btn.classList.remove('copied');
    }, 2000);
}

// ===== KEYBOARD SHORTCUTS =====
urlInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        shortenUrl();
    }
});

// ===== INIT =====
loadTheme();  // Загружаем тему
urlInput.focus();

// Делаем функцию глобальной для onclick в HTML
window.toggleTheme = toggleTheme;