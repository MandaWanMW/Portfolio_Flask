from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

#Environmental variables
PORTFOLIO_DBSERVER = os.getenv('PORTFOLIO_DBSERVER')
PORTFOLIO_PORT = os.getenv('PORTFOLIO_PORT')
PORTFOLIO_DBOA = os.getenv('PORTFOLIO_DBOA')
PORTFOLIO_DBOB = os.getenv('PORTFOLIO_DBOB')

#Email Settings
app.config['MAIL_SERVER'] = PORTFOLIO_DBSERVER
app.config['MAIL_PORT'] = PORTFOLIO_PORT
app.config['MAIL_USERNAME'] = PORTFOLIO_DBOA
app.config['MAIL_PASSWORD'] = PORTFOLIO_DBOB
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=["GET", "POST"])
def home():
  return render_template("index.html")

@app.route('/success_contact', methods=['GET', 'POST'])
def send_email():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    #Send Message
    msg = Message(f'New Contact Form Submission - {name}', 
                  sender=email,
                  recipients=[PORTFOLIO_DBOA])
    msg.body = f'Name: {name}\nEmail: {email}\n\n{message}'
    mail.send(msg)

    #Confirmation message
    success = 'Thanks for your message!'
    response = 'I will get back to you soon.'
  
  return render_template('success_contact.html', success=success, response=response)

if __name__ == "__main__":
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=False)