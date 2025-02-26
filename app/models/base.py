from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
import uuid
from slugify import slugify

# Create a declarative base class
Base = declarative_base()


# Define the abstract base class with UUID and timestamps
class BaseModelWithUUID(Base):
    __tablename__ = "base_model"
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(
        String, unique=True, index=True, default=lambda: str(uuid.uuid4())
    )  # Corrected the default for uuid
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Base model with name, slug, and description
class NameSlugDescriptionBaseModel(BaseModelWithUUID):
    __abstract__ = True

    name = Column(String, index=True)
    slug = Column(String, index=True)
    description = Column(String)

    @validates("name")
    def update_slug(self, key, name):
        """Automatically generate a slug when name is set"""
        self.slug = slugify(name)
        return name  # Return name to maintain validation chain
