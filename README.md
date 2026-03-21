# Online Marketplace (Neo Market)

A high-performance, futuristic e-commerce platform built with Django 6.0 and Tailwind CSS. Neo Market allows users to list items for sale, browse categories with a premium UI, and communicate directly with sellers via a real-time messaging system.

## Table of Contents

- [Features & Functionalities](#features--functionalities)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Design Decisions](#design-decisions)

## Features & Functionalities

### 1. Advanced Authentication & OAuth (`core` app)

- **Local & Social Login:** Supports standard credentials and **Google OAuth 2.0** integration via `django-allauth`.
- **Seamless Account Linking:** Automatically connects social login to existing accounts with the same email address.
- **Access Control:** Fully protected routes ensure only authenticated users can manage items or participate in chats.

### 2. Modern User Profiles (`core` app)

- **Interrupted Setup Flow:** New users are automatically redirected to a profile setup page to provide a profile picture and bio before using the platform.
- **Dynamic Avatars:** Displays user avatars and usernames in the navigation bar using the `Profile` model.
- **Automatic Profile Generation:** Uses Django signals to create user profiles instantly upon registration.

### 3. Item Management (`item` app)

- **Futuristic Browse Experience:** Categories and items are displayed with vibrant dark-mode aesthetics and hover effects.
- **Full CRUD:** Sellers can create, edit, and delete their own items with image upload support.
- **Smart Categorization:** Items are dynamically filtered by categories for intuitive navigation.

### 4. Interactive Messaging (`conversation` app)

- **Direct Chats:** Buyers can initiate private message threads with sellers instantly from item pages.
- **Unified Inbox:** A dedicated management interface for all active buying and selling conversations.

### 5. Premium UI/UX

- **Glassmorphism Design:** Utilizes Tailwind CSS to create a sleek, transparent, and neon-accented interface.
- **Responsive Layout:** Optimized for all screen sizes with a sticky blur-effect navigation bar.

## System Architecture

### Models

- **Item App:** `Item`, `Category`
- **Conversation App:** `Conversation`, `ConversationMessage`
- **Core App:** `Profile` (One-to-One with User)

### Logic & Views

- **Function-Based Views (FBVs):** Clean, readable logic for handling requests.
- **Custom Adapters:** `CustomAccountAdapter` and `CustomSocialAccountAdapter` manage custom redirect logic and profile validation.
- **Security:** Built-in protection against CSRF, SQL Injection, and XSS.

## Tech Stack

- **Backend:** Django 6.0.2
- **Authentication:** django-allauth (w/ SocialAccount)
- **Styling:** Tailwind CSS (Modern Utility-First)
- **Environment Management:** django-environ
- **Database:** SQLite3 (Development) / PostgreSQL (Production ready)
- **Image Processing:** Pillow

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone & Navigate:**

   ```bash
   cd Online_Market_Place
   ```

2. **Setup Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables:**
   Create a `.env` file in the root directory:

   ```env
   SECRET_KEY="your-django-secret-key"
   DEBUG=True
   GOOGLE_CLIENT_ID="your-google-client-id"
   GOOGLE_CLIENT_SECRET="your-google-client-secret"
   ```

5. **Migrations & Superuser:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Server:**
   ```bash
   python manage.py runserver
   ```

## Design Decisions

- **Dark-First Modernity:** The UI is designed to look premium, using a palette of Deep Slate, Cyan, and Purple to create a "Cyborg/Cyberpunk" aesthetic.
- **Zero Hardcoding for Secrets:** All sensitive credentials (API keys, secret keys) are managed via `.env` to prevent accidental exposure.
- **Extensible Profiles:** The `Profile` model is decoupled from the `User` model to allow for future expansion without modifying the core Auth system.
