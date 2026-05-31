# 🎬 Netflix Global Content Insights System (2016-2025)

Program berbasis *Command Line Interface* (CLI) yang dirancang untuk membaca, memproses, menganalisis, dan memvisualisasikan dataset tayangan Netflix dari tahun 2016 hingga 2025. Program ini dibangun menggunakan bahasa pemrograman Python dengan menerapkan prinsip-prinsip Pemrograman Berorientasi Objek (OOP) secara komprehensif.

---

## 🏗️ Arsitektur & Konsep Program

Program ini mengadopsi arsitektur **Modular & Separation of Concerns (SoC)**, di mana setiap file memiliki satu tanggung jawab utama. Pendekatan desain yang digunakan meliputi:

1. **Model (`netflix_content.py`)**: Bertugas mendefinisikan bentuk data (blueprint) beserta aturan validasinya.
2. **Repository Pattern (`netflix_repository.py`)**: Bertindak sebagai jembatan antara program dan sumber data mentah (CSV). Mengisolasi logika pembacaan, pembersihan (*data cleansing*), dan penyimpanan ke memori.
3. **Analyzer (`netflix_analyzer.py`)**: Berisi logika bisnis (*Business Logic*). Mengambil data dari memori dan melakukan agregasi, filtering, serta perhitungan statistik.
4. **View/UI (`main.py` & `visualization_manager.py`)**: Berfungsi sebagai antarmuka interaktif yang menghubungkan input pengguna dengan output program, baik dalam bentuk teks terminal maupun grafik Matplotlib.

---

## 📂 Struktur Direktori

```text
📁 netflix-insights/
├── 📄 main.py                      # Entry point & sistem menu interaktif
├── 📁 data/
│   └── 📄 01_Netflix_2016_2025.csv # Dataset mentah
└── 📁 src/
    ├── 📄 __init__.py              # Package initializer
    ├── 📄 netflix_content.py       # Representasi data (Class Model)
    ├── 📄 netflix_repository.py    # Logika akses & pembersihan data
    ├── 📄 netflix_analyzer.py      # Core logic & kalkulasi statistik
    └── 📄 visualization_manager.py # Modul pembuatan grafik Matplotlib
```

---

# 🚀 Penerapan Modul Pemrograman Berorientasi Objek (PBO)

Program ini mengimplementasikan konsep-konsep kunci OOP sebagai berikut:

## 1. Class, Object, Atribut, & Method (Materi 02)

Diterapkan di seluruh arsitektur program.

**Contoh:** Pada `netflix_content.py`, `NetflixContent` adalah sebuah *Class* (blueprint). Setiap baris data dari file CSV yang berhasil dibaca kemudian diinstansiasi menjadi sebuah *Object*. Variabel seperti `title`, `genre`, dan `country` adalah *Atribut*, sedangkan fungsi seperti `is_popular()` dan `get_content_age()` adalah *Method*.

---

## 2. Enkapsulasi & Validasi (Materi 04)

Digunakan untuk melindungi integritas data dari modifikasi yang tidak disengaja atau tidak valid.

**Contoh:** Pada `NetflixContent`, atribut sensitif dibuat *private* (seperti `__year`, `__imdb_rating`, dan `__viewership_raw`). Akses dan perubahannya diatur ketat menggunakan Decorator `@property` (*Getter*) dan `@<attr>.setter` (*Setter*). Terdapat logika validasi, misalnya rating IMDb tidak boleh kurang dari 0 atau lebih dari 10.

---

## 3. Pewarisan / Inheritance (Materi 06)

Digunakan untuk menghindari duplikasi kode (*DRY - Don't Repeat Yourself*).

**Contoh:** Pada `netflix_analyzer.py`, dibuat sebuah *superclass* bernama `BaseAnalyzer`. Class analisis spesifik seperti `GenreAnalyzer`, `IMDbAnalyzer`, dan `CountryAnalyzer` mewarisi properti bawaan (`self._contents`, `self._result`) dan method helper (`_cetak_header()`) dari class induk menggunakan fungsi `super().__init__()`.

---

## 4. Polimorfisme (Materi 07)

Memungkinkan method yang memiliki nama sama untuk menghasilkan perilaku (*behavior*) yang berbeda tergantung pada class yang mengeksekusinya.

**Contoh:** Terdapat method `analyze()` dan `get_summary()`. Saat dipanggil dari objek `GenreAnalyzer`, program akan mencetak data distribusi genre. Namun, jika dipanggil dari `DirectorAnalyzer`, program secara polimorfik akan mencetak sutradara dan aktor paling produktif.

---

## 5. Abstraksi (Materi 08)

Digunakan untuk membuat "kerangka" atau "kontrak" yang memaksa subclass untuk mengimplementasikan method tertentu.

**Contoh:** `BaseAnalyzer` meng-*inherit* modul `ABC` (*Abstract Base Class*) dari Python. Method `analyze()` dan `get_summary()` diberikan decorator `@abstractmethod`. Ini mencegah `BaseAnalyzer` untuk diinstansiasi secara langsung dan memastikan setiap class analyzer turunan pasti memiliki fungsionalitas analisis dan ringkasan.

---

## 6. Dunder / Magic Methods (Materi 09)

Mengubah perilaku built-in dari bahasa Python terhadap objek yang kita buat.

**Contoh:**

* `__str__` dan `__repr__` di-*override* untuk memberikan format cetak yang rapi saat objek di-*print*.
* `__eq__` (*Equal*) memungkinkan kita membandingkan apakah dua objek konten itu sama berdasarkan judulnya.
* `__lt__` (*Less Than*) di-*override* agar kumpulan objek `NetflixContent` bisa dengan mudah di-*sorting* secara otomatis berdasarkan rating IMDb menggunakan fungsi bawaan Python `sorted()`.

---

# 🛠️ Fitur Utama Program

### 📊 Statistik Umum

Menampilkan rangkuman dataset (total data, rating rata-rata, dll).

### 🔍 Deep-Dive Analysis

Menganalisis topologi data berdasarkan Genre, Rating IMDb, Sutradara, Aktor, hingga metrik unit Viewership.

### 🧹 Data Cleansing

Secara otomatis membersihkan *malformed row* (baris rusak akibat penulisan *double quotes* berlebih pada file CSV) dan menormalisasi satuan penonton (*Minutes* dikonversi menjadi *Hours* agar akurat).

### 📈 Visualisasi Interaktif (Matplotlib)

Menampilkan *Line Chart* (Tren Kualitas/Rating per Tahun) dan *Horizontal Bar Chart* (Top Negara Produksi).

### 🎯 Mesin Pencari & Filter

Mencari film berdasarkan kata kunci judul dan memfilter kumpulan film berdasarkan genre, negara, rilis, maupun batas rating tinggi.

---


