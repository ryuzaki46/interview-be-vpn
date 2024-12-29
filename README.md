# Take Home Test Interview
### Tata Cara Pengerjaan soal
- clone repository template ini kedalam repository github pribadi anda.
- submit jawaban / hasil dengan push ke repository yang telah anda buat sebelumnya sebagai public access repo.
- kirimkan link repo anda ke email jefri.arbi+be_candidate@noble-software.com
- pengerjaan dalam waktu < 7 hari mendapatkan poin ekstra
  
## Soal 1: Django + gRPC Integration

### Deskripsi:
Anda sedang mengembangkan aplikasi Django yang berfungsi sebagai REST API, namun sekarang klien meminta untuk menambahkan dukungan gRPC untuk komunikasi antar layanan di dalam aplikasi yang sama.

### Tugas:
1. Buat sebuah gRPC server sederhana menggunakan Django yang dapat menerima permintaan gRPC untuk mengambil daftar pengguna (User) dari database.
2. Konfigurasi aplikasi agar dapat berjalan dengan Uvicorn dan mendukung gRPC serta HTTP REST API secara bersamaan.
3. Gunakan file `.proto` yang disertakan untuk mendefinisikan skema data gRPC Anda.

### Kriteria Penilaian:
- Struktur proyek
- Kemampuan untuk mengintegrasikan gRPC dan Django
- Cara Anda menangani server untuk gRPC dan REST API secara bersamaan
- Efisiensi dan dokumentasi yang jelas

**Bonus**: Jika aplikasi berhasil dijalankan dengan reverse proxy menggunakan Nginx untuk mengarahkan HTTP/1.1 ke Django dan HTTP/2 ke gRPC.

---

## Soal 2: Implementasi Single Sign-On (SSO)

### Deskripsi:
Anda memiliki tiga proyek terpisah menggunakan Django REST Framework dengan JWT sebagai metode autentikasi. Klien ingin mengimplementasikan sistem Single Sign-On (SSO) yang memungkinkan pengguna login sekali dan mengakses ketiga aplikasi tersebut.

### Tugas:
1. Implementasikan sistem SSO untuk ketiga aplikasi Django tersebut.
2. Sistem SSO harus mendukung JWT dan setiap aplikasi harus dapat melakukan validasi token yang dihasilkan oleh sistem SSO.
3. Gunakan secret key dari masing-masing aplikasi Django untuk memverifikasi JWT pada SSO.

### Kriteria Penilaian:
- Penggunaan JWT dalam SSO
- Validasi dan keamanan token
- Struktur dan pengaturan kode
- Penjelasan singkat tentang arsitektur yang dipilih

**Bonus**: Tambahkan dukungan untuk logout global sehingga semua sesi pada aplikasi terhubung bisa ditutup secara bersamaan.

---

## Soal 3: Custom Password Hashing with Unified Secret Key

### Deskripsi:
Anda memiliki beberapa proyek Django dengan secret key yang berbeda. Anda ingin membuat sebuah SSO yang memungkinkan Anda melakukan validasi password dari semua aplikasi menggunakan unified secret key.

### Tugas:
1. Buat sebuah kelas `CustomPBKDF2PasswordHasher` yang menggunakan secret key dari masing-masing proyek untuk melakukan hash dan check password.
2. Implementasikan sebuah fungsi dalam SSO yang dapat memvalidasi password dari berbagai aplikasi yang menggunakan key yang berbeda.
3. Berikan penjelasan bagaimana cara kerja hash password dan alasan penggunaan `PBKDF2` pada sistem Anda.

### Kriteria Penilaian:
- Implementasi dari `CustomPBKDF2PasswordHasher`
- Fungsi validasi password
- Penjelasan tentang keamanan hash password

**Bonus**: Jelaskan secara singkat tentang alternatif algoritma hashing dan kapan kita perlu menggantinya.

---
