/**
 * AI Services Payment Processing
 * Handles subscription payments, agent pricing, and payment UI
 */

class PaymentProcessor {
    constructor() {
        this.stripe = null;
        this.paypal = null;
        this.selectedAgent = null;
        this.selectedTier = null;
        this.selectedPaymentMethod = 'stripe';
        
        this.init();
    }
    
    /**
     * Initialize payment processor
     */
    init() {
        this.initializeStripe();
        this.initializePayPal();
        this.setupEventListeners();
        this.loadAgentPricing();
    }
    
    /**
     * Initialize Stripe payment processor
     */
    async initializeStripe() {
        if (typeof Stripe === 'undefined') {
            console.warn('Stripe.js not loaded');
            return;
        }
        
        const stripeKey = document.querySelector('meta[name="stripe-key"]');
        if (stripeKey) {
            this.stripe = Stripe(stripeKey.content);
            console.log('Stripe initialized');
        } else {
            console.warn('Stripe public key not found');
        }
    }
    
    /**
     * Initialize PayPal payment processor
     */
    initializePayPal() {
        if (typeof paypal === 'undefined') {
            console.warn('PayPal SDK not loaded');
            return;
        }
        
        const paypalClientId = document.querySelector('meta[name="paypal-client-id"]');
        if (paypalClientId) {
            this.paypal = paypal;
            console.log('PayPal initialized');
        } else {
            console.warn('PayPal client ID not found');
        }
    }
    
    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Agent selection
        document.addEventListener('click', (e) => {
            if (e.target.matches('.agent-select-btn')) {
                const agentId = e.target.dataset.agentId;
                this.selectAgent(agentId);
            }
            
            if (e.target.matches('.tier-select-btn')) {
                const tier = e.target.dataset.tier;
                this.selectTier(tier);
            }
            
            if (e.target.matches('.payment-method-btn')) {
                const method = e.target.dataset.method;
                this.selectPaymentMethod(method);
            }
            
            if (e.target.matches('.process-payment-btn')) {
                this.processPayment();
            }
        });
        
