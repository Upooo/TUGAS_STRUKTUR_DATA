from app import create_app, db
from flask_login import LoginManager

from models.admin import Admin
from models.mahasiswa import Mahasiswa
from models.orangtua import OrangTua
from models.riwayat import Riwayat
from models.status import Status

app = create_app()
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    
    from models.admin import Admin
    from models.mahasiswa import Mahasiswa
    
    # MENGAMBIL USER BERDASARKAN USER_ID
    return Admin.query.get(int(user_id)) or Mahasiswa.query.get(int(user_id)) 

# MEMBUAT TABEL OTOMATIS JIKA BELUM ADA PADA DATABASE
with app.app_context():
    db.create_all() 
    print("[INFO] - TABEL BERHASIL DI BUAT")

if __name__ == '__main__':
    app.run(debug=True)
