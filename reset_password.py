from main import app
from flask_mail import Mail, Message

mail = Mail(app)

    msg = Message("Hello",
                  sender="from@example.com",
                  recipients=["to@example.com"])