import uuid
from datetime import datetime

from app import db
from sqlalchemy.ext.hybrid import hybrid_property


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text(), nullable=False)
    members = db.relationship(
        "Member",
        secondary="members_projects",
        backref=db.backref("projects"),
        lazy="joined",
    )
    permissions = db.relationship(
        "MemberProject", backref=db.backref("projects"), lazy="joined"
    )
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"))
    project = db.relationship(
        "Project", remote_side=[id], backref=db.backref("comments")
    )

    created_by_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    last_updated_by_id = db.Column(db.Integer, db.ForeignKey("members.id"))

    @hybrid_property
    def owner(self):
        for member in self.members:
            if member.id == self.created_by_id:
                return member

    @hybrid_property
    def last_modified_by(self):
        if self.last_updated_by_id is None:
            return None
        for member in self.members:
            if member.id == self.last_updated_by_id:
                return member

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
