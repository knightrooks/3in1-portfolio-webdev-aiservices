"""
AI Services Payment System
Handles Stripe and PayPal integration, subscription management, and usage tracking
"""

import os
import json
import stripe
import paypalrestsdk
from datetime import datetime, timedelta
from decimal import Decimal
from flask import current_app, request, jsonify
from werkzeug.exceptions import BadRequest
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)

# Payment Configuration
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')  # 'live' for production

# Initialize payment gateways
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

if PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET:
    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET
    })

class SubscriptionTier(Enum):
    """Subscription pricing tiers"""
    DAILY = ("daily", 1, 1.00, "1 Day Access")
    WEEKLY = ("weekly", 7, 5.00, "1 Week Access")
    MONTHLY = ("monthly", 30, 19.00, "1 Month Access")
    
    def __init__(self, period, days, price, description):
        self.period = period
        self.days = days
        self.price = price
        self.description = description

@dataclass
class AgentSubscription:
    """Agent subscription data model"""
    user_id: str
    agent_id: str
    tier: SubscriptionTier
    start_date: datetime
    end_date: datetime
    payment_method: str
    transaction_id: str
    status: str
    usage_count: int = 0
    max_usage: int = -1  # -1 for unlimited
    
class PaymentProcessor:
    """Main payment processing class"""
    
    def __init__(self):
        self.agent_pricing = self._load_agent_pricing()
        self.subscriptions = {}  # In production, this would be a database
        
    def _load_agent_pricing(self) -> Dict:
        """Load agent-specific pricing configuration"""
        return {
            'strategist': {'base_multiplier': 1.0, 'premium': False},
            'developer': {'base_multiplier': 1.2, 'premium': True},
            'girlfriend': {'base_multiplier': 0.8, 'premium': False},
            'coderbot': {'base_multiplier': 1.1, 'premium': True},
            'data_scientist': {'base_multiplier': 1.3, 'premium': True},
            'marketing_specialist': {'base_multiplier': 1.0, 'premium': False},
            'product_manager': {'base_multiplier': 1.1, 'premium': True},
            'security_expert': {'base_multiplier': 1.4, 'premium': True},
            'research_analyst': {'base_multiplier': 1.2, 'premium': True},
            'content_creator': {'base_multiplier': 0.9, 'premium': False},
            'customer_success': {'base_multiplier': 0.8, 'premium': False},
            'operations_manager': {'base_multiplier': 1.1, 'premium': True},
            'emotionaljenny': {'base_multiplier': 0.7, 'premium': False},
            'gossipqueen': {'base_multiplier': 0.6, 'premium': False},
            'lazyjohn': {'base_multiplier': 0.5, 'premium': False},
            'strictwife': {'base_multiplier': 0.8, 'premium': False}
        }
    
    def calculate_agent_price(self, agent_id: str, tier: SubscriptionTier) -> float:
        """Calculate price for specific agent and tier"""
        agent_config = self.agent_pricing.get(agent_id, {'base_multiplier': 1.0})
        base_price = tier.price
        multiplier = agent_config['base_multiplier']
        
        final_price = base_price * multiplier
        return round(final_price, 2)
    
    def get_available_plans(self, agent_id: str) -> List[Dict]:
        """Get all available subscription plans for an agent"""
        plans = []
        for tier in SubscriptionTier:
            price = self.calculate_agent_price(agent_id, tier)
            plans.append({
                'tier': tier.period,
                'price': price,
                'duration_days': tier.days,
                'description': tier.description,
                'is_premium': self.agent_pricing.get(agent_id, {}).get('premium', False)
            })
        return plans
    
    def create_stripe_payment_intent(self, user_id: str, agent_id: str, tier: str) -> Dict:
        """Create Stripe payment intent for agent subscription"""
        try:
            subscription_tier = SubscriptionTier[tier.upper()]
            amount_cents = int(self.calculate_agent_price(agent_id, subscription_tier) * 100)
            
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                metadata={
                    'user_id': user_id,
                    'agent_id': agent_id,
                    'subscription_tier': tier,
                    'service': 'ai_agent_subscription'
                },
                description=f'{agent_id.title()} Agent - {subscription_tier.description}'
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': amount_cents / 100,
                'currency': 'usd'
            }
            
        except Exception as e:
            logger.error(f"Stripe payment intent creation failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_paypal_payment(self, user_id: str, agent_id: str, tier: str) -> Dict:
        """Create PayPal payment for agent subscription"""
        try:
            subscription_tier = SubscriptionTier[tier.upper()]
            amount = self.calculate_agent_price(agent_id, subscription_tier)
            
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": f"{request.host_url}ai/payment/paypal/success",
                    "cancel_url": f"{request.host_url}ai/payment/paypal/cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": f"{agent_id.title()} Agent Subscription",
                            "sku": f"{agent_id}_{tier}",
                            "price": str(amount),
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": "USD"
                    },
                    "description": f"{agent_id.title()} Agent - {subscription_tier.description}",
                    "custom": json.dumps({
                        'user_id': user_id,
                        'agent_id': agent_id,
                        'subscription_tier': tier
                    })
                }]
            })
            
            if payment.create():
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'approval_url': approval_url,
                    'amount': amount
                }
            else:
                logger.error(f"PayPal payment creation failed: {payment.error}")
                return {'success': False, 'error': payment.error}
                
        except Exception as e:
            logger.error(f"PayPal payment creation failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def process_stripe_webhook(self, payload: str, signature: str) -> Dict:
        """Process Stripe webhook events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, STRIPE_WEBHOOK_SECRET
            )
            
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                return self._handle_successful_payment(
                    payment_intent['metadata'], 
                    'stripe',
                    payment_intent['id']
                )
            
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                return self._handle_failed_payment(
                    payment_intent['metadata'],
                    'stripe',
                    payment_intent['id']
                )
            
            return {'success': True, 'message': 'Webhook processed'}
            
        except Exception as e:
            logger.error(f"Stripe webhook processing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def process_paypal_webhook(self, data: Dict) -> Dict:
        """Process PayPal webhook events"""
        try:
            event_type = data.get('event_type')
            
            if event_type == 'PAYMENT.SALE.COMPLETED':
                sale = data['resource']
                custom_data = json.loads(sale.get('custom', '{}'))
                return self._handle_successful_payment(
                    custom_data,
                    'paypal',
                    sale['id']
                )
            
            elif event_type == 'PAYMENT.SALE.DENIED':
                sale = data['resource']
                custom_data = json.loads(sale.get('custom', '{}'))
                return self._handle_failed_payment(
                    custom_data,
                    'paypal',
                    sale['id']
                )
            
            return {'success': True, 'message': 'Webhook processed'}
            
        except Exception as e:
            logger.error(f"PayPal webhook processing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_successful_payment(self, metadata: Dict, payment_method: str, transaction_id: str) -> Dict:
        """Handle successful payment and create subscription"""
        try:
            user_id = metadata.get('user_id')
            agent_id = metadata.get('agent_id')
            tier = metadata.get('subscription_tier')
            
            subscription_tier = SubscriptionTier[tier.upper()]
            start_date = datetime.now()
            end_date = start_date + timedelta(days=subscription_tier.days)
            
            subscription = AgentSubscription(
                user_id=user_id,
                agent_id=agent_id,
                tier=subscription_tier,
                start_date=start_date,
                end_date=end_date,
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='active'
            )
            
            # Store subscription (in production, save to database)
            subscription_key = f"{user_id}_{agent_id}"
            self.subscriptions[subscription_key] = subscription
            
            # Log successful subscription
            logger.info(f"Subscription created: {user_id} -> {agent_id} ({tier})")
            
            return {
                'success': True,
                'subscription_id': subscription_key,
                'end_date': end_date.isoformat(),
                'message': 'Subscription activated successfully'
            }
            
        except Exception as e:
            logger.error(f"Payment success handling failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_failed_payment(self, metadata: Dict, payment_method: str, transaction_id: str) -> Dict:
        """Handle failed payment"""
        try:
            user_id = metadata.get('user_id')
            agent_id = metadata.get('agent_id')
            
            logger.warning(f"Payment failed: {user_id} -> {agent_id} ({payment_method})")
            
            return {
                'success': True,
                'message': 'Payment failure handled',
                'action': 'notify_user'
            }
            
        except Exception as e:
            logger.error(f"Payment failure handling failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def check_subscription_access(self, user_id: str, agent_id: str) -> Dict:
        """Check if user has active subscription for agent"""
        subscription_key = f"{user_id}_{agent_id}"
        subscription = self.subscriptions.get(subscription_key)
        
        if not subscription:
            return {
                'has_access': False,
                'reason': 'no_subscription',
                'message': 'No active subscription found'
            }
        
        if subscription.status != 'active':
            return {
                'has_access': False,
                'reason': 'inactive_subscription',
                'message': 'Subscription is not active'
            }
        
        if datetime.now() > subscription.end_date:
            subscription.status = 'expired'
            return {
                'has_access': False,
                'reason': 'expired_subscription',
                'message': 'Subscription has expired',
                'expired_date': subscription.end_date.isoformat()
            }
        
        # Check usage limits if applicable
        if subscription.max_usage > 0 and subscription.usage_count >= subscription.max_usage:
            return {
                'has_access': False,
                'reason': 'usage_limit_reached',
                'message': 'Usage limit reached for this subscription'
            }
        
        return {
            'has_access': True,
            'subscription': {
                'tier': subscription.tier.period,
                'end_date': subscription.end_date.isoformat(),
                'usage_count': subscription.usage_count,
                'max_usage': subscription.max_usage,
                'days_remaining': (subscription.end_date - datetime.now()).days
            }
        }
    
    def track_usage(self, user_id: str, agent_id: str, usage_type: str = 'message') -> Dict:
        """Track agent usage for billing purposes"""
        subscription_key = f"{user_id}_{agent_id}"
        subscription = self.subscriptions.get(subscription_key)
        
        if subscription and subscription.status == 'active':
            subscription.usage_count += 1
            
            # Log usage for analytics
            logger.info(f"Usage tracked: {user_id} -> {agent_id} ({usage_type})")
            
            return {
                'success': True,
                'usage_count': subscription.usage_count,
                'remaining_usage': max(0, subscription.max_usage - subscription.usage_count) if subscription.max_usage > 0 else -1
            }
        
        return {'success': False, 'error': 'No active subscription found'}
    
    def get_user_subscriptions(self, user_id: str) -> List[Dict]:
        """Get all subscriptions for a user"""
        user_subscriptions = []
        
        for key, subscription in self.subscriptions.items():
            if subscription.user_id == user_id:
                user_subscriptions.append({
                    'agent_id': subscription.agent_id,
                    'tier': subscription.tier.period,
                    'start_date': subscription.start_date.isoformat(),
                    'end_date': subscription.end_date.isoformat(),
                    'status': subscription.status,
                    'payment_method': subscription.payment_method,
                    'usage_count': subscription.usage_count,
                    'days_remaining': max(0, (subscription.end_date - datetime.now()).days)
                })
        
        return user_subscriptions
    
    def cancel_subscription(self, user_id: str, agent_id: str) -> Dict:
        """Cancel a user's subscription"""
        subscription_key = f"{user_id}_{agent_id}"
        subscription = self.subscriptions.get(subscription_key)
        
        if not subscription:
            return {'success': False, 'error': 'Subscription not found'}
        
        subscription.status = 'cancelled'
        
        logger.info(f"Subscription cancelled: {user_id} -> {agent_id}")
        
        return {
            'success': True,
            'message': 'Subscription cancelled successfully',
            'refund_eligible': (datetime.now() - subscription.start_date).days < 3
        }
    
    def get_payment_analytics(self) -> Dict:
        """Get payment and subscription analytics"""
        total_subscriptions = len(self.subscriptions)
        active_subscriptions = sum(1 for s in self.subscriptions.values() if s.status == 'active')
        total_revenue = sum(self.calculate_agent_price(s.agent_id, s.tier) for s in self.subscriptions.values())
        
        agent_popularity = {}
        payment_method_stats = {}
        tier_stats = {}
        
        for subscription in self.subscriptions.values():
            # Agent popularity
            agent_popularity[subscription.agent_id] = agent_popularity.get(subscription.agent_id, 0) + 1
            
            # Payment method stats
            payment_method_stats[subscription.payment_method] = payment_method_stats.get(subscription.payment_method, 0) + 1
            
            # Tier stats
            tier_stats[subscription.tier.period] = tier_stats.get(subscription.tier.period, 0) + 1
        
        return {
            'total_subscriptions': total_subscriptions,
            'active_subscriptions': active_subscriptions,
            'total_revenue': round(total_revenue, 2),
            'conversion_rate': round((active_subscriptions / max(1, total_subscriptions)) * 100, 2),
            'agent_popularity': agent_popularity,
            'payment_method_stats': payment_method_stats,
            'tier_distribution': tier_stats
        }

# Global payment processor instance
payment_processor = PaymentProcessor()

# Helper functions for Flask routes
def create_subscription_payment(user_id: str, agent_id: str, tier: str, payment_method: str) -> Dict:
    """Create payment for agent subscription"""
    if payment_method.lower() == 'stripe':
        return payment_processor.create_stripe_payment_intent(user_id, agent_id, tier)
    elif payment_method.lower() == 'paypal':
        return payment_processor.create_paypal_payment(user_id, agent_id, tier)
    else:
        return {'success': False, 'error': 'Unsupported payment method'}

def verify_agent_access(user_id: str, agent_id: str) -> bool:
    """Quick access verification for chat system"""
    result = payment_processor.check_subscription_access(user_id, agent_id)
    return result.get('has_access', False)

def log_agent_usage(user_id: str, agent_id: str, usage_type: str = 'message'):
    """Log agent usage for billing"""
    payment_processor.track_usage(user_id, agent_id, usage_type)

def get_user_dashboard_data(user_id: str) -> Dict:
    """Get comprehensive dashboard data for user"""
    subscriptions = payment_processor.get_user_subscriptions(user_id)
    
    return {
        'subscriptions': subscriptions,
        'total_active': sum(1 for s in subscriptions if s['status'] == 'active'),
        'total_spent': sum(payment_processor.calculate_agent_price(s['agent_id'], SubscriptionTier[s['tier'].upper()]) for s in subscriptions),
        'expiring_soon': [s for s in subscriptions if s['days_remaining'] <= 3 and s['status'] == 'active']
    }