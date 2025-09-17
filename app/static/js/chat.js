/**
 * AI Chat System - JavaScript Module
 * Handles chat functionality, agent switching, WebSocket connections, and UI animations
 */

class AIChatSystem {
    constructor() {
        this.activeAgent = null;
        this.websocket = null;
        this.chatHistory = [];
        this.isConnected = false;
        this.messageQueue = [];
        
        this.init();
    }
    
    /**
     * Initialize the chat system
     */
    init() {
        this.setupEventListeners();
        this.initializeWebSocket();
        this.loadChatHistory();
    }
    
    /**
     * Set up event listeners for chat interface
     */
    setupEventListeners() {
        // Message input handling
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        if (messageInput && sendButton) {
            // Send message on Enter key
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            // Send button click
            sendButton.addEventListener('click', () => {
                this.sendMessage();
            });
            
            // Auto-resize textarea
            messageInput.addEventListener('input', this.autoResizeTextarea);
        }
        
        // Agent selection handling
        const agentCards = document.querySelectorAll('.agent-card');
        agentCards.forEach(card => {
            card.addEventListener('click', (e) => {
                const agentId = card.dataset.agentId;
                if (agentId) {
                    this.switchAgent(agentId);
                }
            });
        });
        
        // Chat actions
        document.addEventListener('click', (e) => {
            if (e.target.matches('.clear-chat-btn')) {
                this.clearChat();
            }
            if (e.target.matches('.export-chat-btn')) {
                this.exportChat();
            }
        });
    }
    
    /**
     * Initialize WebSocket connection
     */
    initializeWebSocket() {
        if (!window.WebSocket) {
            console.warn('WebSocket not supported in this browser');
            return;
        }
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ai/ws`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.updateConnectionStatus(true);
                this.processMessageQueue();
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                this.attemptReconnection();
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateConnectionStatus(false);
            };
            
        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
            this.fallbackToHTTP();
        }
    }
    
    /**
     * Handle incoming WebSocket messages
     */
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'message':
                this.displayMessage(data.content, 'agent', data.agent_id);
                break;
            case 'typing':
                this.showTypingIndicator(data.agent_id);
                break;
            case 'typing_stopped':
                this.hideTypingIndicator(data.agent_id);
                break;
            case 'agent_status':
                this.updateAgentStatus(data.agent_id, data.status);
                break;
            case 'error':
                this.handleError(data.message);
                break;
            default:
                console.warn('Unknown message type:', data.type);
        }
    }
    
    /**
     * Send a message to the active agent
     */
    sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || !this.activeAgent) {
            return;
        }
        
        // Display user message
        this.displayMessage(message, 'user');
        
        // Clear input
        messageInput.value = '';
        this.autoResizeTextarea.call(messageInput);
        
        // Send message
        const messageData = {
            type: 'message',
            content: message,
            agent_id: this.activeAgent,
            timestamp: new Date().toISOString()
        };
        
        if (this.isConnected) {
            this.websocket.send(JSON.stringify(messageData));
        } else {
            // Fallback to HTTP request
            this.sendMessageHTTP(messageData);
        }
        
        // Add to history
        this.chatHistory.push({
            role: 'user',
            content: message,
            timestamp: new Date().toISOString(),
            agent_id: this.activeAgent
        });
        
        this.saveChatHistory();
    }
    
    /**
     * Display a message in the chat interface
     */
    displayMessage(content, role = 'user', agentId = null) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        
        // Add agent info for agent messages
        let agentInfo = '';
        if (role === 'agent' && agentId) {
            const agentData = this.getAgentData(agentId);
            agentInfo = `
                <div class=\"message-header\">
                    <span class=\"agent-icon\">${agentData.icon || '🤖'}</span>
                    <span class=\"agent-name\">${agentData.name || agentId}</span>
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            ${agentInfo}
            <div class=\"message-content\">${this.formatMessage(content)}</div>
            <div class=\"message-timestamp\">${new Date().toLocaleTimeString()}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        
        // Add animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        
        // Trigger animation
        requestAnimationFrame(() => {
            messageDiv.style.transition = 'all 0.3s ease-out';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        });
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    /**
     * Format message content (markdown, links, etc.)
     */
    formatMessage(content) {
        // Basic markdown support
        content = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>')                // Italic
            .replace(/`(.*?)`/g, '<code>$1</code>')              // Inline code
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>') // Code blocks
            .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>'); // Links
        
        return content;
    }
    
    /**
     * Switch to a different agent
     */
    switchAgent(agentId) {
        if (this.activeAgent === agentId) {
            return;
        }
        
        const previousAgent = this.activeAgent;
        this.activeAgent = agentId;
        
        // Update UI
        this.updateActiveAgentUI(agentId, previousAgent);
        
        // Show agent switch message
        this.showAgentSwitchMessage(agentId, previousAgent);
        
        // Notify server about agent switch
        if (this.isConnected) {
            this.websocket.send(JSON.stringify({
                type: 'switch_agent',
                agent_id: agentId,
                previous_agent: previousAgent
            }));
        }
        
        // Load agent-specific chat history
        this.loadAgentChatHistory(agentId);
    }
    
    /**
     * Update UI to reflect active agent
     */
    updateActiveAgentUI(newAgentId, previousAgentId) {
        // Update agent cards
        const agentCards = document.querySelectorAll('.agent-card');
        agentCards.forEach(card => {
            if (card.dataset.agentId === newAgentId) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });
        
        // Update chat header
        const chatHeader = document.getElementById('chatHeader');
        if (chatHeader) {
            const agentData = this.getAgentData(newAgentId);
            chatHeader.innerHTML = `
                <div class=\"active-agent-info\">
                    <span class=\"agent-icon\">${agentData.icon || '🤖'}</span>
                    <div class=\"agent-details\">
                        <h4>${agentData.name || newAgentId}</h4>
                        <p>${agentData.description || 'AI Assistant'}</p>
                    </div>
                </div>
            `;
        }
        
        // Update input placeholder
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            const agentData = this.getAgentData(newAgentId);
            messageInput.placeholder = `Chat with ${agentData.name || newAgentId}...`;
        }
    }
    
