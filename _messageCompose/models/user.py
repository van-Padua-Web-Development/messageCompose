from _familySpin.connectors import db, ph
from flask_login import UserMixin
import uuid, datetime

class User(db.Model, UserMixin):
    __tablename__ = "user"         # actual table name in users.db

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    familyname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(256))
    verified = db.Column(db.Boolean, default=False)
    maxCatalog = db.Column(db.Integer, default=25)
    budget = db.Column(db.Float, default=0.0)
    weekly_savings = db.Column(db.Float, default=0.0)
    created_on = db.Column(db.DateTime)
    last_sign_in = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    energy = db.Column(db.Integer, default=10)
    maxEnergy = db.Column(db.Integer, default=10)
    parking_required = db.Column(db.Boolean, default=False)
    city = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    h3_hex6 = db.Column(db.String(120), nullable=False)
    h3_hex5 = db.Column(db.String(120), nullable=False)
    long = db.Column(db.Integer, default=10)
    lat = db.Column(db.Integer, default=10)

    familyMembers = db.relationship(
        "familyMember",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"  # loads family members automatically
    )

    @classmethod
    def create_user(cls, email, familyname=None, password=None, verified=False, **kwargs):
        user = cls(
            id=str(uuid.uuid4()),
            email=email,
            familyname=familyname,
            password=ph.hash(password),
            verified=verified,
            created_on=datetime.utcnow(),
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def update_last_signin(self):
        self.last_sign_in = datetime.datetime.now()
        db.session.commit()

    def check_password(self, password: str) -> bool:
        try:
            return ph.verify(self.password, password)
        except Exception:
            return False
        
    def to_dict(self):
        """Convert all columns to dict for JSON"""
        return {"budget": self.budget, "weekly_savings": self.weekly_savings, "energy": self.energy, "maxEnergy": self.maxEnergy}

class familyMember(db.Model):
    __tablename__ = "familyMembers"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    user = db.relationship("User", back_populates="familyMembers")
  