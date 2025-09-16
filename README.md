# 3-in-1 Platform: Portfolio, Web Development & AI Services

A modern, lightweight Flask-powered web platform that brings together three distinct yet complementary areas: a personal portfolio, professional web development services, and AI-powered interactive experiences.

## ✨ Features

### 🎯 Three Integrated Platforms

1. **Personal Portfolio**
   - Professional developer showcase
   - Skills and expertise display
   - Project gallery with detailed descriptions
   - Interactive about me section
   - Contact information and social links

2. **Web Development Services**
   - Service offerings and pricing
   - Package deals for different business sizes
   - Client testimonials and reviews
   - Service inquiry and quote system
   - Professional development process showcase

3. **AI-Powered Interactive Experiences**
   - Interactive AI chatbot with context awareness
   - Text analysis tool with sentiment analysis
   - Smart recommendation engine
   - Data insights and analytics dashboard
   - Real-time AI-powered features

### 🛠 Technical Features

- **Modern Flask Architecture**: Clean, modular structure using blueprints
- **Responsive Design**: Bootstrap 5 with custom CSS for all device sizes
- **Interactive UI**: JavaScript-powered dynamic features and animations
- **RESTful API Endpoints**: JSON APIs for AI services and data processing
- **Error Handling**: Custom 404 and 500 error pages
- **Security Best Practices**: Form validation and secure data handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/knightrooks/3in1-portfolio-webdev-aiservices.git
   cd 3in1-portfolio-webdev-aiservices
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** and visit `http://localhost:5000`

## 📁 Project Structure

```
3in1-portfolio-webdev-aiservices/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── blueprints/                    # Flask blueprints
│   ├── __init__.py
│   ├── portfolio.py              # Portfolio module
│   ├── services.py               # Web services module
│   └── ai_services.py            # AI services module
├── templates/                     # HTML templates
│   ├── base.html                 # Base template
│   ├── home.html                 # Homepage
│   ├── about.html                # About page
│   ├── 404.html                  # Error page
│   ├── 500.html                  # Error page
│   ├── portfolio/                # Portfolio templates
│   │   └── index.html
│   ├── services/                 # Services templates
│   │   └── index.html
│   └── ai_services/              # AI services templates
│       ├── index.html
│       ├── chatbot.html
│       └── text_analysis.html
└── static/                       # Static assets
    ├── css/
    │   └── style.css            # Custom styles
    └── js/
        └── main.js              # JavaScript functionality
```

## 🎮 Usage Guide

### Navigation

The platform features a comprehensive navigation system with dropdown menus for each of the three main areas:

- **Portfolio**: Access personal information, projects, skills, and contact details
- **Web Services**: Browse services, packages, testimonials, and request quotes
- **AI Services**: Try interactive AI tools, chatbots, and analysis features

### AI Features

#### Interactive Chatbot
- Navigate to `/ai/chatbot`
- Ask questions about services, portfolio, or general inquiries
- Get instant responses powered by rule-based AI logic

#### Text Analysis Tool
- Navigate to `/ai/text-analysis`
- Enter text for sentiment analysis and keyword extraction
- View comprehensive analysis results with confidence scores

### API Endpoints

The platform provides RESTful API endpoints for AI services:

- `POST /ai/api/chat` - Chatbot conversation endpoint
- `POST /ai/api/analyze-text` - Text analysis endpoint
- `POST /ai/api/recommendations` - Smart recommendations
- `GET /ai/api/insights` - Data insights and analytics

## 🛠 Development

### Adding New Features

1. **Create new routes** in the appropriate blueprint file
2. **Add templates** in the corresponding template directory
3. **Update navigation** in `templates/base.html` if needed
4. **Add styling** in `static/css/style.css`
5. **Add JavaScript** functionality in `static/js/main.js`

### Customization

- **Colors and Styling**: Edit `static/css/style.css`
- **Content**: Update template files in `templates/`
- **AI Responses**: Modify logic in `blueprints/ai_services.py`
- **Services**: Update service data in `blueprints/services.py`
- **Portfolio Info**: Customize portfolio content in `blueprints/portfolio.py`

## 🚀 Deployment

### Production Considerations

1. **Set Environment Variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export FLASK_ENV="production"
   ```

2. **Use a Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Configure Web Server** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static {
           alias /path/to/your/app/static;
       }
   }
   ```

### Cloud Deployment Options

- **Heroku**: Add `Procfile` with `web: gunicorn app:app`
- **AWS EC2**: Use gunicorn with nginx reverse proxy
- **DigitalOcean**: Deploy using their App Platform or Droplets
- **Google Cloud**: Use App Engine or Compute Engine

## 🧪 Testing

Run the application in debug mode for development:

```bash
export FLASK_ENV=development
python app.py
```

The application includes:
- Error handling for common scenarios
- Form validation and sanitization
- Responsive design testing across devices
- API endpoint testing for AI features

## 🎯 Tech Stack

- **Backend**: Python 3.12, Flask 3.0.0
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript ES6+
- **Architecture**: Modular blueprints, RESTful APIs
- **Design**: Responsive, mobile-first approach
- **AI Features**: Rule-based processing with extensible architecture

## 📸 Screenshots

### Homepage
![Homepage](https://github.com/user-attachments/assets/da22778a-201b-4c00-a109-03de368eb619)

### AI Chatbot
![AI Chatbot](https://github.com/user-attachments/assets/4baedf4b-4738-48bb-97bc-c6aac34f487a)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bootstrap team for the excellent CSS framework
- Flask community for the lightweight web framework
- Font Awesome for the comprehensive icon library
- Contributors and users who provide feedback and suggestions

## 📞 Support

For support, questions, or feature requests:

- Open an issue on GitHub
- Use the AI chatbot feature on the platform
- Contact through the portfolio contact form

---

**Built with ❤️ using Flask, Bootstrap, and modern web technologies.**