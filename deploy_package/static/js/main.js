/**
 * KPI GPT - Frontend JavaScript
 * Created by: Famim Farhaz
 * 
 * Interactive chat functionality with real-time messaging and smooth animations
 */

class KPIGPT {
    constructor() {
        this.isLoading = false;
        this.isSystemReady = false;
        this.messageHistory = [];
        this.settings = {
            darkMode: true,
            streamingMode: false,
            soundEffects: false
        };
        
        this.init();
    }
    
    init() {
        this.loadSettings();
        this.initializeElements();
        this.setupEventListeners();
        this.checkSystemStatus();
        this.loadExamples();
        this.hideLoadingOverlay();
    }
    
    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.getElementById('charCount');
        
        // UI elements
        this.sidebar = document.getElementById('sidebar');
        this.menuBtn = document.getElementById('menuBtn');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.clearChatBtn = document.getElementById('clearChatBtn');
        this.settingsBtn = document.getElementById('settingsBtn');
        this.settingsModal = document.getElementById('settingsModal');
        this.closeSettings = document.getElementById('closeSettings');
        this.resetBtn = document.getElementById('resetBtn');
        
        // Status elements
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.systemInfo = document.getElementById('systemInfo');
        this.docCount = document.getElementById('docCount');
        this.modelName = document.getElementById('modelName');
        this.exampleQuestions = document.getElementById('exampleQuestions');
        
