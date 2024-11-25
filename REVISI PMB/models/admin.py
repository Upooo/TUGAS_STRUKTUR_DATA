from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = Column(Integer, primary_key=True)
    nama = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    nomor_telepon = Column(String(20), nullable=False)

    riwayat = relationship("Riwayat", back_populates="admin") # --> RELASI KE TABEL RIWAYAT

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)