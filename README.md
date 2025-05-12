# SCSU BookSwap

SCSU BookSwap is a peer-to-peer textbook exchange platform created for Southern Connecticut State University students. It allows users to buy, sell, or trade textbooks and course materials within a trusted and local community. This project was developed as part of a Software Design and Development course.

## Contributors

- Justin Brennan  
- Tatiana Eng  
- Adrian Flores  
- Asante Frye  
- Orlando Marin

## Project Overview

The goal of the project is to provide SCSU students with a secure, user-friendly platform for exchanging textbooks. Unlike general-purpose platforms, SCSU BookSwap focuses on student needs such as verified campus access, low cost, simplicity, and community trust.

## Features

- Secure login and registration restricted to @southernct.edu emails
- User profile dashboard with navigation options
- Create and post listings with details such as title, author, ISBN, condition, subject, price, and notes
- Browse all active listings in a feed format
- Comment system for asking questions or expressing interest in listings
- Form validation and error handling for user inputs

## Tech Stack

- Python
- Flask
- Flask-WTF
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- HTML, CSS (custom with Flexbox)
- pytz

## How to Run the App Locally

1. Clone the repository:

   git clone https://github.com/yourusername/scsu-bookswap.git  
   cd scsu-bookswap

2. Create a virtual environment and activate it:

   python -m venv venv  
   source venv/bin/activate  (on Windows: venv\Scripts\activate)

3. Install dependencies:

   pip install -r requirements.txt

4. Run the application:

   python run.py

The app will be available at http://127.0.0.1:5000/

## Database Models

- User: userID, fname, lname, major, email, pwd
- Book: bookID, bookTitle, origPrice, listPrice, condition, userID, isbn, author, subject, notes
- Listing: listingID, timestamp, bookID, userID
- Comment: commentID, listingID, userID, text, timeStamp

## Routes Overview

- /                      - Welcome page  
- /login                 - Login page  
- /register              - Registration page  
- /profile               - User dashboard  
- /create_listing        - Create a new book listing  
- /listings              - View all listings  
- /listing/<listing_id>/comment - Post a comment  
- /logout                - Log out of the application

## Future Improvements

- Add image uploads to listings
- Secure password storage using hashing
- Implement direct messaging between users
- Build an admin dashboard for moderation and analytics
- Improve mobile responsiveness and accessibility

## License

This project is for educational purposes only and is not intended for production use.
