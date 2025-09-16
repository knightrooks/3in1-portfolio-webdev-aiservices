// Main JavaScript for 3-in-1 Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation classes when elements come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.card, .feature-card, .benefit-item').forEach(el => {
        observer.observe(el);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Utility Functions
const Utils = {
    // Show loading state
    showLoading: function(element) {
        const originalText = element.innerHTML;
        element.innerHTML = '<span class="loading me-2"></span>Loading...';
        element.disabled = true;
        return originalText;
    },

    // Hide loading state
    hideLoading: function(element, originalText) {
        element.innerHTML = originalText;
        element.disabled = false;
    },

    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Chat functionality
const Chat = {
    container: null,
    input: null,

    init: function() {
        this.container = document.getElementById('chat-messages');
        this.input = document.getElementById('chat-input');
        
        if (this.input) {
            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }
    },

    sendMessage: function() {
        const message = this.input.value.trim();
        if (!message) return;

        this.addMessage(message, 'user');
        this.input.value = '';

        // Send to API
        fetch('/ai/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            this.addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        });
    },

    addMessage: function(text, sender) {
        if (!this.container) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        
        this.container.appendChild(messageDiv);
        this.container.scrollTop = this.container.scrollHeight;
    }
};

// Text Analysis functionality
const TextAnalysis = {
    init: function() {
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', this.analyzeText);
        }
    },

    analyzeText: function() {
        const textArea = document.getElementById('text-input');
        const resultsDiv = document.getElementById('analysis-results');
        const analyzeBtn = document.getElementById('analyze-btn');
        
        if (!textArea || !resultsDiv) return;
        
        const text = textArea.value.trim();
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        const originalBtnText = Utils.showLoading(analyzeBtn);

        fetch('/ai/api/analyze-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            TextAnalysis.displayResults(data, resultsDiv);
            Utils.hideLoading(analyzeBtn, originalBtnText);
        })
        .catch(error => {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<div class="alert alert-danger">Error analyzing text. Please try again.</div>';
            Utils.hideLoading(analyzeBtn, originalBtnText);
        });
    },

    displayResults: function(data, container) {
        const html = `
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="metric-card">
                        <div class="metric-value">${data.word_count}</div>
                        <div class="metric-label">Words</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="metric-card">
                        <div class="metric-value">${data.character_count}</div>
                        <div class="metric-label">Characters</div>
                    </div>
                </div>
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Sentiment Analysis</h6>
                            <div class="d-flex align-items-center">
                                <span class="badge bg-${data.sentiment === 'Positive' ? 'success' : data.sentiment === 'Negative' ? 'danger' : 'secondary'} me-2">
                                    ${data.sentiment}
                                </span>
                                <small class="text-muted">Confidence: ${(data.sentiment_confidence * 100).toFixed(1)}%</small>
                            </div>
                        </div>
                    </div>
                </div>
                ${data.keywords.length > 0 ? `
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Key Words</h6>
                            <div class="keywords">
                                ${data.keywords.map(keyword => `<span class="badge bg-primary me-1">${keyword}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
                ` : ''}
            </div>
        `;
        container.innerHTML = html;
    }
};

// Initialize components based on current page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize chat if on chat page
    if (document.getElementById('chat-messages')) {
        Chat.init();
    }
    
    // Initialize text analysis if on text analysis page
    if (document.getElementById('text-input')) {
        TextAnalysis.init();
    }
});

// Export for global access
window.Utils = Utils;
window.Chat = Chat;
window.TextAnalysis = TextAnalysis;