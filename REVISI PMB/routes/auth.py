from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user

from models.admin import Admin
from models.mahasiswa import Mahasiswa

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        nomor_telepon = request.form['nomor_telepon']
        
        # CEK APAKAH ADMIN
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.nomor_telepon == nomor_telepon:
            login_user(admin)
            return redirect(url_for('admin.dashboard'))  # JIKA YA MAKA AKAN KE DASHBOARD ADMIN

        # CEK APAKAH MAHASISWA
        mahasiswa = Mahasiswa.query.filter_by(email=email).first()
        if mahasiswa and mahasiswa.nomor_telepon == nomor_telepon:
            login_user(mahasiswa)
            return redirect(url_for('mahasiswa.profile'))  # JIKA YA MAKA AKAN DI ARAHKAN
        flash('Email atau nomor telepon salah!', 'danger')

    return render_template('auth/login.html')

# Fungsi untuk registrasi
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app import db
    if request.method == 'POST':
        email = request.form['email']
        nomor_telepon = request.form['nomor_telepon']
        nama = request.form['nama']

        # Cek apakah email sudah terdaftar
        if Admin.query.filter_by(email=email).first() or Admin.query.filter_by(email=email).first():
            flash('Email sudah terdaftar!', 'danger')
            return redirect(url_for('auth.register'))

        # Simpan data mahasiswa baru
        admin = Admin(nama=nama, email=email, nomor_telepon=nomor_telepon)
        db.session.add(admin)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

# Fungsi untuk logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))
