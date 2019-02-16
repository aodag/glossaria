from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject, Session


class Project(BaseObject):
    __tablename__ = "projects"
    query = Session.query_property()
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)


class Glossary(BaseObject):
    __tablename__ = "glossaries"
    query = Session.query_property()
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    description = Column(UnicodeText)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project")
    __table_args__ = (UniqueConstraint(name, project_id),)
