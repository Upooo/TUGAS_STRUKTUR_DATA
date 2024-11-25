from app import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Riwayat(db.Model):
    __tablename__ = 'riwayat'
    
    id = Column(Integer, primary_key=True)
    mahasiswa_id = Column(Integer, ForeignKey('mahasiswa.id'))
    status_id = Column(Integer, ForeignKey('status.id'))
    tanggal_perubahan = Column(DateTime, default=datetime.utcnow)
    admin_id = Column(Integer, ForeignKey('admin.id'))
    
    # RELASI KE TABEL MAHASISWA DAN STATUS
    mahasiswa = relationship("Mahasiswa", back_populates="riwayat")
    status = relationship("Status")
    admin = relationship("Admin", back_populates="riwayat")