        // Form submissions
        const subscriptionForm = document.getElementById('subscriptionForm');
        if (subscriptionForm) {
            subscriptionForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.processPayment();
            });
        }
    }
    
    /**
     * Load agent pricing data
     */
    async loadAgentPricing() {
        try {
            const response = await fetch('/ai/api/pricing');
            if (response.ok) {
                this.agentPricing = await response.json();
                this.updatePricingDisplay();
            }
        } catch (error) {
            console.error('Failed to load pricing data:', error);
        }
    }
    
    /**
     * Select an agent for subscription
     */
    selectAgent(agentId) {
        this.selectedAgent = agentId;
        
        // Update UI
        document.querySelectorAll('.agent-card').forEach(card => {
            if (card.dataset.agentId === agentId) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });
        
        // Update pricing display
        this.updatePricingDisplay();
        this.updatePaymentButton();
    }
    
    /**
     * Select subscription tier
     */
    selectTier(tier) {
        this.selectedTier = tier;
        
        // Update UI
        document.querySelectorAll('.tier-card').forEach(card => {
            if (card.dataset.tier === tier) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });
        
        this.updatePricingDisplay();
        this.updatePaymentButton();
    }
    
    /**
     * Select payment method
     */
    selectPaymentMethod(method) {
        this.selectedPaymentMethod = method;
        
        // Update UI
        document.querySelectorAll('.payment-method-btn').forEach(btn => {
            if (btn.dataset.method === method) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Show/hide payment method specific elements
        this.updatePaymentMethodUI();
    }
    
    /**
     * Update pricing display
     */
    updatePricingDisplay() {
        if (!this.selectedAgent || !this.selectedTier || !this.agentPricing) {
            return;
        }
        
        const agentPlans = this.agentPricing[this.selectedAgent];
        if (agentPlans) {
            const plan = agentPlans.find(p => p.tier === this.selectedTier);
            if (plan) {
                this.displayPrice(plan.price, plan.description);
            }
        }
    }
    
    /**
     * Display price in UI
     */
    displayPrice(price, description) {
        const priceDisplay = document.getElementById('priceDisplay');
        const descriptionDisplay = document.getElementById('planDescription');
        
        if (priceDisplay) {
            priceDisplay.textContent = `$${price.toFixed(2)}`;
        }
        
        if (descriptionDisplay) {
            descriptionDisplay.textContent = description;
        }
        
        // Animate price change
        if (priceDisplay) {
            priceDisplay.classList.add('price-updated');
            setTimeout(() => priceDisplay.classList.remove('price-updated'), 300);
        }
    }
    
    /**
     * Update payment button state
     */
    updatePaymentButton() {
        const paymentBtn = document.getElementById('processPaymentBtn');
        if (paymentBtn) {
            const isReady = this.selectedAgent && this.selectedTier;
            paymentBtn.disabled = !isReady;
            
            if (isReady) {
                paymentBtn.textContent = `Subscribe with ${this.selectedPaymentMethod === 'stripe' ? 'Stripe' : 'PayPal'}`;
            } else {
                paymentBtn.textContent = 'Select Agent and Plan';
            }
        }
    }
    
    /**
     * Update payment method specific UI
     */
    updatePaymentMethodUI() {
        const stripeSection = document.getElementById('stripePaymentSection');
        const paypalSection = document.getElementById('paypalPaymentSection');
        
        if (stripeSection && paypalSection) {
            if (this.selectedPaymentMethod === 'stripe') {
                stripeSection.style.display = 'block';
                paypalSection.style.display = 'none';
            } else {
                stripeSection.style.display = 'none';
                paypalSection.style.display = 'block';
            }
        }
    }
    
    /**
     * Process payment based on selected method
     */
    async processPayment() {
        if (!this.selectedAgent || !this.selectedTier) {
            this.showError('Please select an agent and subscription plan');
            return;
        }
        
        this.showLoading(true);
        
        try {
            if (this.selectedPaymentMethod === 'stripe') {
                await this.processStripePayment();
            } else if (this.selectedPaymentMethod === 'paypal') {
                await this.processPayPalPayment();
            }
        } catch (error) {
            console.error('Payment processing failed:', error);
            this.showError('Payment processing failed. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    /**
     * Process Stripe payment
     */
    async processStripePayment() {
        if (!this.stripe) {
            throw new Error('Stripe not initialized');
        }
        
        // Create payment intent
        const response = await fetch('/ai/api/payment/stripe/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                agent_id: this.selectedAgent,
                tier: this.selectedTier,
                user_id: this.getCurrentUserId()
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create payment intent');
        }
        
        const { client_secret, payment_intent_id } = await response.json();
        
        // Confirm payment with Stripe
        const result = await this.stripe.confirmCardPayment(client_secret, {
            payment_method: {
                card: this.getStripeCardElement(),
                billing_details: this.getBillingDetails()
            }
        });
        
        if (result.error) {
            throw new Error(result.error.message);
        }
        
        // Payment succeeded
        this.handleSuccessfulPayment(result.paymentIntent.id, 'stripe');
    }
    
    /**
     * Process PayPal payment
     */
    async processPayPalPayment() {
        // Create PayPal payment
        const response = await fetch('/ai/api/payment/paypal/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                agent_id: this.selectedAgent,
                tier: this.selectedTier,
                user_id: this.getCurrentUserId()
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create PayPal payment');
        }
        
        const { approval_url, payment_id } = await response.json();
        
        // Redirect to PayPal approval
        window.location.href = approval_url;
    }
    
    /**
     * Get Stripe card element
     */
    getStripeCardElement() {
        // This would be set up elsewhere in your Stripe integration
        return window.stripeCardElement || null;
    }
    
    /**
     * Get billing details from form
     */
    getBillingDetails() {
        return {
            name: document.getElementById('billingName')?.value || '',
            email: document.getElementById('billingEmail')?.value || '',
            address: {
                line1: document.getElementById('billingAddress')?.value || '',
                city: document.getElementById('billingCity')?.value || '',
                state: document.getElementById('billingState')?.value || '',
                postal_code: document.getElementById('billingZip')?.value || '',
                country: document.getElementById('billingCountry')?.value || 'US'
            }
        };
    }
    
    /**
     * Get current user ID (would come from session/auth)
     */
    getCurrentUserId() {
        // This would typically come from authentication system
        return document.querySelector('meta[name="user-id"]')?.content || 'anonymous';
    }
    
    /**
     * Handle successful payment
     */
    handleSuccessfulPayment(transactionId, method) {
        // Update UI to show success
        this.showSuccess(`Payment successful! Your ${this.selectedAgent} subscription is now active.`);
        
        // Redirect to subscription dashboard
        setTimeout(() => {
            window.location.href = '/ai/dashboard';
        }, 3000);
        
        // Track successful conversion
        this.trackConversion(transactionId, method);
    }
    
    /**
     * Show loading state
     */
    showLoading(isLoading) {
        const paymentBtn = document.getElementById('processPaymentBtn');
        const loadingSpinner = document.getElementById('paymentLoading');
        
        if (paymentBtn) {
            paymentBtn.disabled = isLoading;
            if (isLoading) {
                paymentBtn.textContent = 'Processing...';
            } else {
                this.updatePaymentButton();
            }
        }
        
        if (loadingSpinner) {
            loadingSpinner.style.display = isLoading ? 'block' : 'none';
        }
    }
    
    /**
     * Show error message
     */
    showError(message) {
        const errorDiv = document.getElementById('paymentError');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            errorDiv.classList.add('fade-in');
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        } else {
            alert(message); // Fallback
        }
    }
    
    /**
     * Show success message
     */
    showSuccess(message) {
        const successDiv = document.getElementById('paymentSuccess');
        if (successDiv) {
            successDiv.textContent = message;
            successDiv.style.display = 'block';
            successDiv.classList.add('fade-in');
        } else {
            alert(message); // Fallback
        }
    }
    
    /**
     * Track conversion for analytics
     */
    trackConversion(transactionId, method) {
        // Send analytics data
        if (typeof gtag !== 'undefined') {
            gtag('event', 'purchase', {
                transaction_id: transactionId,
                value: this.getCurrentPrice(),
                currency: 'USD',
                items: [{
                    item_id: `${this.selectedAgent}_${this.selectedTier}`,
                    item_name: `${this.selectedAgent} Agent Subscription`,
                    category: 'AI Subscription',
                    quantity: 1,
                    price: this.getCurrentPrice()
                }]
            });
        }
        
        // Custom analytics
        fetch('/ai/api/analytics/conversion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                transaction_id: transactionId,
                agent_id: this.selectedAgent,
                tier: this.selectedTier,
                payment_method: method,
                amount: this.getCurrentPrice()
            })
        }).catch(err => console.warn('Analytics tracking failed:', err));
    }
    
    /**
     * Get current selected price
     */
    getCurrentPrice() {
        if (!this.agentPricing || !this.selectedAgent || !this.selectedTier) {
            return 0;
        }
        
        const agentPlans = this.agentPricing[this.selectedAgent];
        if (agentPlans) {
            const plan = agentPlans.find(p => p.tier === this.selectedTier);
            return plan ? plan.price : 0;
        }
        
        return 0;
    }
}

