import mysql.connector

# MENGHUBUNGKAN KE MYSQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = conn.cursor()

# BUAT DATABASE
cursor.execute("CREATE DATABASE IF NOT EXISTS database_pmb")

# GUNAKAN DATABASE
cursor.execute("USE database_pmb")

# BUAT TABEL MAHASISWA
cursor.execute("""
CREATE TABLE IF NOT EXISTS mahasiswa (
    id_mahasiswa INT AUTO_INCREMENT PRIMARY KEY,
    nama_mahasiswa VARCHAR(255),
    email_mahasiswa VARCHAR(255) UNIQUE,
    no_hp_mahasiswa VARCHAR(20),
    tanggal_lahir_mahasiswa DATE,
    alamat_mahasiswa TEXT,
    jenis_kelamin_mahasiswa ENUM('L', 'P'),
    id_status INT DEFAULT 0
)
""")

# BUAT TABEL ADMIN
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nama_admin VARCHAR(255),
    email_admin VARCHAR(255) UNIQUE,
    no_hp_admin VARCHAR(20)
)
""")

# BUAT TABEL STATUS
cursor.execute("""
CREATE TABLE IF NOT EXISTS status_mahasiswa (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50)
)
""")

print("[INFO] - DATABASE DAN TABEL BERHASIL DI BUAT")
cursor.close()
conn.close()
