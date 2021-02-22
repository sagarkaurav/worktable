from datetime import datetime

from app import db


class MemberProject(db.Model):
    __tablename__ = "members_projects"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    member = db.relationship("Member", backref=db.backref("permissions"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    __table_args__ = (
        db.UniqueConstraint(
            "member_id",
            "project_id",
            name="members_projects_member_id_project_id_uniq_const",
        ),
    )
