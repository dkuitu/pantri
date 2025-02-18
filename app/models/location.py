from app import db
from datetime import datetime

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with pantry items
    items = db.relationship('PantryItem', backref='location', lazy=True)

    def __repr__(self):
        return f'<Location {self.name}>' 