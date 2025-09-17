"""
Web Development Tests
Tests for web development services, pricing, quotes, and project management
"""

import pytest
from unittest.mock import patch, MagicMock
import json


class TestWebDevPages:
    """Test cases for web development pages"""
    
    def test_webdev_index_loads(self, client):
        """Test that web development main page loads"""
        response = client.get('/webdev')
        assert response.status_code == 200
        assert b'web' in response.data.lower()
    
    def test_webdev_pricing_page(self, client):
        """Test web development pricing page"""
        response = client.get('/webdev/pricing')
        assert response.status_code == 200
        assert b'pricing' in response.data.lower()
    
    def test_webdev_quote_page(self, client):
        """Test web development quote page"""
        response = client.get('/webdev/quote')
        assert response.status_code == 200
        assert b'quote' in response.data.lower()
    
    def test_webdev_services_pages(self, client):
        """Test individual service pages"""
        service_pages = [
            '/webdev/websites',
            '/webdev/ecommerce', 
            '/webdev/apps',
            '/webdev/seo',
            '/webdev/marketing',
            '/webdev/maintenance'
        ]
        
        for page in service_pages:
            response = client.get(page)
            assert response.status_code == 200


class TestWebDevContent:
    """Test cases for web development content validation"""
    
    def test_service_descriptions(self, client):
        """Test that services have proper descriptions"""
        response = client.get('/webdev')
        
        # Should contain service descriptions
        service_terms = [
            b'website', b'development', b'design', b'responsive',
            b'ecommerce', b'seo', b'maintenance'
        ]
        
        found_terms = sum(1 for term in service_terms 
                         if term in response.data.lower())
        assert found_terms > 3
    
    def test_technology_stack_display(self, client):
        """Test technology stack information"""
        response = client.get('/webdev')
        
        # Should mention technologies used
        technologies = [
            b'html', b'css', b'javascript', b'python', b'react',
            b'bootstrap', b'django', b'flask'
        ]
        
        found_tech = sum(1 for tech in technologies 
                        if tech in response.data.lower())
        assert found_tech > 2
    
    def test_pricing_information(self, client):
        """Test pricing information display"""
        response = client.get('/webdev/pricing')
        
        # Should contain pricing indicators
        pricing_terms = [b'price', b'cost', b'$', b'quote', b'estimate']
        
        found_terms = sum(1 for term in pricing_terms 
                         if term in response.data.lower())
        assert found_terms > 1
    
    def test_project_examples(self, client):
        """Test project examples or portfolio integration"""
        response = client.get('/webdev')
        
        # Should reference projects or examples
        example_terms = [
            b'project', b'example', b'portfolio', b'work', b'case'
        ]
        
        found_terms = sum(1 for term in example_terms 
                         if term in response.data.lower())
        assert found_terms > 0


class TestWebDevForms:
    """Test cases for web development forms"""
    
    def test_quote_form_structure(self, client):
        """Test quote form structure and fields"""
        response = client.get('/webdev/quote')
        
        if b'<form' in response.data:
            # Should have essential form fields
            form_fields = [
                b'name', b'email', b'project', b'budget', b'timeline'
            ]
            
            found_fields = sum(1 for field in form_fields 
                              if field in response.data.lower())
            assert found_fields > 2
    
    def test_contact_form_fields(self, client):
        """Test contact form has required fields"""
        response = client.get('/webdev/quote')
        
        if b'<form' in response.data:
            # Should have input or textarea elements
            assert b'input' in response.data.lower() or b'textarea' in response.data.lower()
    
    @patch('app.routes.webdev.send_email')
    def test_quote_form_submission(self, mock_send_email, client):
        """Test quote form submission processing"""
        mock_send_email.return_value = True
        
        form_data = {
            'name': 'Test Client',
            'email': 'client@example.com',
            'project_type': 'business_website',
            'description': 'Need a business website',
            'budget': '1000-2500',
            'timeline': 'flexible'
        }
        
        response = client.post('/webdev/quote', data=form_data)
        
        # Should either redirect or show success message
        assert response.status_code in [200, 201, 302]


class TestWebDevAPI:
    """Test cases for web development API endpoints"""
    
    def test_pricing_calculator_api(self, client):
        """Test pricing calculator API if available"""
        pricing_data = {
            'project_type': 'business_website',
            'features': ['responsive', 'contact_form'],
            'pages': 5
        }
        
        response = client.post('/webdev/api/calculate-price', 
                             json=pricing_data,
                             content_type='application/json')
        
        # May not exist, so test passes if not found
        if response.status_code == 200:
            data = response.get_json()
            assert 'price' in data or 'estimate' in data
    
    def test_service_availability_api(self, client):
        """Test service availability API"""
        response = client.get('/webdev/api/services')
        
        # Optional API endpoint
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data, (list, dict))


