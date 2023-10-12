from flask import Flask, render_template, request, redirect
import sqlite3
import json
import random

app = Flask(__name__)


def get_conn():
    '''
    Convenience function for getting a connection to the database.
    '''
    conn = sqlite3.connect('urls.db')
    return conn

@app.route('/', methods=('GET', 'POST'))
def index():
    '''
    Renders the main index page.
    If form for URL is submitted, returns index page with the shortened URL also displayed.
    '''
    if request.method == 'POST':
        # The user has submitted the form -- create a shortened URL and display it on the page
        short_url = shorten_url(request.form['url'])
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

def shorten_url(long_url):
    '''
    Given a URL string, creates a short URL route and saves it to the database.
    Returns the shortened URL string.
    '''
    try:
        conn = get_conn()
        existing_short = conn.execute('SELECT short_url FROM urls').fetchall()
        existing_short = [short[0] for short in existing_short]

        # Ensure that shortened URL is unique by only breaking the loop when it is unique
        while True:
            short_url = request.base_url + 's/' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
            if short_url not in existing_short:
                break
        
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (short_url, long_url))
        conn.commit()
    except sqlite3.Error as err:
        conn.rollback()
        print("Database error:", err)

    conn.close()
    return short_url

@app.route('/s/<short_route>', methods=('GET',))
def redirect_url(short_route):
    '''
    When a short URL is navigated to, redirects user to the full URL.
    '''
    try:
        conn = get_conn()
        long_url = conn.execute('SELECT long_url FROM urls WHERE short_url = ?',
                                (request.base_url,)).fetchall()
    except sqlite3.Error as err:
        print("Database error:", err)
    
    conn.close()

    if len(long_url) < 1 or len(long_url[0]) < 1:
        return "Error: invalid short URL"
    
    return redirect(long_url[0][0], 301)

@app.route('/get_urls', methods=('GET',))
def list_urls():
    '''
    Lists currently saved URLs as (short_url, long_url) pairs.
    '''
    try:
        conn = get_conn()
        urls = conn.execute('SELECT short_url, long_url FROM urls').fetchall()
    except sqlite3.Error as err:
        print("Database error:", err)

    conn.close()
    return json.dumps(urls)

if __name__ == '__main__':
    app.run()