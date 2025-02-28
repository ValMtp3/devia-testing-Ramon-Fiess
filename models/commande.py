from models.database import db

class Commande(db.Model):
    __tablename__ = "commandes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(200), nullable=False)
    cs

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "prix": self.prix, "location": self.location, "date": self.date}