    /**
     * Show agent switch notification
     */
    showAgentSwitchMessage(newAgentId, previousAgentId) {
        const agentData = this.getAgentData(newAgentId);
        const message = `Switched to ${agentData.name || newAgentId}`;
        
        this.displaySystemMessage(message);
    }
    
    /**
     * Display system message
     */
    displaySystemMessage(content) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';
        messageDiv.innerHTML = `
            <div class=\"system-content\">
                <i class=\"fas fa-info-circle\"></i>
                ${content}
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    /**
     * Show typing indicator
     */
    showTypingIndicator(agentId) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        // Remove existing typing indicator
        const existingIndicator = chatMessages.querySelector('.typing-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        const agentData = this.getAgentData(agentId);
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message agent-message typing-indicator';
        typingDiv.innerHTML = `
            <div class=\"message-header\">
                <span class=\"agent-icon\">${agentData.icon || '🤖'}</span>
                <span class=\"agent-name\">${agentData.name || agentId}</span>
            </div>
            <div class=\"typing-animation\">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    /**
     * Hide typing indicator
     */
    hideTypingIndicator(agentId) {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    /**
     * Auto-resize textarea
     */
    autoResizeTextarea() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    }
    
    /**
     * Scroll chat to bottom
     */
    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    /**
     * Clear chat history
     */
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                chatMessages.innerHTML = '';
            }
            
            this.chatHistory = [];
            this.saveChatHistory();
        }
    }
    
    /**
     * Export chat history
     */
    exportChat() {
        const chatData = {
            timestamp: new Date().toISOString(),
            agent: this.activeAgent,
            messages: this.chatHistory
        };
        
        const dataStr = JSON.stringify(chatData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `chat-export-${new Date().toISOString().split('T')[0]}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }
    
    /**
     * Load chat history from localStorage
     */
    loadChatHistory() {
        try {
            const saved = localStorage.getItem('ai_chat_history');
            if (saved) {
                this.chatHistory = JSON.parse(saved);
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }
    
    /**
     * Save chat history to localStorage
     */
    saveChatHistory() {
        try {
            localStorage.setItem('ai_chat_history', JSON.stringify(this.chatHistory));
        } catch (error) {
            console.error('Failed to save chat history:', error);
        }
    }
    
    /**
     * Get agent data by ID
     */
    getAgentData(agentId) {
        // This would typically come from a global agents object or API
        const defaultAgents = {
            'strategist': { name: 'Business Strategist', icon: '📊' },
            'developer': { name: 'Software Developer', icon: '💻' },
            'girlfriend': { name: 'Virtual Girlfriend', icon: '💝' },
            'coderbot': { name: 'Coder Bot', icon: '🤖' }
        };
        
        return defaultAgents[agentId] || { name: agentId, icon: '🤖' };
    }
    
    /**
     * Update connection status indicator
     */
    updateConnectionStatus(connected) {
        const statusIndicator = document.getElementById('connectionStatus');
        if (statusIndicator) {
            statusIndicator.className = connected ? 'connected' : 'disconnected';
            statusIndicator.title = connected ? 'Connected' : 'Disconnected';
        }
    }
    
    /**
     * Attempt to reconnect WebSocket
     */
    attemptReconnection() {
        setTimeout(() => {
            if (!this.isConnected) {
                console.log('Attempting to reconnect...');
                this.initializeWebSocket();
            }
        }, 3000);
    }
    
    /**
     * Fallback to HTTP for browsers without WebSocket support
     */
    fallbackToHTTP() {
        console.log('Falling back to HTTP requests');
        // Implement HTTP polling or long-polling as fallback
    }
    
    /**
     * Send message via HTTP (fallback method)
     */
    async sendMessageHTTP(messageData) {
        try {
            const response = await fetch('/ai/api/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(messageData)
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.response) {
                    this.displayMessage(data.response, 'agent', messageData.agent_id);
                }
            } else {
                throw new Error('HTTP request failed');
            }
        } catch (error) {
            console.error('Failed to send message via HTTP:', error);
            this.handleError('Failed to send message. Please try again.');
        }
    }
    
    /**
     * Handle errors
     */
    handleError(message) {
        this.displaySystemMessage(`Error: ${message}`);
    }
}

// Initialize chat system when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chatMessages') || document.querySelector('.agent-card')) {
        window.aiChat = new AIChatSystem();
    }
});

// Export for use in other modules
window.AIChatSystem = AIChatSystem;