import datetime
from _familySpin.connectors import db
from _familySpin.models.user import User


class UserOAuth(db.Model):
    __tablename__ = "userOAuth" 

    provider = db.Column(db.String(50), nullable=False, primary_key=True)
    subject = db.Column(db.String(200), nullable=False, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("provider", "subject"),)

    @classmethod
    def get_or_create(cls, provider, subject, email=None, familyname=None):
        identity = cls.query.filter_by(provider=provider, subject=subject).first()
        if identity:
            return User.find_by_id(cls.user_id)

        user = User.find_by_email(email) if email else None
        if not user:
            user = User.create_user(email=email or f"{provider}_{subject}@example.com",
                                    familyname=familyname or "Unknown")

        identity = cls(provider=provider, subject=subject, user_id=user.id)
        db.session.add(identity)
        db.session.commit()
        return user