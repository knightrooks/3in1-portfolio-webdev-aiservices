"""
Payment Service Module
Handles Stripe and PayPal payment processing, subscription management, and billing
"""

import stripe
import paypalrestsdk
from decimal import Decimal
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from .db import db, User, Payment, UserRole
import logging
import json
import requests

logger = logging.getLogger(__name__)

class PaymentError(Exception):
    """Custom payment processing error"""
    pass

class PaymentService:
    """Payment service class for handling transactions"""
    
    def __init__(self):
        self.stripe_configured = False
        self.paypal_configured = False
        self._configure_stripe()
        self._configure_paypal()
    
    def _configure_stripe(self):
        """Configure Stripe payment processor"""
        try:
            stripe_secret = current_app.config.get('STRIPE_SECRET_KEY')
            if stripe_secret:
                stripe.api_key = stripe_secret
                self.stripe_configured = True
                logger.info("Stripe payment processor configured")
            else:
                logger.warning("Stripe not configured - missing STRIPE_SECRET_KEY")
        except Exception as e:
            logger.error(f"Stripe configuration failed: {str(e)}")
    
    def _configure_paypal(self):
        """Configure PayPal payment processor"""
        try:
            paypal_client_id = current_app.config.get('PAYPAL_CLIENT_ID')
            paypal_client_secret = current_app.config.get('PAYPAL_CLIENT_SECRET')
            paypal_mode = current_app.config.get('PAYPAL_MODE', 'sandbox')
            
            if paypal_client_id and paypal_client_secret:
                paypalrestsdk.configure({
                    "mode": paypal_mode,
                    "client_id": paypal_client_id,
                    "client_secret": paypal_client_secret
                })
                self.paypal_configured = True
                logger.info(f"PayPal payment processor configured ({paypal_mode} mode)")
            else:
                logger.warning("PayPal not configured - missing credentials")
        except Exception as e:
            logger.error(f"PayPal configuration failed: {str(e)}")
    
    def get_pricing_plans(self):
        """Get available pricing plans"""
        return {
            "free": {
                "name": "Free",
                "price": 0,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "10 AI messages per day",
                    "Basic web development consultation",
                    "Portfolio showcase",
                    "Community support"
                ],
                "limits": {
                    "daily_messages": 10,
                    "ai_agents": ["coderbot"],
                    "web_consultations": 1
                }
            },
            "pro": {
                "name": "Pro",
                "price": 29.99,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "Unlimited AI messages",
                    "Access to all AI agents",
                    "Priority web development services",
                    "Custom AI training",
                    "Email support",
                    "API access"
                ],
                "limits": {
                    "daily_messages": -1,  # unlimited
                    "ai_agents": "all",
                    "web_consultations": 5,
                    "api_calls": 1000
                },
                "stripe_price_id": current_app.config.get('STRIPE_PRO_PRICE_ID'),
                "paypal_plan_id": current_app.config.get('PAYPAL_PRO_PLAN_ID')
            },
            "enterprise": {
                "name": "Enterprise",
                "price": 99.99,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "Everything in Pro",
                    "Dedicated AI agents",
                    "White-label solutions",
                    "Advanced analytics",
                    "24/7 phone support",
                    "Custom integrations",
                    "SLA guarantee"
                ],
                "limits": {
                    "daily_messages": -1,
                    "ai_agents": "all",
                    "web_consultations": -1,
                    "api_calls": 10000,
                    "custom_models": 3
                },
                "stripe_price_id": current_app.config.get('STRIPE_ENTERPRISE_PRICE_ID'),
                "paypal_plan_id": current_app.config.get('PAYPAL_ENTERPRISE_PLAN_ID')
            }
        }
    
    def create_stripe_payment_intent(self, user_id, plan, billing_period="monthly"):
        """Create Stripe payment intent for subscription"""
        try:
            if not self.stripe_configured:
                raise PaymentError("Stripe not configured")
            
            plans = self.get_pricing_plans()
            if plan not in plans:
                raise PaymentError(f"Invalid plan: {plan}")
            
            plan_info = plans[plan]
            amount = int(plan_info["price"] * 100)  # Stripe uses cents
            
            # Adjust amount for yearly billing (10% discount)
            if billing_period == "yearly":
                amount = int(amount * 12 * 0.9)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=plan_info["currency"].lower(),
                metadata={
                    "user_id": user_id,
                    "plan": plan,
                    "billing_period": billing_period,
                    "product_type": "ai_subscription"
                },
                automatic_payment_methods={
                    "enabled": True,
                },
            )
            
            # Create payment record
            payment = Payment(
                user_id=user_id,
                stripe_payment_id=intent.id,
                amount=Decimal(str(plan_info["price"])),
                currency=plan_info["currency"],
                product_type="ai_subscription",
                product_name=f"{plan_info['name']} Plan",
                billing_period=billing_period,
                status="pending",
                payment_method="stripe"
            )
            db.session.add(payment)
            db.session.commit()
            
            logger.info(f"Stripe payment intent created: {intent.id} for user {user_id}")
            
            return {
                "payment_id": payment.id,
                "client_secret": intent.client_secret,
                "amount": amount / 100,
                "currency": plan_info["currency"]
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise PaymentError(f"Payment processing error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Payment intent creation failed: {str(e)}")
            raise PaymentError(f"Payment setup failed: {str(e)}")
    
    def create_paypal_payment(self, user_id, plan, billing_period="monthly"):
        """Create PayPal payment for subscription"""
        try:
            if not self.paypal_configured:
                raise PaymentError("PayPal not configured")
            
            plans = self.get_pricing_plans()
            if plan not in plans:
                raise PaymentError(f"Invalid plan: {plan}")
            
            plan_info = plans[plan]
            amount = plan_info["price"]
            
            # Adjust amount for yearly billing
            if billing_period == "yearly":
                amount = amount * 12 * 0.9
            
            # Create PayPal payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/payment/paypal/success",
                    "cancel_url": f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/payment/paypal/cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": f"{plan_info['name']} Plan ({billing_period})",
                            "sku": f"{plan}_{billing_period}",
                            "price": str(amount),
                            "currency": plan_info["currency"],
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": plan_info["currency"]
                    },
                    "description": f"AI Portfolio Platform - {plan_info['name']} subscription"
                }]
            })
            
            if payment.create():
                # Create payment record
                payment_record = Payment(
                    user_id=user_id,
                    paypal_payment_id=payment.id,
                    amount=Decimal(str(amount)),
                    currency=plan_info["currency"],
                    product_type="ai_subscription",
                    product_name=f"{plan_info['name']} Plan",
                    billing_period=billing_period,
                    status="pending",
                    payment_method="paypal"
                )
                db.session.add(payment_record)
                db.session.commit()
                
                # Get approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                logger.info(f"PayPal payment created: {payment.id} for user {user_id}")
                
                return {
                    "payment_id": payment_record.id,
                    "paypal_payment_id": payment.id,
                    "approval_url": approval_url,
                    "amount": amount,
                    "currency": plan_info["currency"]
                }
            else:
                logger.error(f"PayPal payment creation failed: {payment.error}")
                raise PaymentError("PayPal payment creation failed")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"PayPal payment creation failed: {str(e)}")
            raise PaymentError(f"Payment setup failed: {str(e)}")
    
    def confirm_stripe_payment(self, payment_intent_id):
        """Confirm and process successful Stripe payment"""
        try:
            # Retrieve payment intent from Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status != "succeeded":
                raise PaymentError("Payment not completed")
            
            # Get payment record
            payment = Payment.query.filter_by(stripe_payment_id=payment_intent_id).first()
            if not payment:
                raise PaymentError("Payment record not found")
            
            # Update payment status
            payment.status = "completed"
            payment.completed_at = datetime.utcnow()
            
            # Update user subscription
            user = User.query.get(payment.user_id)
            if user:
                self._activate_subscription(user, payment)
            
            db.session.commit()
            
            logger.info(f"Stripe payment confirmed: {payment_intent_id}")
            return payment
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe confirmation error: {str(e)}")
            raise PaymentError(f"Payment confirmation failed: {str(e)}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Payment confirmation failed: {str(e)}")
            raise PaymentError(f"Payment processing failed: {str(e)}")
    
    def confirm_paypal_payment(self, payment_id, payer_id):
        """Confirm and execute PayPal payment"""
        try:
            # Get PayPal payment
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                # Get payment record
                payment_record = Payment.query.filter_by(paypal_payment_id=payment_id).first()
                if not payment_record:
                    raise PaymentError("Payment record not found")
                
                # Update payment status
                payment_record.status = "completed"
                payment_record.completed_at = datetime.utcnow()
                
                # Update user subscription
                user = User.query.get(payment_record.user_id)
                if user:
                    self._activate_subscription(user, payment_record)
                
                db.session.commit()
                
                logger.info(f"PayPal payment confirmed: {payment_id}")
                return payment_record
            else:
                logger.error(f"PayPal payment execution failed: {payment.error}")
                raise PaymentError("PayPal payment execution failed")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"PayPal payment confirmation failed: {str(e)}")
            raise PaymentError(f"Payment processing failed: {str(e)}")
    
    def _activate_subscription(self, user, payment):
        """Activate user subscription based on payment"""
        try:
            # Determine subscription level
            product_name = payment.product_name.lower()
            
            if "pro" in product_name:
                user.role = UserRole.PRO
            elif "enterprise" in product_name:
                user.role = UserRole.ENTERPRISE
            else:
                logger.warning(f"Unknown subscription type: {product_name}")
                return
            
            # Set subscription expiry
            if payment.billing_period == "yearly":
                expiry_date = datetime.utcnow() + timedelta(days=365)
            else:  # monthly
                expiry_date = datetime.utcnow() + timedelta(days=30)
            
            user.subscription_expires = expiry_date
            
            # Reset daily message count for immediate access
            user.daily_message_count = 0
            user.last_message_date = datetime.utcnow().date()
            
            logger.info(f"Subscription activated for user {user.id}: {user.role.value} until {expiry_date}")
            
        except Exception as e:
            logger.error(f"Subscription activation failed: {str(e)}")
            raise PaymentError(f"Subscription activation failed: {str(e)}")
    
    def create_webdev_invoice(self, user_id, project_details):
        """Create invoice for web development services"""
        try:
            # Calculate pricing based on project requirements
            base_price = self._calculate_webdev_pricing(project_details)
            
            # Create payment record
            payment = Payment(
                user_id=user_id,
                amount=base_price,
                currency="USD",
                product_type="webdev_service",
                product_name=f"Web Development - {project_details.get('project_type', 'Custom')}",
                billing_period="one_time",
                status="pending"
            )
            db.session.add(payment)
            db.session.commit()
            
            return {
                "payment_id": payment.id,
                "amount": float(base_price),
                "currency": "USD",
                "description": payment.product_name,
                "invoice_details": self._generate_invoice_details(project_details, base_price)
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Web dev invoice creation failed: {str(e)}")
            raise PaymentError(f"Invoice creation failed: {str(e)}")
    
    def _calculate_webdev_pricing(self, project_details):
        """Calculate web development project pricing"""
        try:
            base_prices = {
                "basic_website": 500,
                "business_website": 1200,
                "ecommerce": 2500,
                "web_application": 3500,
                "mobile_app": 5000,
                "custom": 1000
            }
            
            project_type = project_details.get('project_type', 'custom')
            base_price = base_prices.get(project_type, base_prices['custom'])
            
            # Add complexity multipliers
            features = project_details.get('features', [])
            complexity_multiplier = 1.0
            
            complex_features = ['user_authentication', 'payment_processing', 'api_integration', 'real_time_features']
            for feature in features:
                if feature in complex_features:
                    complexity_multiplier += 0.3
            
            # Timeline urgency multiplier
            timeline = project_details.get('timeline', 'standard')
            if timeline == 'rush':
                complexity_multiplier += 0.5
            elif timeline == 'extended':
                complexity_multiplier -= 0.1
            
            final_price = Decimal(str(base_price * complexity_multiplier))
            return final_price.quantize(Decimal('0.01'))
            
        except Exception as e:
            logger.error(f"Pricing calculation failed: {str(e)}")
            return Decimal('1000.00')  # Default price
    
    def _generate_invoice_details(self, project_details, amount):
        """Generate detailed invoice breakdown"""
        return {
            "project_type": project_details.get('project_type', 'Custom Project'),
            "features": project_details.get('features', []),
            "timeline": project_details.get('timeline', 'Standard'),
            "pages_estimate": project_details.get('pages', 'TBD'),
            "base_amount": float(amount),
            "breakdown": {
                "development": float(amount * Decimal('0.7')),
                "design": float(amount * Decimal('0.2')),
                "testing": float(amount * Decimal('0.1'))
            },
            "terms": "50% deposit required, remainder due upon completion",
            "estimated_delivery": "2-4 weeks from project approval"
        }
    
    def handle_stripe_webhook(self, payload, sig_header):
        """Handle Stripe webhook events"""
        try:
            endpoint_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
            if not endpoint_secret:
                logger.warning("Stripe webhook secret not configured")
                return False
            
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            
            # Handle different event types
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                self.confirm_stripe_payment(payment_intent['id'])
            
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                self._handle_failed_payment(payment_intent['id'], 'stripe')
            
            elif event['type'] == 'invoice.payment_succeeded':
                # Handle subscription renewal
                invoice = event['data']['object']
                self._handle_subscription_renewal(invoice)
            
            logger.info(f"Stripe webhook handled: {event['type']}")
            return True
            
        except ValueError as e:
            logger.error(f"Invalid Stripe webhook payload: {str(e)}")
            return False
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid Stripe webhook signature: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Stripe webhook error: {str(e)}")
            return False
    
    def _handle_failed_payment(self, payment_id, provider):
        """Handle failed payment"""
        try:
            if provider == 'stripe':
                payment = Payment.query.filter_by(stripe_payment_id=payment_id).first()
            else:  # paypal
                payment = Payment.query.filter_by(paypal_payment_id=payment_id).first()
            
            if payment:
                payment.status = "failed"
                db.session.commit()
                
                # Notify user of failed payment
                # Could send email notification here
                
                logger.info(f"Payment marked as failed: {payment_id}")
                
        except Exception as e:
            logger.error(f"Failed payment handling error: {str(e)}")
    
    def _handle_subscription_renewal(self, invoice):
        """Handle automatic subscription renewal"""
        try:
            customer_id = invoice.get('customer')
            if not customer_id:
                return
            
            # Find user by Stripe customer ID (would need to store this)
            # For now, log the renewal
            logger.info(f"Subscription renewal processed for customer: {customer_id}")
            
        except Exception as e:
            logger.error(f"Subscription renewal error: {str(e)}")
    
    def get_user_payment_history(self, user_id, limit=20):
        """Get user's payment history"""
        try:
            payments = Payment.query.filter_by(user_id=user_id)\
                                  .order_by(Payment.created_at.desc())\
                                  .limit(limit)\
                                  .all()
            
            return [payment.to_dict() for payment in payments]
            
        except Exception as e:
            logger.error(f"Payment history retrieval failed: {str(e)}")
            return []
    
    def cancel_subscription(self, user_id):
        """Cancel user subscription"""
        try:
            user = User.query.get(user_id)
            if not user:
                raise PaymentError("User not found")
            
            # Revert to free plan
            user.role = UserRole.FREE
            user.subscription_expires = None
            
            db.session.commit()
            
            logger.info(f"Subscription cancelled for user: {user_id}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Subscription cancellation failed: {str(e)}")
            return False

# Global payment service instance
payment_service = PaymentService()