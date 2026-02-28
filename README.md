Mechanic Shop API - README
📋 Project Description
The Mechanic Shop API is a comprehensive RESTful backend service designed to manage all aspects of an automotive repair shop's daily operations. Built with Flask and SQLAlchemy, this API provides a robust platform for handling customers, mechanics, service tickets, parts inventory, and work assignments.

Key Features
Customer Management: Register, authenticate, and manage customer profiles

Mechanic Management: Track mechanics, their specializations, and work assignments

Service Tickets: Create and track repair jobs from start to completion

Parts Inventory: Manage parts stock and track parts used in repairs

Assignment System: Assign mechanics to tickets and parts to specific jobs

Authentication: Role-based JWT authentication (customer and mechanic roles)

Rate Limiting: Protect endpoints from abuse with configurable rate limits

Caching: Improve performance with response caching

Comprehensive Testing: Extensive unit and integration tests

🚀 Getting Started
Prerequisites
Python 3.12 or higher

pip (Python package manager)

Git (optional, for cloning)

Installation
Clone the repository

bash
git clone <repository-url>
cd mechanic-shop-api
Create a virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables (optional)
Create a .env file in the root directory:

env
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url (for production)
Initialize the database

bash
python main.py
This will create the SQLite database and all required tables.

Run the application

bash
python main.py
The server will start at http://127.0.0.1:5000

📚 API Documentation
Once the application is running, you can access the interactive Swagger documentation:

text
http://127.0.0.1:5000/api/docs
Base URL
Development: http://127.0.0.1:5000

Production: https://api-application-factory-pattern.onrender.com

Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

text
Authorization: Bearer <your-token>
Core Endpoints
Customers (/customers)
Method	Endpoint	Description	Auth Required
POST	/customers/login	Customer login	No
POST	/customers	Register new customer	No
GET	/customers	Get all customers (paginated)	No
GET	/customers/<id>	Get customer by ID	No
PUT	/customers	Update own profile	Yes (Customer)
DELETE	/customers/<id>	Delete customer	No
GET	/customers/profile	Get own profile	Yes (Customer)
GET	/customers/my-tickets	Get customer's tickets	Yes (Customer)
GET	/customers/search	Search customer by email	No
Mechanics (/mechanics)
Method	Endpoint	Description	Auth Required
POST	/mechanics/login	Mechanic login	No
POST	/mechanics	Create new mechanic	No
GET	/mechanics	Get all mechanics	No
PUT	/mechanics	Update own profile	Yes (Mechanic)
DELETE	/mechanics	Delete own account	Yes (Mechanic)
GET	/mechanics/profile	Get own profile	Yes (Mechanic)
GET	/mechanics/my-tickets	Get assigned tickets	Yes (Mechanic)
GET	/mechanics/top-mechanics	Get top 5 mechanics by ticket count	No
Service Tickets (/tickets)
Method	Endpoint	Description	Auth Required
POST	/tickets	Create service ticket	Yes (Mechanic)
GET	/tickets	Get all tickets (paginated)	Yes (Mechanic)
GET	/tickets/<id>	Get ticket by ID	No
PUT	/tickets/<id>	Update ticket	Yes (Assigned Mechanic)
DELETE	/tickets/<id>	Delete ticket	Yes (Assigned Mechanic)
POST	/tickets/<id>/mechanics/<mid>	Assign mechanic to ticket	Yes (Mechanic)
DELETE	/tickets/<id>/mechanics/<mid>	Remove mechanic from ticket	Yes (Mechanic)
POST	/tickets/<id>/parts/<pid>	Add part to ticket	Yes (Mechanic)
DELETE	/tickets/<id>/parts/<pid>	Remove part from ticket	Yes (Mechanic)
GET	/tickets/<id>/parts	Get all parts for a ticket	No
Parts & Inventory (/parts)
Method	Endpoint	Description	Auth Required
POST	/parts/inventory	Create inventory item	Yes (Mechanic)
GET	/parts/inventory	Get all inventory items	No
GET	/parts/inventory/<id>	Get inventory item by ID	No
PUT	/parts/inventory/<id>	Update inventory item	Yes (Mechanic)
DELETE	/parts/inventory/<id>	Delete inventory item	Yes (Mechanic)
POST	/parts	Create part	Yes (Mechanic)
GET	/parts	Get all parts	No
GET	/parts/<id>	Get part by ID	No
PUT	/parts/<id>	Update part	Yes (Mechanic)
DELETE	/parts/<id>	Delete part	Yes (Mechanic)
GET	/parts/available	Get unassigned parts	No
🧪 Testing
The project includes comprehensive tests using both unittest and pytest.

Running All Tests
bash
# Using unittest
python -m unittest discover app/tests

# Using pytest
pytest app/tests -v
Running Specific Test Files
bash
# Test customers
python app/tests/test_customer.py

# Test mechanics
python app/tests/test_mechanic.py

# Test parts and inventory
python app/tests/test_parts.py

# Test service tickets
python app/tests/test_service_tickets.py

# Using pytest with specific file
pytest app/tests/test_pytest_customer.py -v
🏗️ Project Structure
text
mechanic-shop-api/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── extensions.py          # Extension initializations
│   ├── models.py              # Database models
│   ├── util/
│   │   └── auth.py            # JWT authentication
│   ├── blueprints/            # Route blueprints
│   │   ├── customers/         # Customer routes
│   │   ├── mechanics/         # Mechanic routes
│   │   ├── parts/             # Parts routes
│   │   └── service_tickets/   # Ticket routes
│   └── tests/                 # Test files
│       ├── test_customer.py
│       ├── test_mechanic.py
│       ├── test_parts.py
│       ├── test_service_tickets.py
│       └── test_pytest_customer.py
├── static/                     # Static files
│   ├── *.yaml                  # Swagger documentation
│   └── ERD.png                 # Entity Relationship Diagram
├── config.py                   # Configuration classes
├── main.py                     # Application entry point
├── merge_swagger.py            # Swagger file merger
├── requirements.txt            # Dependencies
└── README.md                   # This file
🔧 Configuration
The application supports three configuration environments:

Development: SQLite database, debug mode enabled

Testing: In-memory SQLite database, test-specific settings

Production: PostgreSQL (via Render), debug mode disabled

Configure via config.py or environment variables.

📦 Dependencies
Key dependencies include:

Flask 3.1.2 - Web framework

Flask-SQLAlchemy 3.1.1 - ORM

Flask-Marshmallow 1.3.0 - Serialization

Flask-Limiter 4.0.0 - Rate limiting

Flask-Caching 2.3.1 - Response caching

python-jose 3.5.0 - JWT authentication

pytest 9.0.1 - Testing

Gunicorn 23.0.0 - WSGI server (production)

🚢 Deployment
This API is configured for easy deployment on Render.com:

Push code to GitHub

Connect repository to Render

Set environment variables:

SECRET_KEY: Your secret key

DATABASE_URL: PostgreSQL connection string (provided by Render)

Deploy!

The included main.yaml GitHub Actions workflow automates CI/CD.

🤝 Contributing
Fork the repository

Create a feature branch

Write tests for new functionality

Ensure all tests pass

Submit a pull request
