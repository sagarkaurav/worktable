import secrets
from datetime import datetime, timedelta

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
    reset_password_token = db.Column(db.String(255), nullable=True, unique=True)
    reset_password_token_created_at = db.Column(db.DateTime, nullable=True)
    reset_password_token_valid_for = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    disabled_at = db.Column(db.DateTime, nullable=True)
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

    def is_reset_token_valid(self, token):
        if self.reset_password_token is None:
            return False
        if self.reset_password_token != token:
            return False
        reset_created_at = self.reset_password_token_created_at
        valid_till = reset_created_at + timedelta(
            seconds=self.reset_password_token_valid_for
        )
        current = datetime.utcnow()
        if current < valid_till:
            return True
        return False

    def remove_reset_token(self):
        self.reset_password_token = None
        self.reset_password_token_created_at = None
        self.reset_password_token_valid_for = None

    def create_reset_password_token(self):
        self.reset_password_token = secrets.token_urlsafe(50)
        self.reset_password_token_valid_for = 3600
        self.reset_password_token_created_at = datetime.utcnow()
        return self.reset_password_token

    @property
    def is_active(self):
        return True
