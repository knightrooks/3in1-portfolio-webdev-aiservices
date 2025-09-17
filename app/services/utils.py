"""
Utilities Service Module
Helper functions for validation, formatting, file handling, and common operations
"""

import re
import json
import uuid
import hashlib
import secrets
import base64
import mimetypes
import os
from datetime import datetime, timedelta
from decimal import Decimal
from urllib.parse import urlparse, urljoin
from flask import request, current_app
from werkzeug.utils import secure_filename
import logging
from typing import Dict, List, Any, Optional, Union
import bleach
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error"""
    pass

class FileError(Exception):
    """Custom file handling error"""
    pass

class UtilityService:
    """Utility service for common helper functions"""
    
    # Validation functions
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format"""
        if not email or len(email) > 320:  # RFC 5321 limit
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.lower()))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check for valid length (10-15 digits)
        if len(digits_only) < 10 or len(digits_only) > 15:
            return False
        
        # Basic pattern for international numbers
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, digits_only))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def validate_credit_card(card_number: str) -> Dict[str, Any]:
        """Validate credit card using Luhn algorithm"""
        if not card_number:
            return {"valid": False, "error": "Card number required"}
        
        # Remove spaces and hyphens
        card_number = re.sub(r'[\s-]', '', card_number)
        
        # Check if all characters are digits
        if not card_number.isdigit():
            return {"valid": False, "error": "Card number must contain only digits"}
        
        # Check length
        if len(card_number) < 13 or len(card_number) > 19:
            return {"valid": False, "error": "Invalid card number length"}
        
        # Luhn algorithm
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        
        is_valid = luhn_checksum(card_number) == 0
        
        # Determine card type
        card_type = UtilityService.get_card_type(card_number)
        
        return {
            "valid": is_valid,
            "card_type": card_type,
            "masked": UtilityService.mask_card_number(card_number)
        }
    
    @staticmethod
    def get_card_type(card_number: str) -> str:
        """Determine credit card type from number"""
        patterns = {
            'Visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
            'Mastercard': r'^5[1-5][0-9]{14}$',
            'American Express': r'^3[47][0-9]{13}$',
            'Discover': r'^6(?:011|5[0-9]{2})[0-9]{12}$',
            'Diners Club': r'^3[0-9]{4,}$',
            'JCB': r'^(?:2131|1800|35\d{3})\d{11}$'
        }
        
        for card_type, pattern in patterns.items():
            if re.match(pattern, card_number):
                return card_type
        
        return 'Unknown'
    
    @staticmethod
    def mask_card_number(card_number: str) -> str:
        """Mask credit card number for display"""
        if len(card_number) <= 4:
            return card_number
        
        return '*' * (len(card_number) - 4) + card_number[-4:]
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength and return detailed feedback"""
        if not password:
            return {"valid": False, "errors": ["Password is required"], "score": 0}
        
        errors = []
        score = 0
        
        # Length check
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif len(password) >= 12:
            score += 2
        else:
            score += 1
        
        # Character variety checks
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        else:
            score += 1
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        else:
            score += 1
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        else:
            score += 1
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        else:
            score += 1
        
        # Common password patterns
        common_patterns = ['password', '123456', 'qwerty', 'abc123', 'letmein']
        if password.lower() in common_patterns:
            errors.append("Password is too common")
            score = max(0, score - 2)
        
        # Sequential or repeated characters
        if re.search(r'(.)\1{2,}', password):  # 3+ repeated chars
            errors.append("Password contains too many repeated characters")
            score = max(0, score - 1)
        
        # Strength levels
        strength_levels = {
            0: 'Very Weak',
            1: 'Weak', 
            2: 'Fair',
            3: 'Good',
            4: 'Strong',
            5: 'Very Strong',
            6: 'Excellent'
        }
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "score": score,
            "strength": strength_levels.get(score, 'Very Weak')
        }
    
    # Formatting functions
    @staticmethod
    def format_currency(amount: Union[int, float, Decimal], currency: str = 'USD') -> str:
        """Format currency amount for display"""
        try:
            amount = float(amount)
            
            currency_symbols = {
                'USD': '$',
                'EUR': '€',
                'GBP': '£',
                'JPY': '¥',
                'CAD': 'C$',
                'AUD': 'A$'
            }
            
            symbol = currency_symbols.get(currency, currency)
            
            if currency == 'JPY':
                # No decimal places for JPY
                return f"{symbol}{amount:,.0f}"
            else:
                return f"{symbol}{amount:,.2f}"
                
        except (ValueError, TypeError):
            return f"{currency} 0.00"
    
    @staticmethod
    def format_phone(phone: str, country_code: str = 'US') -> str:
        """Format phone number for display"""
        if not phone:
            return ""
        
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        if country_code == 'US' and len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif country_code == 'US' and len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            # International format
            return f"+{digits}"
    
    @staticmethod
    def format_date(date: datetime, format_type: str = 'medium') -> str:
        """Format datetime for display"""
        if not date:
            return ""
        
        formats = {
            'short': '%m/%d/%Y',
            'medium': '%B %d, %Y',
            'long': '%A, %B %d, %Y',
            'time': '%I:%M %p',
            'datetime': '%B %d, %Y at %I:%M %p',
            'iso': '%Y-%m-%dT%H:%M:%SZ'
        }
        
        format_str = formats.get(format_type, formats['medium'])
        return date.strftime(format_str)
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size for human reading"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in seconds to human readable format"""
        if seconds < 0:
            return "0 seconds"
        
        time_units = [
            (31536000, 'year'),
            (2592000, 'month'),
            (604800, 'week'),
            (86400, 'day'),
            (3600, 'hour'),
            (60, 'minute'),
            (1, 'second')
        ]
        
        for unit_seconds, unit_name in time_units:
            if seconds >= unit_seconds:
                count = seconds // unit_seconds
                remainder = seconds % unit_seconds
                
                result = f"{count} {unit_name}"
                if count != 1:
                    result += "s"
                
                # Add next smaller unit if significant
                if remainder > 0 and unit_seconds > 1:
                    for next_unit_seconds, next_unit_name in time_units:
                        if next_unit_seconds < unit_seconds and remainder >= next_unit_seconds:
                            next_count = remainder // next_unit_seconds
                            if next_count > 0:
                                next_unit = f"{next_count} {next_unit_name}"
                                if next_count != 1:
                                    next_unit += "s"
                                result += f", {next_unit}"
                            break
                
                return result
        
        return "0 seconds"
    
    # File handling functions
    @staticmethod
    def allowed_file(filename: str, allowed_extensions: Optional[List[str]] = None) -> bool:
        """Check if file extension is allowed"""
        if not filename:
            return False
        
        if allowed_extensions is None:
            allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx']
        
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension from filename"""
        if not filename or '.' not in filename:
            return ""
        
        return filename.rsplit('.', 1)[1].lower()
    
    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """Generate secure filename with timestamp"""
        if not original_filename:
            return f"file_{int(datetime.utcnow().timestamp())}"
        
        # Secure the filename
        secure_name = secure_filename(original_filename)
        
        # Add timestamp to avoid collisions
        name, ext = os.path.splitext(secure_name)
        timestamp = int(datetime.utcnow().timestamp())
        
        return f"{name}_{timestamp}{ext}"
    
    @staticmethod
    def validate_image(file_content: bytes) -> Dict[str, Any]:
        """Validate and get information about image file"""
        try:
            with Image.open(io.BytesIO(file_content)) as img:
                return {
                    "valid": True,
                    "format": img.format,
                    "size": img.size,
                    "mode": img.mode,
                    "file_size": len(file_content)
                }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    @staticmethod
    def resize_image(file_content: bytes, max_width: int = 1920, max_height: int = 1080) -> bytes:
        """Resize image while maintaining aspect ratio"""
        try:
            with Image.open(io.BytesIO(file_content)) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Calculate new dimensions
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Save to bytes
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                return output.getvalue()
                
        except Exception as e:
            logger.error(f"Image resize failed: {str(e)}")
            return file_content  # Return original if resize fails
    
    # Security functions
    @staticmethod
    def generate_random_string(length: int = 32) -> str:
        """Generate cryptographically secure random string"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate UUID4 string"""
        return str(uuid.uuid4())
    
    @staticmethod
    def hash_string(text: str, salt: Optional[str] = None) -> str:
        """Hash string with optional salt using SHA-256"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        hash_obj = hashlib.sha256()
        hash_obj.update((text + salt).encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def verify_hash(text: str, hash_value: str, salt: str) -> bool:
        """Verify hash with salt"""
        return UtilityService.hash_string(text, salt) == hash_value
    
    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """Sanitize HTML content to prevent XSS"""
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'code', 'pre'
        ]
        
        allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            '*': ['class']
        }
        
        return bleach.clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
    
    @staticmethod
    def encode_base64(data: Union[str, bytes]) -> str:
        """Encode data to base64"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def decode_base64(encoded_data: str) -> bytes:
        """Decode base64 data"""
        return base64.b64decode(encoded_data)
    
    # Request/Response utilities
    @staticmethod
    def get_client_ip() -> str:
        """Get client IP address from request"""
        if request.environ.get('HTTP_X_FORWARDED_FOR'):
            # Handle proxy forwarding
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
        elif request.environ.get('HTTP_X_REAL_IP'):
            return request.environ['HTTP_X_REAL_IP']
        else:
            return request.environ.get('REMOTE_ADDR', 'unknown')
    
    @staticmethod
    def get_user_agent() -> str:
        """Get user agent from request"""
        return request.headers.get('User-Agent', 'Unknown')
    
    @staticmethod
    def is_mobile_device() -> bool:
        """Check if request is from mobile device"""
        user_agent = UtilityService.get_user_agent().lower()
        mobile_keywords = [
            'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 
            'windows phone', 'nokia', 'samsung', 'htc', 'lg', 'motorola'
        ]
        
        return any(keyword in user_agent for keyword in mobile_keywords)
    
    @staticmethod
    def get_referrer() -> Optional[str]:
        """Get referrer URL from request"""
        return request.headers.get('Referer')
    
    # Data processing utilities
    @staticmethod
    def paginate_data(data: List[Any], page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Paginate list of data"""
        if page < 1:
            page = 1
        
        total = len(data)
        start = (page - 1) * per_page
        end = start + per_page
        
        items = data[start:end]
        
        return {
            'items': items,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_prev': page > 1,
            'has_next': end < total,
            'prev_num': page - 1 if page > 1 else None,
            'next_num': page + 1 if end < total else None
        }
    
    @staticmethod
    def filter_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
        """Filter dictionary to only include allowed keys"""
        return {key: value for key, value in data.items() if key in allowed_keys}
    
    @staticmethod
    def deep_merge_dict(dict1: Dict, dict2: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = UtilityService.deep_merge_dict(result[key], value)
            else:
                result[key] = value
        
        return result
    
    @staticmethod
    def flatten_dict(data: Dict[str, Any], prefix: str = '', separator: str = '.') -> Dict[str, Any]:
        """Flatten nested dictionary"""
        items = []
        
        for key, value in data.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            
            if isinstance(value, dict):
                items.extend(
                    UtilityService.flatten_dict(value, new_key, separator).items()
                )
            else:
                items.append((new_key, value))
        
        return dict(items)
    
    @staticmethod
    def calculate_percentage(part: Union[int, float], total: Union[int, float]) -> float:
        """Calculate percentage with division by zero protection"""
        if total == 0:
            return 0.0
        
        return round((part / total) * 100, 2)
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
        """Truncate text to specified length"""
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    # Configuration utilities
    @staticmethod
    def get_config_value(key: str, default: Any = None, cast_type: type = str):
        """Get configuration value with type casting"""
        try:
            value = current_app.config.get(key, default)
            
            if value is None:
                return default
            
            if cast_type == bool:
                return str(value).lower() in ('true', '1', 'yes', 'on')
            elif cast_type == int:
                return int(value)
            elif cast_type == float:
                return float(value)
            elif cast_type == list:
                if isinstance(value, str):
                    return [item.strip() for item in value.split(',')]
                return list(value)
            else:
                return cast_type(value)
                
        except (ValueError, TypeError):
            logger.warning(f"Invalid config value for {key}: {value}, using default: {default}")
            return default
    
    @staticmethod
    def is_development() -> bool:
        """Check if running in development mode"""
        return current_app.config.get('ENV', 'production').lower() == 'development'
    
    @staticmethod
    def is_debug() -> bool:
        """Check if debug mode is enabled"""
        return current_app.config.get('DEBUG', False)
    
    # Logging utilities
    @staticmethod
    def log_api_request(endpoint: str, method: str, user_id: Optional[str] = None, 
                       response_time: Optional[float] = None):
        """Log API request for analytics"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'user_id': user_id,
            'ip': UtilityService.get_client_ip(),
            'user_agent': UtilityService.get_user_agent(),
            'response_time': response_time
        }
        
        logger.info(f"API Request: {json.dumps(log_data)}")
    
    @staticmethod
    def create_error_response(message: str, error_code: str = 'GENERIC_ERROR', 
                            status_code: int = 400) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            'error': True,
            'message': message,
            'error_code': error_code,
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': UtilityService.generate_uuid()
        }
    
    @staticmethod
    def create_success_response(data: Any = None, message: str = 'Success') -> Dict[str, Any]:
        """Create standardized success response"""
        response = {
            'success': True,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if data is not None:
            response['data'] = data
        
        return response

# Create global utility instance
utils = UtilityService()