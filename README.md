# SS-Ecom (Social Shoppr)

A comprehensive Django REST Framework-based e-commerce backend API with robust authentication, JWT token handling, role-based access control, Stripe-based payments and Two-Factor Authentication (2FA) capabilities.

## Features

- **JWT Authentication** - Secure token-based authentication using `SimpleJWT`
- **Two-Factor Authentication (2FA)** - TOTP implementation with QR code generation
- **Role-Based Access Control** - Support for Admin, Vendor, and Customer roles
- **User Management** - Complete user registration, login, logout, and profile management
- **Interactive API Documentation** - Auto-generated Swagger UI using `drf-yasg`
- **RESTful API Design** - Clean, consistent API endpoints
- **Secure Backend** - Built with Django security best practices
- **Stripe Integration** - Seamless checkout with Stripe, webhook support for payment events

##  Tech Stack

- **Backend**: Django 4+, Django REST Framework
- **Authentication**: JWT (`djangorestframework-simplejwt`), 2FA (`pyotp`)
- **Documentation**: Swagger UI (`drf-yasg`)
- **Database**: SQLite (development) - easily configurable for production databases
- **Python**: 3.10+
- **Payments**: Stripe 

##  Quick Start

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Alokik24/SS-Ecom.git
   cd SS-Ecom
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

##  Two-Factor Authentication (2FA) Flow

SS-Ecom implements a secure 2FA flow using TOTP (Time-based One-Time Password):

1. **User logs in** → If 2FA is enabled but not verified, server prompts for OTP
2. **Generate 2FA secret** → User visits `/api/generate-2fa/` to receive a QR code and TOTP secret
3. **Scan QR code** → QR code is scanned in Google Authenticator or similar TOTP app
4. **Verify OTP** → OTP is submitted via `/api/verify-2fa/`
5. **Authentication complete** → On success, full authentication session is established

## 📋 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/register/` | POST | ❌ | Register a new user |
| `/api/login/` | POST | ❌ | Login with email & password |
| `/api/logout/` | POST | ✅ | Log out and reset 2FA state |
| `/api/profile/` | GET | ✅ | View current user profile |
| `/api/generate-2fa/` | GET | ✅ | Generate 2FA QR code and secret |
| `/api/verify-2fa/` | POST | ✅ | Submit OTP for 2FA verification |
| `/api/docs/` | GET | ❌ | Swagger UI (Auto-generated docs) |

##  API Documentation

Interactive API documentation is available through Swagger UI:

- **Swagger UI**: `http://localhost:8000/swagger`
- **ReDoc** (if enabled): `http://localhost:8000/api/redoc/`

The documentation is auto-generated using `drf-yasg` and provides:
- Complete endpoint documentation
- Request/response schemas
- Authentication requirements
- Interactive testing capabilities

## Basic Project Structure

```
SS-Ecom/
├── manage.py
├── requirements.txt
├── SS_Ecom/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── payments/
│   ├── users/
│   └── ...
└── README.md
```

##  Configuration

### Environment Variables

For production deployment, configure the following environment variables:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com

STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Database Configuration

The project uses SQLite by default for development. For production, configure your preferred database in `settings.py`:

## User Roles

The system supports three distinct user roles:

- **Admin**: Full system access and management capabilities
- **Vendor**: Product and inventory management
- **Customer**: Shopping and order management

## Security Features

- JWT token-based authentication
- TOTP-based Two-Factor Authentication
- Role-based access control
- Secure password hashing
- CORS configuration
- Input validation and sanitization

## Stripe Payments

SS-Ecom supports secure Stripe-based checkout with webhook handling:

- Create checkout sessions linked to authenticated users and orders
- Automatically handle payment events via Stripe webhooks:
  - `checkout.session.completed`
  - `payment_intent.succeeded`
  - `payment_intent.payment_failed`
- Payment status updates are reflected in `PaymentTransaction` and related `Order` models

### Stripe Webhook Setup

1. In your Stripe Dashboard, set the webhook URL to: `http://<your-domain>/api/webhook/`
2. Use the following events:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`

3. Set your Stripe secret keys and webhook secret in `.env` or `settings.py`:

```env
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-webhook-secret
```
Make sure webhook endpoint is accessible publicly in production.

##  Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes and commit**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

##  License

This project is licensed under the BSD License. See the [LICENSE](LICENSE) file for details.

##  Author

**Alokik Garg**
- GitHub: [@Alokik24](https://github.com/Alokik24)
- Email: alokikgarg24@gmail.com

##  Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Alokik24/SS-Ecom/issues) page
2. Create a new issue with detailed information
3. Contact the author via email

##  Deployment

For production deployment, consider:

- Using PostgreSQL or MySQL instead of SQLite
- Configuring proper environment variables
- Setting up proper CORS policies
- Implementing rate limiting
- Using a production WSGI server like Gunicorn
- Setting up proper logging and monitoring

---

⭐ If you find this project helpful, please consider giving it a star!
