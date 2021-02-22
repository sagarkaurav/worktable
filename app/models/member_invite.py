import secrets
from datetime import datetime

from app import db


class MemberInvite(db.Model):
    __tablename__ = "member_invites"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship(
        "Organization",
        backref=db.backref("member_invites"),
        lazy="joined",
    )
    token = db.Column(
        db.String(100),
        nullable=False,
        default=lambda _: secrets.token_urlsafe(50),
        unique=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    __table_args__ = (
        db.UniqueConstraint(
            "email",
            "organization_id",
            name="member_invites_email_organization_id_uniq_const",
        ),
    )
