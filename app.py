from flask import Flask, render_template,  request, redirect, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'rahasia'

#BERINTERAKSI DENGAN DATABASE
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="database_pmb"
    )

#LOGIKA_INDEX
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/daftar', methods=['GET', 'POST'])
def daftar_mahasiswa():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        no_hp = request.form['no_hp']
        tanggal_lahir = request.form['tgl_lahir']
        alamat = request.form['alamat']
        jenis_kelamin = request.form['jenis_kelamin']

        # Koneksi ke database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Cek apakah email sudah terdaftar
        cursor.execute("SELECT * FROM mahasiswa WHERE email_mahasiswa = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Jika email sudah ada, tampilkan pesan error
            cursor.close()
            conn.close()
            return render_template('daftar.html', error_message="Email sudah terdaftar, silakan gunakan email lain.")

        # Jika email belum ada, lakukan insert data mahasiswa baru
        cursor.execute("""
        INSERT INTO mahasiswa (nama_mahasiswa, email_mahasiswa, no_hp_mahasiswa, tanggal_lahir_mahasiswa, alamat_mahasiswa, jenis_kelamin_mahasiswa)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (nama, email, no_hp, tanggal_lahir, alamat, jenis_kelamin))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Pendaftaran berhasil, silakan login!")
        return redirect('/')

    return render_template('daftar.html')

#LOGIKA_LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        no_hp = request.form['no_hp']

        conn = get_db_connection()
        cursor = conn.cursor()

        # PERIKSA APAKAH LOGIN SEBAGAI ADMIN
        query_admin = "SELECT * FROM admin WHERE email_admin = %s AND no_hp_admin = %s"
        cursor.execute(query_admin, (email, no_hp))
        admin = cursor.fetchone()

        if admin:
            session['user_id'] = admin[0]
            session['user_type'] = 'admin'
            flash("Login berhasil sebagai Admin.")
            return redirect('/admin/dashboard')
        
        # PERIKSA APAKAH LOGIN SEBAGAI MAHASISWA
        query_mahasiswa = "SELECT * FROM mahasiswa WHERE email_mahasiswa = %s AND no_hp_mahasiswa = %s"
        cursor.execute(query_mahasiswa, (email, no_hp))
        mahasiswa = cursor.fetchone()

        if mahasiswa:
            session['user_id'] = mahasiswa[0]
            session['user_type'] = 'mahasiswa'
            flash("Login berhasil sebagai Mahasiswa.")
            return redirect('/mahasiswa/profil')

        else:
            cursor.close()
            conn.close()
            return render_template('login.html', error_message="Email atau Nomor Telepon salah, silakan coba lagi.")

    
    return render_template('login.html')

#LOGIKA_LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash("Anda telah logout.")
    return redirect('/')

#LOGIKA_DASHBOARD
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def dashboard_admin():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    # Ambil kata kunci pencarian dari form atau query string
    search_query = request.args.get('search', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Jika ada pencarian, filter berdasarkan nama atau email mahasiswa
    if search_query:
        query = """
        SELECT m.id_mahasiswa, m.nama_mahasiswa, m.email_mahasiswa, m.no_hp_mahasiswa, 
               m.tanggal_lahir_mahasiswa, m.alamat_mahasiswa, m.jenis_kelamin_mahasiswa, 
               COALESCE(s.status, 'Menunggu') AS status
        FROM mahasiswa m
        LEFT JOIN status_mahasiswa s ON m.id_status = s.id_status
        WHERE m.nama_mahasiswa LIKE %s OR m.email_mahasiswa LIKE %s
        """
        cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        # Jika tidak ada pencarian, tampilkan semua mahasiswa
        query = """
        SELECT m.id_mahasiswa, m.nama_mahasiswa, m.email_mahasiswa, m.no_hp_mahasiswa, 
               m.tanggal_lahir_mahasiswa, m.alamat_mahasiswa, m.jenis_kelamin_mahasiswa, 
               COALESCE(s.status, 'Menunggu') AS status
        FROM mahasiswa m
        LEFT JOIN status_mahasiswa s ON m.id_status = s.id_status
        """
        cursor.execute(query)

    mahasiswa = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('adm_dashboard.html', mahasiswa=mahasiswa, search_query=search_query)

#LOGIKA_PROFILE
@app.route('/mahasiswa/profil')
def profil_mahasiswa():
    if 'user_id' not in session or session.get('user_type') != 'mahasiswa':
        flash("Silakan login sebagai Mahasiswa.")
        return redirect('/login')

    mahasiswa_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # MENGAMBIL DATA MAHASISWA BERDASARKAN ID
    query = "SELECT * FROM mahasiswa WHERE id_mahasiswa = %s"
    cursor.execute(query, (mahasiswa_id,))
    mahasiswa = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('profil_mhs.html', mahasiswa=mahasiswa)

#LOGIKA_TINDER
@app.route('/admin/tindakan_terkini', methods=['GET', 'POST'])
def tindakan_terkini():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Mengambil data mahasiswa
    query = """
    SELECT m.id_mahasiswa, m.nama_mahasiswa, m.email_mahasiswa, s.status
    FROM mahasiswa m
    LEFT JOIN status_mahasiswa s ON m.id_status = s.id_status
    """
    cursor.execute(query)
    mahasiswa = cursor.fetchall()

    if request.method == 'POST':
        id_mahasiswa = request.form['id_mahasiswa']
        keputusan = request.form['keputusan']

        # Update status mahasiswa
        update_query = "UPDATE mahasiswa SET id_status = %s WHERE id_mahasiswa = %s"
        cursor.execute(update_query, (keputusan, id_mahasiswa))
        conn.commit()
        flash("Tindakan berhasil disimpan.")
        return redirect('/admin/tindakan_terkini')

    # Mengambil status untuk dropdown
    cursor.execute("SELECT * FROM status_mahasiswa")
    status_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('tinder.html', mahasiswa=mahasiswa, status_list=status_list)

#LOGIKA_DAFTAR_ADMIN
@app.route('/admin/daftar_admin')
def daftar_admin():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Mengambil data admin
    query = "SELECT * FROM admin"
    cursor.execute(query)
    admins = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('daftar_admin.html', admins=admins)

#LOGIKA_TAMBAH_ADMIN
@app.route('/admin/tambah', methods=['GET', 'POST'])
def tambah_admin():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        no_hp = request.form['no_hp']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO admin (nama_admin, email_admin, no_hp_admin)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (nama, email, no_hp))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Admin berhasil ditambahkan.")
        return redirect('/admin/daftar_admin')

    return render_template('tambah_admin.html')

@app.route('/admin/hapus/<int:id_admin>', methods=['POST'])
def hapus_admin(id_admin):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Hapus admin berdasarkan ID
    query = "DELETE FROM admin WHERE id_admin = %s"
    cursor.execute(query, (id_admin,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Admin berhasil dihapus.")
    return redirect('/admin/daftar_admin')

@app.route('/admin/edit_mahasiswa/<int:id_mahasiswa>', methods=['GET', 'POST'])
def edit_mahasiswa(id_mahasiswa):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        no_hp = request.form['no_hp']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        status_id = request.form['status_id']

        query = """
        UPDATE mahasiswa
        SET nama_mahasiswa = %s, email_mahasiswa = %s, no_hp_mahasiswa = %s, tanggal_lahir_mahasiswa = %s, jenis_kelamin_mahasiswa = %s, alamat_mahasiswa = %s, id_status = %s
        WHERE id_mahasiswa = %s
        """
        cursor.execute(query, (nama, email, no_hp, tanggal_lahir, jenis_kelamin, alamat, status_id, id_mahasiswa))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Data mahasiswa berhasil diperbarui.")
        return redirect('/admin/dashboard')

    # Mengambil data mahasiswa yang akan diedit
    cursor.execute("SELECT * FROM mahasiswa WHERE id_mahasiswa = %s", (id_mahasiswa,))
    mahasiswa = cursor.fetchone()

    # Mengambil data status mahasiswa untuk dropdown
    cursor.execute("SELECT * FROM status_mahasiswa")
    status_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('edit_mahasiswa.html', mahasiswa=mahasiswa, status_list=status_list)

@app.route('/admin/hapus_mahasiswa/<int:id_mahasiswa>', methods=['POST'])
def hapus_mahasiswa(id_mahasiswa):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash("Silakan login sebagai Admin.")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM mahasiswa WHERE id_mahasiswa = %s"
    cursor.execute(query, (id_mahasiswa,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Mahasiswa berhasil dihapus.")
    return redirect('/admin/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
