"""
AI Services Blueprint
Handles AI-powered interactive experiences
"""

from flask import Blueprint, render_template, request, jsonify
import random

ai_services_bp = Blueprint('ai_services', __name__)

@ai_services_bp.route('/')
def index():
    """AI services overview"""
    ai_services_data = [
        {
            'name': 'AI Chatbot',
            'description': 'Interactive chatbot for customer support and engagement',
            'features': ['Natural language processing', 'Context awareness', 'Multi-language support'],
            'demo_url': '/ai/chatbot'
        },
        {
            'name': 'Text Analysis',
            'description': 'Sentiment analysis and text processing tools',
            'features': ['Sentiment analysis', 'Keyword extraction', 'Text summarization'],
            'demo_url': '/ai/text-analysis'
        },
        {
            'name': 'Smart Recommendations',
            'description': 'AI-powered recommendation engine',
            'features': ['Personalized recommendations', 'Content filtering', 'User behavior analysis'],
            'demo_url': '/ai/recommendations'
        },
        {
            'name': 'Data Insights',
            'description': 'Automated data analysis and visualization',
            'features': ['Pattern recognition', 'Predictive analytics', 'Interactive charts'],
            'demo_url': '/ai/insights'
        }
    ]
    return render_template('ai_services/index.html', services=ai_services_data)

@ai_services_bp.route('/chatbot')
def chatbot():
    """AI Chatbot demo"""
    return render_template('ai_services/chatbot.html')

@ai_services_bp.route('/api/chat', methods=['POST'])
def chat_api():
    """Simple chatbot API endpoint"""
    data = request.get_json()
    user_message = data.get('message', '').lower().strip()
    
    # Simple rule-based responses (in a real app, you'd use proper AI/ML)
    responses = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hi there! What can I do for you?',
        'how are you': 'I\'m doing great! Thanks for asking. How about you?',
        'what can you do': 'I can help answer questions, provide information, and have conversations with you!',
        'services': 'I can tell you about our portfolio, web development services, and AI tools!',
        'portfolio': 'Check out our portfolio section to see amazing projects and skills!',
        'web development': 'We offer frontend, backend, and full-stack development services!',
        'ai': 'Our AI services include chatbots, text analysis, and smart recommendations!',
        'pricing': 'We have packages starting from $999. Check our services section for details!',
        'contact': 'You can reach us through the contact form in the portfolio section!',
        'bye': 'Goodbye! Thanks for chatting with me!',
        'default': 'That\'s interesting! Could you tell me more, or ask me about our services?'
    }
    
    # Find matching response
    response_text = responses.get('default')
    for key in responses:
        if key in user_message:
            response_text = responses[key]
            break
    
    return jsonify({'response': response_text})

@ai_services_bp.route('/text-analysis')
def text_analysis():
    """Text analysis demo"""
    return render_template('ai_services/text_analysis.html')

@ai_services_bp.route('/api/analyze-text', methods=['POST'])
def analyze_text_api():
    """Simple text analysis API"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Simple analysis (in a real app, you'd use proper NLP libraries)
    word_count = len(text.split())
    char_count = len(text)
    
    # Simple sentiment analysis based on positive/negative words
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'love', 'like', 'happy', 'positive']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'negative', 'poor', 'disappointing']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = 'Positive'
        confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
    elif negative_count > positive_count:
        sentiment = 'Negative' 
        confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
    else:
        sentiment = 'Neutral'
        confidence = 0.5
    
    # Extract "keywords" (just the longest words for demo)
    words = text.split()
    keywords = sorted([word.strip('.,!?;:') for word in words if len(word) > 4], key=len, reverse=True)[:5]
    
    analysis_result = {
        'word_count': word_count,
        'character_count': char_count,
        'sentiment': sentiment,
        'sentiment_confidence': round(confidence, 2),
        'keywords': keywords
    }
    
    return jsonify(analysis_result)

@ai_services_bp.route('/recommendations')
def recommendations():
    """Smart recommendations demo"""
    return render_template('ai_services/recommendations.html')

@ai_services_bp.route('/api/recommendations', methods=['POST'])
def recommendations_api():
    """Simple recommendations API"""
    data = request.get_json()
    preferences = data.get('preferences', [])
    
    # Sample recommendation data
    all_items = [
        {'id': 1, 'title': 'Modern Web Development Course', 'category': 'education', 'tags': ['web', 'frontend', 'javascript']},
        {'id': 2, 'title': 'Python Flask Tutorial', 'category': 'education', 'tags': ['python', 'backend', 'flask']},
        {'id': 3, 'title': 'AI and Machine Learning Book', 'category': 'education', 'tags': ['ai', 'ml', 'python']},
        {'id': 4, 'title': 'React Development Tools', 'category': 'tools', 'tags': ['react', 'frontend', 'development']},
        {'id': 5, 'title': 'Database Design Patterns', 'category': 'education', 'tags': ['database', 'design', 'backend']},
        {'id': 6, 'title': 'Mobile App Development', 'category': 'education', 'tags': ['mobile', 'app', 'development']},
        {'id': 7, 'title': 'Cloud Computing Basics', 'category': 'education', 'tags': ['cloud', 'aws', 'deployment']},
        {'id': 8, 'title': 'UI/UX Design Principles', 'category': 'design', 'tags': ['design', 'ui', 'ux']}
    ]
    
    # Simple recommendation logic based on tag matching
    recommendations = []
    for item in all_items:
        score = 0
        for pref in preferences:
            if pref.lower() in [tag.lower() for tag in item['tags']]:
                score += 1
        if score > 0:
            recommendations.append({**item, 'relevance_score': score})
    
    # Sort by relevance and add some randomization
    recommendations.sort(key=lambda x: (x['relevance_score'], random.random()), reverse=True)
    
    return jsonify({'recommendations': recommendations[:6]})

@ai_services_bp.route('/insights')
def insights():
    """Data insights demo"""
    return render_template('ai_services/insights.html')

@ai_services_bp.route('/api/insights', methods=['GET'])
def insights_api():
    """Generate sample data insights"""
    # Generate sample data for demo
    import datetime
    
    # Sample website analytics data
    dates = []
    visitors = []
    for i in range(30):
        date = datetime.datetime.now() - datetime.timedelta(days=29-i)
        dates.append(date.strftime('%Y-%m-%d'))
        # Generate realistic visitor numbers with some trend
        base_visitors = 100 + i * 2  # Growing trend
        daily_variation = random.randint(-20, 30)
        visitors.append(max(0, base_visitors + daily_variation))
    
    # Sample service popularity
    services = ['Frontend Development', 'Backend Development', 'Full-Stack', 'AI Services', 'Consulting']
    service_data = [random.randint(10, 50) for _ in services]
    
    insights_data = {
        'traffic_trend': {
            'dates': dates,
            'visitors': visitors,
            'total_visitors': sum(visitors),
            'average_daily': round(sum(visitors) / len(visitors), 1),
            'trend': 'upward' if visitors[-1] > visitors[0] else 'downward'
        },
        'service_popularity': {
            'services': services,
            'requests': service_data,
            'most_popular': services[service_data.index(max(service_data))]
        },
        'key_metrics': {
            'conversion_rate': round(random.uniform(2.5, 8.5), 1),
            'bounce_rate': round(random.uniform(25, 60), 1),
            'avg_session_duration': f"{random.randint(2, 8)}m {random.randint(10, 59)}s"
        }
    }
    
    return jsonify(insights_data)