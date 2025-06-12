class AuthManager {
    constructor() {
        this.currentUser = null;
        this.initElements();
        this.initEventListeners();
        this.checkAuthState();
    }

    initElements() {
        // Кнопки и формы
        this.loginBtn = document.getElementById('loginBtn');
        this.registerBtn = document.getElementById('registerBtn');
        this.logoutBtn = document.getElementById('logoutBtn');
        this.loginForm = document.getElementById('loginForm');
        this.registerForm = document.getElementById('registerForm');
        
        // Модальные окна
        this.loginModal = document.getElementById('loginModal');
        this.registerModal = document.getElementById('registerModal');
        
        // Контейнеры
        this.authButtons = document.getElementById('authButtons');
        this.userInfo = document.getElementById('userInfo');
        this.userName = document.getElementById('userName');
    }

    initEventListeners() {
        // Открытие модальных окон
        this.loginBtn.addEventListener('click', () => this.showModal(this.loginModal));
        this.registerBtn.addEventListener('click', () => this.showModal(this.registerModal));
        
        // Закрытие модальных окон
        document.querySelectorAll('.modal-close').forEach(button => {
            button.addEventListener('click', (e) => this.hideModal(e.target.closest('.modal')));
        });

        // Обработка форм
        this.loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        this.registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        this.logoutBtn.addEventListener('click', () => this.handleLogout());

        // Закрытие модального окна при клике вне его
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hideModal(e.target);
            }
        });
    }

    showModal(modal) {
        modal.classList.remove('hidden');
    }

    hideModal(modal) {
        modal.classList.add('hidden');
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            // Здесь должен быть запрос к серверу
            const response = await this.mockLoginRequest(email, password);
            this.setCurrentUser(response.user);
            this.hideModal(this.loginModal);
            this.loginForm.reset();
        } catch (error) {
            alert('Ошибка входа: ' + error.message);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const name = document.getElementById('registerName').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            // Здесь должен быть запрос к серверу
            const response = await this.mockRegisterRequest(name, email, password);
            this.setCurrentUser(response.user);
            this.hideModal(this.registerModal);
            this.registerForm.reset();
        } catch (error) {
            alert('Ошибка регистрации: ' + error.message);
        }
    }

    handleLogout() {
        this.setCurrentUser(null);
        localStorage.removeItem('user');
    }

    setCurrentUser(user) {
        this.currentUser = user;
        if (user) {
            this.authButtons.classList.add('hidden');
            this.userInfo.classList.remove('hidden');
            this.userName.textContent = user.name;
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            this.authButtons.classList.remove('hidden');
            this.userInfo.classList.add('hidden');
            this.userName.textContent = '';
        }
    }

    checkAuthState() {
        const savedUser = localStorage.getItem('user');
        if (savedUser) {
            this.setCurrentUser(JSON.parse(savedUser));
        }
    }

    // Временные методы для демонстрации (замените на реальные запросы к серверу)
    mockLoginRequest(email, password) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (email && password) {
                    resolve({
                        user: {
                            id: 1,
                            name: email.split('@')[0],
                            email: email
                        }
                    });
                } else {
                    reject(new Error('Неверные учетные данные'));
                }
            }, 500);
        });
    }

    mockRegisterRequest(name, email, password) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (name && email && password) {
                    resolve({
                        user: {
                            id: 1,
                            name: name,
                            email: email
                        }
                    });
                } else {
                    reject(new Error('Неверные данные регистрации'));
                }
            }, 500);
        });
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
}); 