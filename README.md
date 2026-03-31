# Online Marketplace (AELAF MART)

A high-performance, futuristic e-commerce platform built with **Django 6.0**, **Tailwind CSS**, and **PostgreSQL**. AELAF MART provides a premium shopping experience with real-time messaging, secure payments via Stripe, and a sleek, responsive UI.

## Table of Contents

- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Development Workflow](#development-workflow)

## Key Features

### 1. Advanced Authentication & Security (`core` app)

- **8-Digit Email Verification:** Mandatory secure verification flow for all new accounts with timed OTP codes.
- **Social Login:** Integrated **Google OAuth 2.0** via `django-allauth` for seamless onboarding.
- **Custom Adapters:** Intelligent account linking for users with existing emails.

### 2. Comprehensive Shopping Experience (`cart` & `item` apps)

- **Persistent Shopping Cart:** Add/remove items with real-time total calculation.
- **Item Discovery:** Dynamic filtering by categories with neon-accented hover states.
- **Full Item CRUD:** Sellers can easily manage their listings with a premium dashboard interface.

### 3. Secure Payments & Automation (`cart` app)

- **Stripe Integration:** Production-ready checkout session flow for secure transaction processing.
- **Post-Purchase Automation:**
  - Real-time **Order Notifications** sent to both buyer and seller.
  - Automatic marking of items as **SOLD** to remove them from public feeds.
  - Systematic cart clearing upon successful payment.

### 4. Interactive Messaging System (`conversation` app)

- **Direct Seller-Buyer Communication:** Initiate chats directly from item detail pages.
- **Automated Order Alerts:** System-generated messages for purchase confirmations and shipment preparation.

### 5. Premium UI/UX & Responsive Design

- **Futuristic Aesthetics:** Glassmorphism, deep-slate backgrounds, and vibrant blue accents.
- **Image Cropping:** Integrated **Cropper.js** for high-quality, perfectly-resized profile pictures.
- **Fully Responsive:** Optimized for everything from mobile phones to high-resolution desktop monitors.

## Technical Architecture

### Core Data Models

- **Item:** Name, description, price, category, status (is_sold), and media.
- **Cart & CartItem:** Relational mapping for persistent user shopping states.
- **Order:** Tracks Stripe payment intents, total amounts, and paid status.
- **EmailVerification:** Handles 8-digit OTP generation and expiry (5 min).
- **Profile:** Extends user data with bio, phone, and cropped avatars.
- **Conversation & Message:** Thread-based messaging between marketplace members.

## Tech Stack

- **Backend:** Django 6.0.2 & Python 3.10+
- **Database:** PostgreSQL (Production) / SQLite (Dev)
- **Cache/Broker:** Redis (Session & Background processing ready)
- **Payments:** Stripe API
- **Styling:** Tailwind CSS (Modern Glassmorphic UI)
- **Image handling:** Pillow & Cropper.js
- **Containerization:** Docker & Docker Compose
- **Auth:** django-allauth

## Getting Started

### Method 1: Docker (Recommended)

The fastest way to get up and running with all dependencies (PostgreSQL, Redis) is using Docker Compose.

1. **Build and Start:**
   ```bash
   docker-compose up --build
   ```
2. **Setup Admin:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Method 2: Local Setup

1. **Clone & Setup Venv:**
   ```bash
   git clone <repository-url>
   cd Online_Market_Place
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Setup:** (See [Environment Variables](#environment-variables))
4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start Dev Server:**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY="your-secret-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional for Docker)
DATABASE_URL=postgres://postgres:postgres@db:5432/marketplace

# Social Auth
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

# Stripe Payments
STRIPE_PUBLIC_KEY="pk_test_..."
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
```

## Development Workflow

- **Styling:** Tailwind is used for all UI components. Visual changes should follow the established Glassmorphism design pattern.
- **Email:** In development, emails are sent to the console (`EmailBackend`). Check your terminal for verification codes.
- **Migrations:** Always run `python manage.py makemigrations` and `migrate` after updating models.
