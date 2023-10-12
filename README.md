# URL Shortener

This application allows users to reduce long URLs to shorter, unique URLs.

The frontend platform is built in HTML and CSS/Bootstrap. Since the application uses Flask as the backend web framework, you will need to have Flask and Python 3+ in your environment in order to host the website locally.

## To run:

- In the terminal, run `python init_db.py` in the main directory to initialize the necessary SQLite database first.
- Then run `python -m flask --app server run` and navigate to http://127.0.0.1:5000 on the browser to view the website.