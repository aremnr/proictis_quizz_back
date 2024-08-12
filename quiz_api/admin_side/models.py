from sqlalchemy import ForeignKey, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from quiz_app.models import Base
import datetime
import uuid

class AdminModel(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

