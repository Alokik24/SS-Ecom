
# SS-Ecom – Secure E-commerce API with 2FA and Stripe Payment

A Django REST Framework-based e-commerce backend API with secure authentication, JWT token handling, role-based access (`Admin`, `Vendor`, `Customer`), and Two-Factor Authentication (2FA) using TOTP and QR codes. Includes interactive **Swagger docs** via `drf-yasg`.

---

## Features

-  JWT Authentication (`SimpleJWT`)
-  Two-Factor Authentication (TOTP via QR Code)
-  Role-Based Access Control (Admin / Vendor / Customer)
-  User Registration, Login, Logout, Profile
-  Swagger API Documentation using `drf-yasg`

---

## ⚙ Tech Stack

- **Backend**: Django 4+, Django REST Framework
- **Auth**: JWT (`djangorestframework-simplejwt`), 2FA (`pyotp`)
- **Docs**: Swagger (`drf-yasg`)
- **Database**: SQLite (development)
- **Tools**: Python 3.10+, Virtualenv

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Alokik24/SS-Ecom.git
cd SS-Ecom
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

---

## 🔐 2FA Setup Flow

1. User logs in → if 2FA is enabled but not verified, server prompts for OTP.
2. User visits `/api/generate-2fa/` to receive a **QR code and TOTP secret**.
3. QR code is scanned in Google Authenticator or similar app.
4. OTP is submitted via `/api/verify-2fa/`.
5. On success, full authentication session is established.

---

## 📡 API Endpoints Overview

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/register/` | POST | ❌ | Register a new user |
| `/api/login/` | POST | ❌ | Login with email & password |
| `/api/logout/` | POST | ✅ | Log out and reset 2FA state |
| `/api/profile/` | GET | ✅ | View current user profile |
| `/api/generate-2fa/` | GET | ✅ | Generate 2FA QR code and secret |
| `/api/verify-2fa/` | POST | ✅ | Submit OTP for 2FA verification |
| `/api/docs/` | GET | ❌ | Swagger UI (Auto-generated docs) |

---

## 📘 API Documentation (Swagger)

Swagger UI is auto-generated using [`drf-yasg`](https://github.com/axnsan12/drf-yasg).

> 📍 Visit:  
> 👉 [`http://localhost:8000/api/docs/`](http://localhost:8000/api/docs/)  
> 👉 [`http://localhost:8000/api/redoc/`](http://localhost:8000/api/redoc/) *(if added)*

---

## ✅ How to Set Up Swagger (`drf-yasg`)

Already included in the repo. But in case you’re setting it up yourself:

### Install `drf-yasg`

```bash
pip install drf-yasg
```

### In `urls.py`:

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SS-Ecom API",
      default_version='v1',
      description="API documentation for the SS-Ecom Django backend",
      contact=openapi.Contact(email="your-email@example.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # optional
]
```

---

## 🧾 License

BSD License © 2025 [Alokik Garg](https://github.com/Alokik24)

---

## 🤝 Contribution

Pull requests are welcome!  
To contribute:
- Fork the repo
- Create a feature branch
- Commit & push
- Open a PR

---

## 📬 Contact

- GitHub: [@Alokik24](https://github.com/Alokik24)
- Email: `alokikgarg24@gmail.com`
