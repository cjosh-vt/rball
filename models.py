#from app import db

class Authenticate_db(db.Model):
    __tablename__ = 'auth_login'

    player_id=db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String())
    password= db.Column(db.String())

    def __init__(self, username, password):
        self.player_id = player_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<username {(self.username)}>"
    
    def serialize(self):
        return {
            'player_id': self.player_id,
            'username': self.username, 
            'password': self.password
        }
