from database import db

from flask_login import UserMixin

#for encrypting passwords
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


class User(UserMixin):
    """User."""

    def __init__(self, username, password, email, isAdmin=False, isDeletable=True):
        self.username = username
        self.id = username #for flask-login to work
        self.password = password
        self.email = email
        self.isAdmin = isAdmin 
        self.isDeletable = isDeletable

    @staticmethod
    def from_dict(source):
        return User(source['username'], source['password'], source['email'], source['isAdmin'], source['isDeletable'])

    def to_dict(self):
        return {
            'username' : self.username,
            'password' : self.password,
            'email' : self.email,
            'isAdmin' : self.isAdmin,
            'isDeletable' : self.isDeletable
        }


    @classmethod
    def register(cls, username, password, email, isAdmin, isDeletable):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, isAdmin=isAdmin, isDeletable=isDeletable)


    @staticmethod
    def get(username):
        doc = db.collection('users').document(username).get()
        if doc.exists:
            return User.from_dict(doc.to_dict())
        else:
            return None

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        user = User.get(username)

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False