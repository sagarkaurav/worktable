from datetime import datetime

from app import db
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class Member(UserMixin, db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    # username = db.Column(db.String(80), nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE")
    )
    organization = db.relationship(
        "Organization",
        backref=db.backref("members", passive_deletes=True),
        lazy="joined",
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    __table_args__ = (
        db.UniqueConstraint(
            "email", "organization_id", name="members_email_organization_id_uniq_const"
        ),
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_active(self):
        return True
