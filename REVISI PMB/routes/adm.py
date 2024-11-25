from app import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from models.mahasiswa import Mahasiswa
from models.orangtua import OrangTua
from models.status import Status
from models.riwayat import Riwayat

adm_bp = Blueprint('admin', __name__)

# DASHBOARD ADMIN
@adm_bp.route('/admin/dashboard')
@login_required
def dashboard():
    mahasiswa_list = Mahasiswa.query.all()  # AMBIL SEMUA DATA CALON MAHASISWA
    orangtua_list = OrangTua.query.all() # AMBIL SEMUA DATA ORANGTUA CALON MAHASISWA
    return render_template('admin/dashboard.html', mahasiswa=mahasiswa_list, orangtua=orangtua_list)

# KELOLA MAHASISWA
@adm_bp.route('/admin/dashboard')
@login_required
def manage():
    mahasiswa_list = Mahasiswa.query.all()  # AMBIL SEMUA DATA CALON MAHASISWA
    return render_template('admin/dashboard.html', mahasiswa=mahasiswa_list)

@adm_bp.route('/admin/dashboard/<int:mahasiswa_id>/terima')
@login_required
def terima_mahasiswa(mahasiswa_id):
    mahasiswa = Mahasiswa.query.get_or_404(mahasiswa_id)
    status_accepted = Status.query.filter_by(status='Diterima').first()

    # UPDATE STATUS
    mahasiswa.status_id = status_accepted.id
    db.session.commit()

    # SIMPAN RIWAYAT
    riwayat = Riwayat(mahasiswa_id=mahasiswa.id, status_id=status_accepted.id, admin_id=current_user.id)
    db.session.add(riwayat)
    db.session.commit()

    flash('Mahasiswa telah diterima.', 'success')
    return redirect(url_for('admin.dashboard'))

@adm_bp.route('/admin/dashboard/<int:mahasiswa_id>/tolak')
@login_required
def tolak_mahasiswa(mahasiswa_id):
    mahasiswa = Mahasiswa.query.get_or_404(mahasiswa_id)
    status_rejected = Status.query.filter_by(status='Ditolak').first()

    # UPDATE STATUS
    mahasiswa.status_id = status_rejected.id
    db.session.commit()

    # SIMPAN RIWAYAT
    riwayat = Riwayat(mahasiswa_id=mahasiswa.id, status_id=status_rejected.id, admin_id=current_user.id)
    db.session.add(riwayat)
    db.session.commit()

    flash('Mahasiswa telah ditolak.', 'danger')
    return redirect(url_for('admin.dashboard'))