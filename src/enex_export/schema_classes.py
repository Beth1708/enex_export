# Python for sqlalchemy classes, paste in the contents of the capture.schema file
# Generated this using the jetbrains ai assistant.
# Another idea is to use SQLAlchemy's automap feature or sqlacodegen
# See comments in obsidian
# Comment from the ai assistant
# In these classes, ForeignKey is used to set referential integrity between the tables. Also relationship is used to
# provide a relationship between two mapped classes for a specific association.
# Please replace the data types and relationships according to your exact requirements. The above code is for
# illustration. Also, remember to create a session and add these objects to your database using that session.


from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DbMeta(Base):
    __tablename__ = "db_meta"
    db_version = Column(Text, primary_key=True)


class DocMeta(Base):
    __tablename__ = "doc_meta"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    source_url = Column(Text)

    attributes = relationship("Attributes", cascade="all, delete-orphan")
    content_files = relationship("ContentFiles", cascade="all, delete-orphan")


class Attributes(Base):
    __tablename__ = "attributes"
    id = Column(Integer, primary_key=True)
    doc_meta_id = Column(Integer, ForeignKey("doc_meta.id", ondelete="CASCADE"))
    source = Column(Text)
    source_url = Column(Text)


class ContentFiles(Base):
    __tablename__ = "content_files"
    id = Column(Integer, primary_key=True)
    doc_meta_id = Column(Integer, ForeignKey("doc_meta.id", ondelete="CASCADE"))
    filename = Column(Text)
    content_type = Column(Text)
    mime_type = Column(Text)
    width = Column(Integer)
    height = Column(Integer)
    data = Column(Text)


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(Text, nullable=False)


class DocTagLink(Base):
    __tablename__ = "doc_tag_link"
    doc_id = Column(
        Integer, ForeignKey("doc_meta.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )
