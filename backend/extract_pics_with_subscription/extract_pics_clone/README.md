# Extract.pics Clone - Django Application

A complete clone of the extract.pics website built with Django, featuring both a web interface and REST API with JWT authentication.

## 🚀 Features

### Web Interface
- **Modern UI**: Clean, responsive design matching the original extract.pics
- **Image Extraction**: Extract images from any public website URL
- **User Authentication**: Login/Register system with session management
- **Dashboard**: Personal dashboard showing extraction history and statistics
- **Results Display**: Grid view of extracted images with filtering and sorting
- **Responsive Design**: Works on both desktop and mobile devices

### REST API
- **JWT Authentication**: Secure token-based authentication
- **Image Extraction API**: Programmatic access to image extraction
- **User Management**: Registration and authentication endpoints
- **CORS Support**: Cross-origin requests enabled for frontend integration
- **Django REST Framework**: Full browsable API interface

## 🛠 Technology Stack

- **Backend**: Django 5.2.3
- **API**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (default, easily configurable)
- **Frontend**: Django Templates with Tailwind CSS
- **Image Processing**: Pillow, BeautifulSoup4, Requests

## 📁 Project Structure

```
extract_pics_clone/
├── manage.py
├── extract_pics_clone/
│   ├── settings.py          # Django settings with JWT and CORS config
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── extractor/               # Main web application
│   ├── models.py            # Database models (Extraction, Image)
│   ├── views.py             # Web views (Home, Login, Dashboard, etc.)
│   ├── urls.py              # Web URL patterns
│   ├── utils.py             # Image extraction logic
│   └── templates/           # Django templates
│       └── extractor/
│           ├── base.html    # Base template with navigation
│           ├── home.html    # Landing page
│           ├── login.html   # Login form
│           ├── register.html # Registration form
│           ├── dashboard.html # User dashboard
│           └── results.html # Extraction results
├── api/                     # REST API application
│   ├── views.py             # API views with JWT authentication
│   ├── serializers.py       # API serializers
│   └── urls.py              # API URL patterns
└── users/                   # User management (placeholder)
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- pip

### 1. Clone and Setup
```bash
cd extract_pics_clone
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt beautifulsoup4 requests pillow
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

The application will be available at `http://localhost:8000`

## 🌐 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/register/` - User registration

### Image Extraction
- `POST /api/extract/` - Extract images from URL (requires authentication)
- `GET /api/extractions/` - List user's extractions (requires authentication)
- `GET /api/extractions/{id}/` - Get specific extraction details
- `POST /api/bulk-download/` - Download multiple images as ZIP

### Example API Usage

#### 1. Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

#### 2. Extract Images
```bash
curl -X POST http://localhost:8000/api/extract/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## 🎨 Web Interface

### Pages
1. **Home** (`/`) - Landing page with URL input
2. **Login** (`/login/`) - User authentication
3. **Register** (`/register/`) - User registration
4. **Dashboard** (`/dashboard/`) - User's personal dashboard
5. **Results** (`/results/{id}/`) - Extraction results display

### Features
- **Responsive Design**: Mobile-friendly interface
- **Modern UI**: Clean design with gradient backgrounds
- **Real-time Feedback**: Success/error messages
- **Image Grid**: Sortable and filterable image display
- **Bulk Operations**: Select and download multiple images

## 🔒 Security Features

- **JWT Authentication**: Secure token-based API access
- **CSRF Protection**: Built-in Django CSRF protection
- **Input Validation**: Proper form validation and sanitization
- **Permission Checks**: User-based access control
- **Secure Headers**: CORS and security headers configured

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL recommended)
4. Configure static files serving
5. Set up proper web server (nginx + gunicorn)

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"
export DEBUG=False
export DATABASE_URL="your-database-url"
```

## 📊 Database Models

### Extraction Model
- `url`: Website URL to extract from
- `user`: Associated user (optional for anonymous)
- `status`: Extraction status (pending/completed/failed)
- `timestamp`: Creation timestamp

### Image Model
- `extraction`: Foreign key to Extraction
- `url`: Image URL
- `name`: Image filename
- `size`: File size in bytes
- `width/height`: Image dimensions
- `format`: Image format (jpg, png, etc.)

## 🔧 Customization

### Adding New Features
1. **Models**: Add new fields to `extractor/models.py`
2. **API**: Extend `api/views.py` and `api/serializers.py`
3. **Web**: Add new views to `extractor/views.py`
4. **Templates**: Create new templates in `extractor/templates/`

### Styling
- Templates use Tailwind CSS classes
- Modify `extractor/templates/extractor/base.html` for global changes
- Add custom CSS in static files if needed

## 🐛 Troubleshooting

### Common Issues
1. **Template Errors**: Check template syntax and context variables
2. **API Errors**: Verify JWT token and request format
3. **Database Issues**: Run migrations and check model definitions
4. **CORS Issues**: Verify CORS settings in settings.py

### Debug Mode
Set `DEBUG = True` in settings.py for detailed error messages.

## 📝 License

This project is created as a demonstration and learning tool. Please respect the original extract.pics service and use this clone responsibly.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Note**: This is a complete functional clone of extract.pics with both web interface and API. The application includes user authentication, image extraction, and a modern responsive design matching the original service.

