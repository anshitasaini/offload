import uuid

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import relationship

Base = declarative_base()

from enum import Enum, unique


@unique
class sourceTypeEnum(Enum):
    website = "website"
    discord = "discord"


class Source(Base):
    __tablename__ = "sources"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at = Column(DateTime, default=func.now())
    type = Column(pgEnum(sourceTypeEnum, name="source_type"), nullable=False)
    data = Column(JSONB, nullable=True)
    name = Column(String, nullable=True)
    last_sync = Column(DateTime, nullable=True)
    next_refresh = Column(DateTime, default=func.now())

    # Relationships
    files = relationship("File", backref="source")



class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=func.now())
    title = Column(String, nullable=False)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    raw_content = Column(String, nullable=False)
    markdown = Column(String, nullable=False)
