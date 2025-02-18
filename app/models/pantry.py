from app import db
from datetime import datetime
from app.models.location import Location  # Import Location instead of defining it

class PantryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f'<PantryItem {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'location': self.location.name
        }

    @property
    def display_amount(self):
        """Format the quantity and unit for display"""
        return f"{self.quantity} {self.unit}"

    @property
    def is_expired(self):
        """Check if item is expired"""
        if not self.expiry_date:
            return False
        return self.expiry_date < datetime.now().date()

    @property
    def expiring_soon(self):
        """Check if item is expiring within 7 days"""
        if not self.expiry_date:
            return False
        days_until_expiry = (self.expiry_date - datetime.now().date()).days
        return 0 <= days_until_expiry <= 7
