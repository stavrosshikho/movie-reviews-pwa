# Stavros Movie Review PWA

Stavros Movie Review PWA is a web application developed for a Year 12 Software Engineering assessment. The website allows users to create an account, log in, and post movie reviews using a star rating system.

The project demonstrates web development skills, including authentication, database storage, JavaScript interactivity, and offline functionality using a Progressive Web App (PWA) approach.

## Features

- User registration, login, and logout
- Secure password storage using hashing
- Post movie reviews with star ratings
- Edit and delete your own reviews
- View reviews posted by other users
- Offline access to previously visited pages
- Simple and clear user interface

## Technologies Used

- Python (Flask) – server-side logic and routing
- SQLite – database used to store users and reviews
- HTML & CSS – structure and styling of the website
- JavaScript – client-side interactivity and validation
- Service Worker – offline support and caching
- Web App Manifest – configuration for PWA features

## How the System Works

1. Users create an account and log in using a username and password.
2. Authentication is handled using server-side sessions.
3. Reviews are stored in an SQLite database and linked to the user who created them.
4. Only the original poster of a review can edit or delete it.
5. A service worker caches core pages and assets so content can still be accessed while offline.

## Offline Functionality

The website includes Progressive Web App functionality. Core pages and assets are cached using a service worker, allowing pages to load when the user is offline. Offline support works across modern browsers such as Chrome, Edge, and Safari.

## Installation and Running the Project

1. Clone the repository:
```
git clone https://github.com/stavrosshikho/movie-reviews-pwa
```

3. Navigate to the project folder:
```
   cd stavros-movie-review-pwa
```
5. Create and activate a virtual environment:

Mac/Linux
```
python3 -m venv .venv
source .venv/bin/activate

```
Windows
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
     
```
4. Install dependencies:
```
pip install -r requirements.txt
```

6. Run the application:
```
   python app.py
```
8. Open a browser and go to:
```
   http://127.0.0.1:5000
```
```
### Project Structure
stavros-movie-review-pwa/
│
├── app.py
├── database.db
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── sw.js
│   ├── manifest.webmanifest
│   ├── icon-192.svg
│   └── icon-512.svg
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_review.html
│   ├── edit_review.html
│   ├── login.html
│   ├── register.html
│   └── offline.html
│
└── README.md
```

## Security Considerations

- Passwords are stored using hashing instead of plain text.
- Server-side checks ensure only logged-in users can create reviews.
- Only the owner of a review can edit or delete it.

## Limitations and Future Improvements

- No password recovery system
- No review sorting or filtering

Possible future improvements include password reset functionality and review searching and filtering.

## Author

Created by Stavros  
Year 12 Software Engineering – Assessment Task 1
