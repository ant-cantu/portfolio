from flask import Flask, render_template, request, jsonify
import requests
from forms import ContactForm
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

print(DISCORD_WEBHOOK_URL)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
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
            r = requests.post(DISCORD_WEBHOOK_URL, json=message)

            return jsonify(success=True)
        else:
            # Add error handler
            print("Did not validate!!")
    return render_template('index.html', form=form)

@app.route("/privacy-policy")
def privacy():
    return render_template('privacy.html')
    

if __name__ == "__main__":
    app.run(debug=True)