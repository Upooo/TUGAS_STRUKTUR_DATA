from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
import enum

class Gender(enum.Enum):
    LAKI_LAKI = "l"
    PEREMPUAN = "P"

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    
    id = Column(Integer, primary_key=True)
    nama = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    nomor_telepon = Column(String(20), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    jenis_kelamin = Column(Enum(Gender), nullable=False)
    alamat = Column(String(255), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'))
    
    # RELASI KE TABEL STATUS, ORANGTUA, DAN RIWAYAT
    status = relationship("Status", back_populates="mahasiswa")
    orangtua = relationship("OrangTua", uselist=False, back_populates="mahasiswa")
    riwayat = relationship("Riwayat", back_populates="mahasiswa")

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)