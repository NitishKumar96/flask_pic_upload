from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Index, VARCHAR, Boolean

class Book(db.Model):
    
    __tablename__ = "pic_table"

    id = Column(BigInteger(), primary_key=True)
    name = Column(VARCHAR(length=100), nullable=False)
    details = Column(JSONB)
    status = Column(Boolean(), nullable=False)


    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'author': self.author,
            'published':self.published
        }
