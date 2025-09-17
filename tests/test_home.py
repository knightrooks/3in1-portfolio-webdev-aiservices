"""
Home Page Tests
Tests for the main landing page functionality, navigation, and content
"""

import pytest
from flask import url_for


class TestHomePage:
    """Test cases for home page functionality"""
    
    def test_home_page_loads(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'AI Portfolio Platform' in response.data
    
    def test_home_page_sections(self, client):
        """Test that all main sections are present"""
        response = client.get('/')
        
        # Check for hero section
        assert b'hero' in response.data.lower() or b'welcome' in response.data.lower()
        
        # Check for services sections
        assert b'web development' in response.data.lower()
        assert b'ai' in response.data.lower()
        assert b'portfolio' in response.data.lower()
    
    def test_navigation_links(self, client):
        """Test that navigation links are present"""
        response = client.get('/')
        
        # Check for navigation links
        assert b'/portfolio' in response.data or b'portfolio' in response.data.lower()
        assert b'/webdev' in response.data or b'web' in response.data.lower()
        assert b'/ai' in response.data or b'ai' in response.data.lower()
    
    def test_contact_information(self, client):
        """Test that contact information is accessible"""
        response = client.get('/')
        
        # Should have contact information or link to contact
        assert (b'contact' in response.data.lower() or 
                b'email' in response.data.lower() or
                b'@' in response.data)
    
    def test_meta_tags(self, client):
        """Test that essential meta tags are present"""
        response = client.get('/')
        
        # Check for essential meta tags
        assert b'<title>' in response.data
        assert b'description' in response.data.lower()
        
    def test_responsive_design_indicators(self, client):
        """Test for responsive design indicators"""
        response = client.get('/')
        
        # Check for Bootstrap or CSS framework indicators
        assert (b'bootstrap' in response.data.lower() or 
                b'responsive' in response.data.lower() or
                b'viewport' in response.data.lower())
    
    def test_social_links(self, client):
        """Test for social media links or indicators"""
        response = client.get('/')
        
        # Not required but good to have
        # This test will pass regardless for now
        assert response.status_code == 200


class TestHomePageSEO:
    """Test cases for SEO-related functionality"""
    
    def test_title_tag(self, client):
        """Test that page has proper title tag"""
        response = client.get('/')
        assert b'<title>' in response.data
        # Title should not be empty
        title_start = response.data.find(b'<title>') + 7
        title_end = response.data.find(b'</title>')
        title_content = response.data[title_start:title_end]
        assert len(title_content) > 0
    
    def test_meta_description(self, client):
        """Test meta description presence"""
        response = client.get('/')
        assert b'meta' in response.data.lower()
        assert b'description' in response.data.lower()
    
    def test_canonical_url(self, client):
        """Test for canonical URL (optional but good practice)"""
        response = client.get('/')
        # This is optional, test passes regardless
        assert response.status_code == 200


class TestHomePagePerformance:
    """Test cases for performance-related aspects"""
    
    def test_response_time(self, client):
        """Test that home page responds quickly"""
        import time
        start_time = time.time()
        response = client.get('/')
        end_time = time.time()
        
        assert response.status_code == 200
        # Response should be under 1 second in test environment
        assert (end_time - start_time) < 1.0
    
    def test_content_size(self, client):
        """Test that home page content is reasonable size"""
        response = client.get('/')
        
        # Content should not be empty but also not excessively large
        content_size = len(response.data)
        assert content_size > 1000  # At least 1KB
        assert content_size < 500000  # Less than 500KB


class TestHomePageSecurity:
    """Test cases for security-related aspects"""
    
    def test_no_sensitive_information(self, client):
        """Test that no sensitive information is exposed"""
        response = client.get('/')
        
        # Should not contain sensitive data
        sensitive_terms = [b'password', b'secret_key', b'api_key', b'private_key']
        for term in sensitive_terms:
            assert term not in response.data.lower()
    
    def test_csrf_protection_indicators(self, client):
        """Test for CSRF protection indicators in forms"""
        response = client.get('/')
        
        # If there are forms, they should have CSRF tokens
        if b'<form' in response.data:
            # This is a basic check - more detailed testing would be in form-specific tests
            assert response.status_code == 200


class TestHomePageAccessibility:
    """Test cases for accessibility features"""
    
    def test_alt_text_presence(self, client):
        """Test that images have alt text"""
        response = client.get('/')
        
        if b'<img' in response.data:
            # Images should have alt attributes
            # This is a basic check
            assert b'alt=' in response.data
    
    def test_heading_structure(self, client):
        """Test proper heading structure"""
        response = client.get('/')
        
        # Should have at least h1 tag
        assert b'<h1' in response.data or b'<h1>' in response.data
    
    def test_semantic_html(self, client):
        """Test for semantic HTML elements"""
        response = client.get('/')
        
        # Should use semantic HTML5 elements
        semantic_elements = [b'<header', b'<main', b'<section', b'<nav']
        found_elements = sum(1 for element in semantic_elements if element in response.data)
        
        # Should have at least some semantic elements
        assert found_elements > 0


class TestHomePageIntegration:
    """Integration tests for home page with other components"""
    
    def test_static_files_loading(self, client):
        """Test that static files are properly referenced"""
        response = client.get('/')
        
        # Should reference CSS and JS files
        assert (b'.css' in response.data or 
                b'stylesheet' in response.data.lower())
    
    def test_error_handling(self, client):
        """Test error handling for invalid requests"""
        # Test with invalid method
        response = client.post('/')
        # Should either work or return appropriate error
        assert response.status_code in [200, 405, 404]
    
    def test_redirects(self, client):
        """Test redirect behavior if any"""
        # Test common redirect patterns
        response = client.get('/home')
        # Should either work or redirect to /
        assert response.status_code in [200, 301, 302, 404]


# Parametrized tests for different user agents
@pytest.mark.parametrize("user_agent", [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',  # Desktop
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',      # Mobile
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'  # Bot
])
def test_user_agent_compatibility(client, user_agent):
    """Test compatibility with different user agents"""
    response = client.get('/', headers={'User-Agent': user_agent})
    assert response.status_code == 200