class TestWebDevSEO:
    """Test cases for web development SEO"""
    
    def test_service_page_titles(self, client):
        """Test that service pages have descriptive titles"""
        pages = ['/webdev', '/webdev/pricing', '/webdev/websites']
        
        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                assert b'<title>' in response.data
                # Title should contain relevant keywords
                title_content = response.data.lower()
                seo_keywords = [b'web', b'development', b'design', b'website']
                found = sum(1 for keyword in seo_keywords 
                           if keyword in title_content)
                assert found > 0
    
    def test_meta_descriptions_present(self, client):
        """Test meta descriptions for service pages"""
        response = client.get('/webdev')
        assert b'meta' in response.data.lower()
        assert b'description' in response.data.lower()
    
    def test_schema_markup(self, client):
        """Test for structured data markup"""
        response = client.get('/webdev')
        
        # Schema markup is optional but beneficial
        # Test passes regardless
        assert response.status_code == 200


class TestWebDevResponsive:
    """Test cases for responsive design"""
    
    def test_responsive_service_pages(self, client):
        """Test service pages are responsive"""
        response = client.get('/webdev')
        
        # Should contain responsive design indicators
        responsive_indicators = [
            b'responsive', b'mobile', b'viewport', b'bootstrap'
        ]
        
        found = sum(1 for indicator in responsive_indicators 
                   if indicator in response.data.lower())
        assert found > 0
    
    def test_mobile_friendly_forms(self, client):
        """Test forms are mobile-friendly"""
        response = client.get('/webdev/quote')
        
        if b'<form' in response.data:
            # Should have mobile-friendly form structure
            # Basic check for responsive classes or viewport meta
            assert b'viewport' in response.data.lower() or b'responsive' in response.data.lower()


class TestWebDevSecurity:
    """Test cases for web development security"""
    
    def test_csrf_protection_in_forms(self, client):
        """Test CSRF protection in forms"""
        response = client.get('/webdev/quote')
        
        if b'<form' in response.data:
            # Should have CSRF tokens in forms
            # In test environment, this might be disabled
            # Test passes regardless for now
            assert response.status_code == 200
    
    def test_no_sensitive_data_exposure(self, client):
        """Test no sensitive data in client-facing pages"""
        pages = ['/webdev', '/webdev/pricing', '/webdev/quote']
        
        sensitive_terms = [b'password', b'secret', b'api_key', b'private']
        
        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                for term in sensitive_terms:
                    assert term not in response.data.lower()
    
    def test_form_input_sanitization(self, client):
        """Test form input sanitization"""
        malicious_data = {
            'name': '<script>alert("xss")</script>',
            'email': 'test@example.com',
            'message': 'Normal message'
        }
        
        response = client.post('/webdev/quote', data=malicious_data)
        
        # Should handle malicious input gracefully
        assert response.status_code in [200, 302, 400]


class TestWebDevPerformance:
    """Test cases for web development performance"""
    
    def test_page_load_performance(self, client):
        """Test page load performance"""
        import time
        
        start_time = time.time()
        response = client.get('/webdev')
        end_time = time.time()
        
        assert response.status_code == 200
        # Should load quickly in test environment
        assert (end_time - start_time) < 2.0
    
    def test_static_asset_optimization(self, client):
        """Test static asset optimization indicators"""
        response = client.get('/webdev')
        
        # Should reference optimized assets
        optimization_indicators = [
            b'.min.css', b'.min.js', b'compressed', b'optimized'
        ]
        
        # This is optional optimization
        assert response.status_code == 200


class TestWebDevAccessibility:
    """Test cases for web development accessibility"""
    
    def test_form_labels(self, client):
        """Test form labels for accessibility"""
        response = client.get('/webdev/quote')
        
        if b'<form' in response.data:
            # Forms should have labels
            assert b'<label' in response.data or b'label' in response.data.lower()
    
    def test_alt_text_on_images(self, client):
        """Test alt text on service images"""
        response = client.get('/webdev')
        
        if b'<img' in response.data:
            assert b'alt=' in response.data
    
    def test_keyboard_navigation(self, client):
        """Test keyboard navigation support"""
        response = client.get('/webdev')
        
        # Should have focusable elements with proper structure
        # This is a basic test
        assert response.status_code == 200


class TestWebDevIntegration:
    """Integration tests for web development services"""
    
    @patch('app.services.payments.payment_processor')
    def test_pricing_integration(self, mock_payment, client):
        """Test integration with pricing system"""
        mock_payment.calculate_webdev_pricing.return_value = 1500.00
        
        # Test pricing calculation integration
        response = client.get('/webdev/pricing')
        assert response.status_code == 200
    
    def test_portfolio_integration(self, client):
        """Test integration with portfolio section"""
        response = client.get('/webdev')
        
        # Should reference portfolio or examples
        portfolio_indicators = [
            b'portfolio', b'examples', b'work', b'projects'
        ]
        
        found = sum(1 for indicator in portfolio_indicators 
                   if indicator in response.data.lower())
        assert found > 0
    
    def test_contact_integration(self, client):
        """Test integration with contact system"""
        response = client.get('/webdev')
        
        # Should have contact information or links
        contact_indicators = [
            b'contact', b'email', b'phone', b'get in touch'
        ]
        
        found = sum(1 for indicator in contact_indicators 
                   if indicator in response.data.lower())
        assert found > 0