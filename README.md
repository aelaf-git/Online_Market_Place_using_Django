# AI-Powered Online Marketplace (AELAF MART)

A high-performance, futuristic e-commerce platform built with **Django 6.0**, **Tailwind CSS**, and **PostgreSQL (Neon)**. AELAF MART features an advanced **AI Shopping Assistant** powered by **LangChain** and **Groq (Llama 3.3)**, providing real-time inventory-aware recommendations and persistent conversation memory.

## Table of Contents

- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Development Workflow](#development-workflow)

## Key Features

### 1. AI-Powered Shopping Assistant (`chatbot` app)

- **RAG-Powered Conversations**: The assistant (Llama-3.3-70b) has real-time access to the store's inventory to help users find exactly what they need.
- **Persistent Memory**: Uses `PostgresChatMessageHistory` via LangChain to remember user preferences and past interactions across sessions.
- **Sleek Widget**: A futuristic, floating chat interface with real-time typing indicators.

### 2. Advanced Authentication & Security (`core` app)

- **8-Digit Email Verification**: Mandatory secure verification flow for all new accounts with timed OTP codes.
- **Social Login**: Integrated **Google OAuth 2.0** via `django-allauth` for seamless onboarding.
- **Custom Adapters**: Intelligent account linking for users with existing emails.

### 3. Comprehensive Shopping Experience (`cart` & `item` apps)

- **Persistent Shopping Cart**: Add/remove items with real-time total calculation.
- **Item Discovery**: Dynamic filtering by categories with neon-accented hover states.
- **Full Item CRUD**: Sellers can easily manage their listings with a premium dashboard interface.

### 4. Secure Payments & Automation (`cart` app)

- **Stripe Integration**: Production-ready checkout session flow for secure transaction processing.
- **Post-Purchase Automation**: Mark items as **SOLD** automatically and notify both parties.

## Technical Architecture

The platform follows a modular Django architecture integrated with a cloud-native database and an AI reasoning layer.

```mermaid
graph TD
    User((User)) -->|HTTPS| Django[Django 6.0 App]
    Django -->|ORM| Postgres[(Postgres - Neon)]
    Django -->|Context| LangChain[LangChain Engine]
    LangChain -->|Llama-3.3 API| Groq[Groq Cloud AI]
    LangChain -->|History| Postgres
    Django -->|Stripe API| Stripe((Stripe Payments))
    Django -->|OAuth| Google((Google Auth))
```

### Core Data Models

- **Item**: Name, description, price, category, status (is_sold), and media.
- **Profile**: Extends user data with bio, phone, and cropped avatars.
- **PostgresChatMessageHistory**: Stores AI conversation logs in a dedicated Postgres table.
- **Order**: Tracks Stripe payment intents and transaction status.

## Tech Stack

- **Backend**: Django 6.0.2 & Python 3.10+
- **AI Engine**: LangChain & Groq (Llama-3.3-70b-versatile)
- **Database**: PostgreSQL (Neon Cloud)
- **Cache/Broker**: Redis (Session & Background processing ready)
- **Payments**: Stripe API
- **Styling**: Tailwind CSS (Modern Glassmorphic UI)
- **Image handling**: Pillow & Cropper.js
- **Auth**: django-allauth & Google OAuth

## Getting Started

### Method 1: Local Setup (Recommended)

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
3. **Environment Setup:** (Create a `.env` file based on the template below)
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

# Database (Neon Postgres)
DATABASE_URL=postgresql://user:pass@ep-host.aws.neon.tech/neondb?sslmode=require

# AI Assistant
GROQ_API_KEY="gsk_..."

# Social Auth
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

# Stripe Payments
STRIPE_PUBLIC_KEY="pk_test_..."
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
```

## Development Workflow

- **AI Features**: The chatbot logic resides in `chatbot/views.py`. It uses a custom RAG (Retrieval-Augmented Generation) flow to fetch store items.
- **Styling**: Tailwind is used for all UI components. Visual changes should follow the established Glassmorphism design pattern.
- **Migrations**: Always run `python manage.py makemigrations` and `migrate` after updating models.
