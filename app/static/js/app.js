function escapeHtml(text) {
    if (!text) return '';
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

function formatTime(ts) {
    if (!ts) return '';
    const d = new Date(ts);
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
}

function getToken() {
    return localStorage.getItem('token');
}

function getUser() {
    try {
        return JSON.parse(localStorage.getItem('user') || '{}');
    } catch {
        return {};
    }
}

function isLoggedIn() {
    return !!getToken();
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

function updateNav() {
    const navRight = document.querySelector('.nav-right');
    if (!navRight) return;

    const token = getToken();
    const user = getUser();

    if (token && user.username) {
        navRight.innerHTML = `
            <span class="user-greeting">👋 ${escapeHtml(user.username)}</span>
            <a href="/profile" class="nav-link">个人主页</a>
            ${user.is_admin ? '<a href="/admin" class="nav-link">⚙️ 管理</a>' : ''}
            <a href="#" class="nav-link" onclick="logout()">退出</a>
        `;
    } else {
        navRight.innerHTML = `
            <a href="/login" class="nav-link">登录</a>
            <a href="/register" class="nav-link btn-primary">注册</a>
        `;
    }
}

async function apiFetch(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(endpoint, {
        ...options,
        headers
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || '请求失败');
    }

    return data;
}

async function loadPosts(containerId, page = 1, perPage = 20) {
    const container = document.getElementById(containerId);
    if (!container) return;

    try {
        const data = await apiFetch(`/api/posts?page=${page}&per_page=${perPage}`);

        if (data.data && data.data.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>📭 还没有帖子</p>
                    <a href="/new-post" class="btn btn-primary">发布第一个帖子</a>
                </div>
            `;
            return;
        }

        let html = '';
        data.data.forEach(post => {
            html += `
                <div class="post-card" onclick="location.href='/post/${post.id}'">
                    <h3 class="post-title">${escapeHtml(post.title)}</h3>
                    <div class="post-meta">
                        <span>👤 ${escapeHtml(post.username || '匿名')}</span>
                        <span>📅 ${formatTime(post.created_at)}</span>
                        <span>💬 ${post.reply_count || 0} 回复</span>
                        ${post.is_pinned ? '<span class="badge-pinned">📌 置顶</span>' : ''}
                    </div>
                    <p class="post-preview">${escapeHtml(post.content).substring(0, 200)}${post.content.length > 200 ? '...' : ''}</p>
                </div>
            `;
        });

        container.innerHTML = html;

        const paginationContainer = document.getElementById('pagination');
        if (paginationContainer) {
            const totalPages = data.pagination.pages;
            if (totalPages > 1) {
                let pagesHtml = '';
                for (let i = 1; i <= totalPages; i++) {
                    pagesHtml += `<button class="page-btn ${i === page ? 'active' : ''}" onclick="loadPosts('${containerId}', ${i})">${i}</button>`;
                }
                paginationContainer.innerHTML = pagesHtml;
            } else {
                paginationContainer.innerHTML = '';
            }
        }

    } catch (error) {
        container.innerHTML = `
            <div class="error-state">❌ 加载失败: ${error.message}</div>
        `;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateNav();
});
