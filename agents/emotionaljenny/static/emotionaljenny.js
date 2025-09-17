// Emotional Jenny Agent JavaScript

class EmotionaljennyAgent {
    constructor() {
        this.agentId = 'emotionaljenny';
        this.personalityType = 'Emotional';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupWebSocket();
        this.loadConversationHistory();
    }

    setupEventListeners() {
        const sendButton = document.getElementById('sendButton');
        const messageInput = document.getElementById('messageInput');

        sendButton.addEventListener('click', () => this.sendMessage());
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    setupWebSocket() {
        // WebSocket setup for real-time communication
        if (typeof io !== 'undefined') {
            this.socket = io(`/${this.agentId}`);
            
            this.socket.on('connect', () => {
                console.log(`Connected to ${this.agentId}`);
            });

            this.socket.on('response', (data) => {
                this.addMessage(data.message, 'agent');
            });
        }
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        messageInput.value = '';

        // Send to server
        try {
            const response = await fetch(`/${this.agentId}/api/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.getSessionId()
                })
            });

            const data = await response.json();
            if (data.success) {
                this.addMessage(data.response, 'agent');
            } else {
                this.addMessage('Sorry, I encountered an error.', 'agent');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Connection error. Please try again.', 'agent');
        }
    }

    addMessage(content, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Add animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            messageDiv.style.transition = 'all 0.3s ease-out';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 50);
    }

    getSessionId() {
        let sessionId = localStorage.getItem(`${this.agentId}_session_id`);
        if (!sessionId) {
            sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            localStorage.setItem(`${this.agentId}_session_id`, sessionId);
        }
        return sessionId;
    }

    loadConversationHistory() {
        // Load previous conversation from localStorage or server
        const history = localStorage.getItem(`${this.agentId}_history`);
        if (history) {
            try {
                const messages = JSON.parse(history);
                messages.forEach(msg => {
                    this.addMessage(msg.content, msg.sender);
                });
            } catch (e) {
                console.error('Error loading conversation history:', e);
            }
        }
    }

    saveMessageToHistory(content, sender) {
        const history = JSON.parse(localStorage.getItem(`${this.agentId}_history`) || '[]');
        history.push({
            content,
            sender,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last 50 messages
        if (history.length > 50) {
            history.splice(0, history.length - 50);
        }
        
        localStorage.setItem(`${this.agentId}_history`, JSON.stringify(history));
    }
}

// Initialize agent when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EmotionaljennyAgent();
});