/**
 * Subscription Dashboard Management
 */
class SubscriptionDashboard {
    constructor() {
        this.subscriptions = [];
        this.init();
    }
    
    init() {
        this.loadSubscriptions();
        this.setupEventListeners();
    }
    
    /**
     * Load user subscriptions
     */
    async loadSubscriptions() {
        try {
            const response = await fetch('/ai/api/subscriptions');
            if (response.ok) {
                this.subscriptions = await response.json();
                this.renderSubscriptions();
            }
        } catch (error) {
            console.error('Failed to load subscriptions:', error);
        }
    }
    
    /**
     * Set up dashboard event listeners
     */
    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.cancel-subscription-btn')) {
                const agentId = e.target.dataset.agentId;
                this.cancelSubscription(agentId);
            }
            
            if (e.target.matches('.renew-subscription-btn')) {
                const agentId = e.target.dataset.agentId;
                this.renewSubscription(agentId);
            }
        });
    }
    
    /**
     * Render subscriptions in dashboard
     */
    renderSubscriptions() {
        const container = document.getElementById('subscriptionsContainer');
        if (!container) return;
        
        if (this.subscriptions.length === 0) {
            container.innerHTML = `
                <div class="no-subscriptions">
                    <h3>No Active Subscriptions</h3>
                    <p>Subscribe to an AI agent to get started</p>
                    <a href="/ai/pricing" class="btn btn-primary">Browse Agents</a>
                </div>
            `;
            return;
        }
        
        const subscriptionsHTML = this.subscriptions.map(sub => this.renderSubscriptionCard(sub)).join('');
        container.innerHTML = subscriptionsHTML;
    }
    
    /**
     * Render individual subscription card
     */
    renderSubscriptionCard(subscription) {
        const daysRemaining = subscription.days_remaining;
        const statusClass = subscription.status === 'active' ? 'success' : 
                           subscription.status === 'expired' ? 'danger' : 'warning';
        
        return `
            <div class="subscription-card">
                <div class="subscription-header">
                    <h4>${subscription.agent_id.replace('_', ' ').toUpperCase()}</h4>
                    <span class="status-badge status-${statusClass}">${subscription.status}</span>
                </div>
                <div class="subscription-details">
                    <p><strong>Plan:</strong> ${subscription.tier.toUpperCase()}</p>
                    <p><strong>Expires:</strong> ${new Date(subscription.end_date).toLocaleDateString()}</p>
                    <p><strong>Days Remaining:</strong> ${daysRemaining}</p>
                    <p><strong>Usage:</strong> ${subscription.usage_count} messages</p>
                </div>
                <div class="subscription-actions">
                    ${subscription.status === 'active' ? 
                        `<button class="btn btn-danger cancel-subscription-btn" data-agent-id="${subscription.agent_id}">Cancel</button>` :
                        `<button class="btn btn-primary renew-subscription-btn" data-agent-id="${subscription.agent_id}">Renew</button>`
                    }
                </div>
            </div>
        `;
    }
    
    /**
     * Cancel subscription
     */
    async cancelSubscription(agentId) {
        if (!confirm('Are you sure you want to cancel this subscription?')) {
            return;
        }
        
        try {
            const response = await fetch(`/ai/api/subscription/${agentId}/cancel`, {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                alert(result.message);
                this.loadSubscriptions(); // Reload to update UI
            } else {
                throw new Error('Cancellation failed');
            }
        } catch (error) {
            console.error('Subscription cancellation failed:', error);
            alert('Failed to cancel subscription. Please try again.');
        }
    }
    
    /**
     * Renew subscription
     */
    renewSubscription(agentId) {
        // Redirect to pricing page with agent pre-selected
        window.location.href = `/ai/pricing?agent=${agentId}`;
    }
}

// Initialize payment processor when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('paymentContainer') || document.querySelector('.agent-select-btn')) {
        window.paymentProcessor = new PaymentProcessor();
    }
    
    if (document.getElementById('subscriptionsContainer')) {
        window.subscriptionDashboard = new SubscriptionDashboard();
    }
});

// Export for use in other modules
window.PaymentProcessor = PaymentProcessor;
window.SubscriptionDashboard = SubscriptionDashboard;