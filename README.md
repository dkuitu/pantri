# Pantri

A modern, minimalist kitchen inventory and recipe management system built with Flask.

## Overview

Pantri helps you keep track of your kitchen inventory across different storage locations, monitor expiration dates, and manage recipes. It's designed to be simple, clean, and efficient.

## Features

### Inventory Management
- Track items across multiple storage locations (Fridge, Cupboards, etc.)
- Monitor quantities and expiration dates
- Quick add/edit/remove functionality
- Filter items by location

### Recipe Organization
- Store your favorite recipes
- See which recipes you can make with your current inventory
- Easy-to-read recipe cards with cook times and servings
- Tag and categorize recipes

### Shopping List
- Automatically generate lists based on recipes
- Track needed items
- Mark items as purchased

## Tech Stack

- **Backend**: Python/Flask
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML/CSS with TailwindCSS
- **Icons**: Lucide React

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/dkuitu/pantri.git
cd pantri
```

2. Set up your virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
pantri/
├── app/
│   ├── models/           # Database models
│   ├── routes/           # Route handlers
│   ├── static/           # Static files
│   ├── templates/        # Jinja2 templates
│   ├── __init__.py      # App initialization
│   └── config.py        # Configuration
├── migrations/          # Database migrations
├── .env                # Environment variables
├── .gitignore         # Git ignore file
├── README.md          # This file
├── requirements.txt   # Dependencies
└── run.py            # Application entry
```

## Development

To make changes to the database:

```bash
# After modifying models
flask db migrate -m "Description of changes"
flask db upgrade
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## License

This project is licensed under the MIT License.
