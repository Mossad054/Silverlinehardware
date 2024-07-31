Silverline Hardware E-Commerce.
Introduction
Welcome to the  Silverline Hardware E-commerce Project! This project was designed to provide a seamless and efficient platform for online shopping, enabling users to browse, purchase, and manage products effortlessly. Our goal was to create an application that is both user-friendly and feature-rich, catering to the needs of both buyers and sellers.

Features
User Authentication: Secure user registration and login.
Product Management: Add, update, and delete products.
Shopping Cart: Add products to the cart and manage quantities.
Checkout Process: Seamless checkout with multiple payment options.
Order Management: Track orders and order history.
Responsive Design: Mobile and tablet-friendly layout.
Technologies Used
Backend
Python
Flask
SQLAlchemy
Frontend
HTML5
CSS3
Database
SQLite 
Installation
To get a local copy up and running, follow these steps:

Prerequisites
Python 3.8+
Baakipay setup
Clone the repository:

sh
Copy code
git clone https://github.com/Mossad054/Silverlinehardware.git
cd ecommerce-project
Create a virtual environment and activate it:

sh
Copy code
python -m venv venv
source venv/bin/activate
Install the required packages:

sh
Copy code
pip install -r requirements.txt
Set up the database:

sh
Copy code
flask db init
flask db migrate
flask db upgrade
Run the development server:

sh
Copy code
flask run
Usage
Open your web browser and navigate to http://localhost:5000.
Register a new account or log in with an existing one.
Browse products, add them to your cart, and proceed to checkout.
Manage your orders and track order history.
Architecture

The application follows a typical three-tier architecture:

Presentation Layer: Implemented using HTML and CSS for a dynamic and responsive user interface.
Business Logic Layer: Managed by Flask for handling API requests and business logic.
Data Layer: SQLAlchemy for ORM and database interactions.
Challenges and Solutions
Challenge 1: User Authentication
Situation: Ensuring secure authentication and authorization.
Task: Implement a secure authentication system.
Action: Used Flask's built-in authentication system and implemented JWT for secure token-based authentication.
Result: Achieved a robust and secure user authentication process.
