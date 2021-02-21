import uuid
from datetime import datetime

from app import db


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id", ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"))
    project = db.relationship(
        "Project", remote_side=[id], backref=db.backref("comments")
    )
    owner = db.relationship(
        "Member", backref=db.backref("projects", passive_deletes=True)
    )
    # comments_count = db.column_property(
    #     db.select([db.func.count(project.id)]).where(project.project_id == 1)
    # )
    last_updated_by = db.relationship("Member")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
