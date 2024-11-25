from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Status(db.Model):
    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False)
    
    # Relasi ke mahasiswa
    mahasiswa = relationship("Mahasiswa", back_populates="status")
