from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models.mahasiswa import Mahasiswa
from models.orangtua import OrangTua

mhs_bp = Blueprint('mahasiswa', __name__)

# FROM PENDAFTARAN MAHASISWA
@mhs_bp.route('/mahasiswa/new', methods=['GET', 'POST'])
def new_mahasiswa():
    if request.method == 'POST':
        # Data mahasiswa
        nama = request.form['nama']
        email = request.form['email']
        nomor_telepon = request.form['nomor_telepon']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        
        # Simpan data mahasiswa baru
        mahasiswa = Mahasiswa(nama=nama, email=email, nomor_telepon=nomor_telepon, 
                              tanggal_lahir=tanggal_lahir, jenis_kelamin=jenis_kelamin, alamat=alamat)
        db.session.add(mahasiswa)
        db.session.commit()

        # Data orang tua
        orang_tua_nama = request.form['orang_tua_nama']
        alamat = request.form['alamat']
        orang_tua_nomor_telepon = request.form['nomor_telepon']
        
        orang_tua = OrangTua(nama=orang_tua_nama, nomor_telepon=orang_tua_nomor_telepon, alamat=alamat, mahasiswa_id=mahasiswa.id)
        db.session.add(orang_tua)
        db.session.commit()


        flash('Pendaftaran berhasil! Anda akan menerima pemberitahuan mengenai status pendaftaran.', 'success')
        return redirect(url_for('mahasiswa.profile'))

    return render_template('mahasiswa/new.html')

#PROFILE MAHASISWA
@mhs_bp.route('/mahasiswa/profile')
@login_required
def profile():
    return render_template('mahasiswa/profile.html', mahasiswa=current_user)
