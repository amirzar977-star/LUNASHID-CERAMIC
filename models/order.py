from database import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(50), default="در انتظار")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
