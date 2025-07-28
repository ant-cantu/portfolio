from flask import Flask, render_template, request, jsonify, abort
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
import requests
from forms import ContactForm
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Secret Key CRSF Protection
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Discord Webhook URL
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Redis Server URI
if os.getenv('APP_ENV') == "development":
    LIMITER_URI = "memory://"
else:
    LIMITER_URI = os.getenv("REDIS_URI")

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=LIMITER_URI
)

@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    return render_template(
        'index.html', 
        form=form
    )

@app.route("/submit-form", methods=['POST'])
def submit():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                with limiter.limit("10 per day;2 per 5 minute"):
                    if form.honeypot.data:
                        print("SPAM Detected!!")
                        # Handle this error correctly before launch
                        return render_template('index.html', form=form)
                    
                    name = form.name.data
                    email = form.email.data
                    message = form.message.data
                    terms = form.terms.data

                    message = {
                        "content": f"Name: {name}\nEmail: {email}\nMessage:\n{message}\nTerms Accepted: {terms}"
                    }
                    requests.post(DISCORD_WEBHOOK_URL, json=message)

                    return jsonify(success=True)
            except RateLimitExceeded: 
                return jsonify(success=False, errors={'rate limit': ['Too many requests, please try again later.']}), 429
        else:
            # Add error handler
            return jsonify(success=False, errors=form.errors)

@app.route("/privacy-policy")
def privacy():
    return render_template('privacy.html')

if os.getenv('APP_ENV') == "development":
    if __name__ == "__main__":
        app.run(debug=True)