from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class OrangTua(db.Model):
    __tablename__ = 'orangtua'
    
    id = Column(Integer, primary_key=True)
    mahasiswa_id = Column(Integer, ForeignKey('mahasiswa.id'))
    nama = Column(String(50), nullable=False)
    alamat = Column(String(100), nullable=False)
    nomor_telepon = Column(String(20), nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="orangtua") # --> RELASI KE TABEL MAHASISWA
