from sqlalchemy import (
    Column, Integer, String, ForeignKey, Table, Enum, DateTime, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from database import Base
import enum
import uuid

# --- Many-to-many: accepted collaborators ---
project_collaborators = Table(
    "project_collaborators",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project_project.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("todo_users.id", ondelete="CASCADE"), primary_key=True),
)

# --- Invitation model ---
class InviteStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"
    revoked = "revoked"
    expired = "expired"

class ProjectInvite(Base):
    __tablename__ = "project_invites"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project_project.id", ondelete="CASCADE"), nullable=False, index=True)
    inviter_id = Column(Integer, ForeignKey("todo_users.id", ondelete="CASCADE"), nullable=False)
    invitee_email = Column(String, nullable=False, index=True)
    status = Column(Enum(InviteStatus), default=InviteStatus.pending, nullable=False)
    token_nonce = Column(String, nullable=False, default=lambda: uuid.uuid4().hex)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resent_at = Column(DateTime(timezone=True))

    project = relationship("Projects", back_populates="invites")
    inviter = relationship("TodoUsers")

    __table_args__ = (
        # Only one *pending* invite per (project, email)
        UniqueConstraint("project_id", "invitee_email", "status", name="uq_project_invite_pending"),
    )
