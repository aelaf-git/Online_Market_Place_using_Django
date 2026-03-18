# Online Marketplace

A comprehensive e-commerce platform built with Django and Tailwind CSS that allows users to list items for sale, browse categories, and communicate directly with sellers.

## Table of Contents

- [Features & Functionalities](#features--functionalities)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Design Decisions](#design-decisions)

## Features & Functionalities

### 1. User Authentication & Authorization (`core` app)

- **Sign Up / Log In:** Secure user registration and login functionality using Django's built-in authentication system.
- **Access Control:** Protected routes utilizing the `@login_required` decorator to ensure only authenticated users can create items, view their dashboard, or send messages.

### 2. Item Management (`item` app)

- **Browse Items:** Public users can view all listed items under the items page.
- **Item Details:** Detailed view of an individual item, showing its image, price, description, and the seller's information.
- **CRUD Operations:** Authenticated users can create, edit, and delete their own items dynamically.
- **Categories:** Items are organized into categories, enabling easier navigation, grouping, and filtering.

### 3. User Dashboard (`dashboard` app)

- **Personalized View:** A dedicated workspace (`dashboard:index`) for authenticated users to manage all the items they have currently listed for sale. Provides quick navigation to edit or delete operations.

### 4. Real-time Messaging & Conversations (`conversation` app)

- **Direct Communication:** Buyers can initiate a conversation with a seller directly from an item's detail page.
- **Inbox:** Users have a dedicated inbox (`conversation:inbox`) to track all their active conversations, whether they are buying or selling.
- **Conversation Threads:** Threaded messaging interface (`conversation:detail`) between the buyer and seller regarding a specific item, automatically ordered by modification date.

### 5. Core Interface

- **Responsive Design:** Styled uniformly with Tailwind CSS via CDN for a modern, mobile-friendly interface.
- **Reusability:** Extends from a modular `base.html` offering consistent layout, global navigation bar, and footer across all apps.

## System Architecture

The project strictly follows the standard **Django Model-Template-View (MTV)** architectural pattern:

### Models (Database Representation)

The models define the relational SQLite schema and utilize heavily integrated foreign keys.

- **Item App:** `Item`, `Category`
- **Conversation App:** `Conversation`, `ConversationMessage`
  The `Conversation` model uses a `ManyToManyField` to link multiple users (buyers/sellers) to a private thread tied to a specific `Item`.

### Views (Business Logic)

- Implemented as Python function-based views (FBVs).
- Business logic is clearly partitioned. For instance, the `conversation` views explicitly verify object ownership and membership (`members__in=[request.user.id]`) before showing threads or messages, ensuring strong data privacy.
- Uses `get_object_or_404` to maintain application stability on bad requests.

### Templates (Presentation Layer)

- HTML files enriched with the Django Template Language (DTL).
- Styled using Tailwind CSS utility classes, minimizing the need for custom CSS files.

### Project Structure

```text
Online_Market_Place/
├── core/                   # Overarching views (auth, base templates, index, contact)
├── item/                   # Item and Category models, CRUD views, and templates
├── dashboard/              # User-specific item management and views
├── conversation/           # Messaging system (inbox, threads, message models/forms)
├── market_place/           # Main Django project configuration (settings, urls, wsgi)
├── media/                  # Location for user-uploaded files (e.g., item images)
├── manage.py               # Django command-line utility
└── db.sqlite3              # SQLite database (default)
```

## Tech Stack

- **Backend Framework:** Django 4.2+ (Python 3.x)
- **Frontend Styling:** HTML5, Tailwind CSS
- **Database:** SQLite3 (Development)

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation & Setup

1. **Navigate to the project directory:**

   ```bash
   cd Online_Market_Place
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   _(Ensure you have Django and Pillow installed for image handling)_

   ```bash
   pip install django pillow
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create an admin user (optional):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Design Decisions

- **Tailwind CSS via CDN:** Chosen for rapid prototyping, keeping the HTML files relatively standalone while maintaining robust styling power without installing Node.js/NPM.
- **De-coupled Django Apps:** Business logic is compartmentalized. `dashboard` isolates user-specific rendering from general `item` browsing. `conversation` is extracted from items, enabling easier potential future features.
- **Secure by Default:** Django's built-in User model and session authentication are utilized heavily, paired with CSRF tokens on every form to prevent cross-site request forgery.