        // Containers
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toastContainer = document.getElementById('toastContainer');
    }
    
    setupEventListeners() {
        // Chat input
        this.messageInput.addEventListener('input', () => this.handleInputChange());
        this.messageInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // UI controls
        this.menuBtn.addEventListener('click', () => this.toggleSidebar());
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        this.settingsBtn.addEventListener('click', () => this.openSettings());
        this.closeSettings.addEventListener('click', () => this.closeSettingsModal());
        this.resetBtn.addEventListener('click', () => this.resetDatabase());
        
        // Modal close on background click
        this.settingsModal.addEventListener('click', (e) => {
            if (e.target === this.settingsModal) {
                this.closeSettingsModal();
            }
        });
        
        // Settings
        document.getElementById('darkMode').addEventListener('change', (e) => {
            this.settings.darkMode = e.target.checked;
            this.saveSettings();
        });
        
        document.getElementById('streamingMode').addEventListener('change', (e) => {
            this.settings.streamingMode = e.target.checked;
            this.saveSettings();
        });
        
        document.getElementById('soundEffects').addEventListener('change', (e) => {
            this.settings.soundEffects = e.target.checked;
            this.saveSettings();
        });
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
        
        // Close sidebar on outside click (mobile)
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && this.sidebar.classList.contains('open')) {
                if (!this.sidebar.contains(e.target) && e.target !== this.menuBtn) {
                    this.toggleSidebar(false);
                }
            }
        });
    }
    
    handleInputChange() {
        const length = this.messageInput.value.length;
        this.charCount.textContent = length;
        
        // Update send button state
        this.updateSendButtonState();
    }
    
    handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    updateSendButtonState() {
        const hasText = this.messageInput.value.trim().length > 0;
        const isReady = this.isSystemReady && !this.isLoading;
        this.sendBtn.disabled = !hasText || !isReady;
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading || !this.isSystemReady) return;
        
        this.isLoading = true;
        this.updateSendButtonState();
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.charCount.textContent = '0';
        this.autoResizeTextarea();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await this.callAPI('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            if (response.success) {
                this.addMessage(response.answer, 'bot', {
                    sources: response.sources,
                    model: response.model_used
                });
                
                // Play sound effect
                if (this.settings.soundEffects) {
                    this.playSoundEffect('message');
                }
            } else {
                this.addMessage(`Sorry, I encountered an error: ${response.error}`, 'bot', {
                    isError: true
                });
                this.showToast(`Error: ${response.error}`, 'error');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Sorry, I encountered a connection error. Please try again.', 'bot', {
                isError: true
            });
            this.showToast('Connection error. Please try again.', 'error');
        } finally {
            this.hideTypingIndicator();
            this.isLoading = false;
            this.updateSendButtonState();
            this.scrollToBottom();
        }
    }
    
    addMessage(text, sender, metadata = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        if (sender === 'user') {
            avatar.innerHTML = '<img src="/static/images/user-profile.jpg" alt="User Profile">';
        } else {
            avatar.innerHTML = '<i class="fas fa-robot"></i>';
        }
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;
        
        bubble.appendChild(messageText);
        
        // Add sources if available
        if (metadata.sources && metadata.sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'message-sources';
            
            const sourcesTitle = document.createElement('div');
            sourcesTitle.className = 'sources-title';
            sourcesTitle.innerHTML = '<i class="fas fa-book"></i> Sources';
            sourcesDiv.appendChild(sourcesTitle);
            
            metadata.sources.slice(0, 3).forEach(source => {
                const sourceItem = document.createElement('div');
                sourceItem.className = 'source-item';
                sourceItem.innerHTML = `
                    <span class="source-section">${source.section}</span>
                    <span class="source-score">${(source.similarity_score || 0).toFixed(2)}</span>
                `;
                sourcesDiv.appendChild(sourceItem);
            });
            
            bubble.appendChild(sourcesDiv);
        }
        
        // Add metadata
        const metadataDiv = document.createElement('div');
        metadataDiv.className = 'message-metadata';
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.innerHTML = `
            <i class="fas fa-clock"></i>
            <span>${new Date().toLocaleTimeString()}</span>
        `;
        
        metadataDiv.appendChild(timeDiv);
        
        if (metadata.model) {
            const modelDiv = document.createElement('div');
            modelDiv.className = 'message-model';
            modelDiv.innerHTML = `<i class="fas fa-microchip"></i> ${metadata.model}`;
            metadataDiv.appendChild(modelDiv);
        }
        
        content.appendChild(bubble);
        content.appendChild(metadataDiv);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Store in history
        this.messageHistory.push({
            text,
            sender,
            timestamp: Date.now(),
            metadata
        });
        
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear the chat?')) {
            // Remove all messages except welcome message
            const messages = this.chatMessages.querySelectorAll('.message');
            messages.forEach(message => message.remove());
            
            this.messageHistory = [];
            this.showToast('Chat cleared', 'success');
        }
    }
    
    toggleSidebar(forceState = null) {
        if (forceState === null) {
            this.sidebar.classList.toggle('open');
        } else {
            this.sidebar.classList.toggle('open', forceState);
        }
    }
    
    openSettings() {
        this.settingsModal.style.display = 'flex';
        
        // Update settings UI
        document.getElementById('darkMode').checked = this.settings.darkMode;
        document.getElementById('streamingMode').checked = this.settings.streamingMode;
        document.getElementById('soundEffects').checked = this.settings.soundEffects;
    }
    
    closeSettingsModal() {
        this.settingsModal.style.display = 'none';
    }
    
    async resetDatabase() {
        if (!confirm('Are you sure you want to reset the database? This will clear all cached data.')) {
            return;
        }
        
        this.showLoadingOverlay('Resetting database...');
        
        try {
            const response = await this.callAPI('/api/system/reset', {
                method: 'POST'
            });
            
            if (response.success) {
                this.showToast('Database reset successfully!', 'success');
                this.checkSystemStatus();
            } else {
                this.showToast(`Reset failed: ${response.message}`, 'error');
            }
        } catch (error) {
            console.error('Error resetting database:', error);
            this.showToast('Failed to reset database', 'error');
        } finally {
            this.hideLoadingOverlay();
        }
    }
    
    async checkSystemStatus() {
        try {
            const response = await this.callAPI('/api/system/status');
            
            if (response.status === 'ready') {
                this.isSystemReady = true;
                this.statusDot.className = 'status-dot ready';
                this.statusText.textContent = 'System Ready';
                
                // Update system info
                if (response.info) {
                    this.docCount.textContent = response.info.database?.document_count || '-';
                    this.modelName.textContent = response.info.models?.generation || '-';
                }
            } else if (response.status === 'error') {
                this.isSystemReady = false;
                this.statusDot.className = 'status-dot error';
                this.statusText.textContent = 'System Error';
            } else {
                this.isSystemReady = false;
                this.statusDot.className = 'status-dot';
                this.statusText.textContent = 'Initializing...';
                
                // Check again after a delay
                setTimeout(() => this.checkSystemStatus(), 3000);
            }
        } catch (error) {
            console.error('Error checking system status:', error);
            this.isSystemReady = false;
            this.statusDot.className = 'status-dot error';
            this.statusText.textContent = 'Connection Error';
        }
        
        this.updateSendButtonState();
    }
    
    async loadExamples() {
        try {
            const response = await this.callAPI('/api/examples');
            
            if (response.examples) {
                this.exampleQuestions.innerHTML = '';
                
                response.examples.slice(0, 6).forEach(example => {
                    const exampleDiv = document.createElement('div');
                    exampleDiv.className = 'example-question';
                    exampleDiv.textContent = example;
                    exampleDiv.addEventListener('click', () => {
                        this.messageInput.value = example;
                        this.handleInputChange();
                        this.autoResizeTextarea();
                        this.toggleSidebar(false);
                        this.messageInput.focus();
                    });
                    this.exampleQuestions.appendChild(exampleDiv);
                });
            }
        } catch (error) {
            console.error('Error loading examples:', error);
            this.exampleQuestions.innerHTML = '<div class="loading-examples">Failed to load examples</div>';
        }
    }
    
    showLoadingOverlay(text = 'Loading...') {
        this.loadingOverlay.style.display = 'flex';
        const loadingText = this.loadingOverlay.querySelector('h3');
        if (loadingText) {
            loadingText.textContent = text;
        }
    }
    
    hideLoadingOverlay() {
        this.loadingOverlay.style.display = 'none';
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Remove toast after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOutToast 0.3s ease forwards';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 5000);
    }
    
    playSoundEffect(type) {
        if (!this.settings.soundEffects) return;
        
        // Create simple sound effects using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            if (type === 'message') {
                oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
            }
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        } catch (error) {
            console.warn('Sound effects not supported:', error);
        }
    }
    
    loadSettings() {
        try {
            const saved = localStorage.getItem('kpiGptSettings');
            if (saved) {
                this.settings = { ...this.settings, ...JSON.parse(saved) };
            }
        } catch (error) {
            console.warn('Error loading settings:', error);
        }
    }
    
    saveSettings() {
        try {
            localStorage.setItem('kpiGptSettings', JSON.stringify(this.settings));
        } catch (error) {
            console.warn('Error saving settings:', error);
        }
    }
    
    async callAPI(endpoint, options = {}) {
        const response = await fetch(endpoint, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
}

// Add custom CSS animation for toast slide out
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutToast {
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.kpiGPT = new KPIGPT();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.kpiGPT) {
        // Check system status when page becomes visible again
        window.kpiGPT.checkSystemStatus();
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.kpiGPT && window.innerWidth > 768) {
        // Close sidebar on desktop view
        window.kpiGPT.toggleSidebar(false);
    }
});
