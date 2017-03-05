from . import db

class UserProfile(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    biography = db.Column(db.String(255))
    image = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    age = db.Column(db.String(80))
    profile_created_on = db.Column(db.String(255))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)