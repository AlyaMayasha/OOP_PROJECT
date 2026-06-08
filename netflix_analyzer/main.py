import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.netflix_repository    import NetflixRepository
from src.netflix_analyzer      import (
    NetflixAnalyzer,
    GenreAnalyzer,
    IMDbAnalyzer,
    CountryAnalyzer,
    DirectorAnalyzer,
)
from src.visualization_manager import VisualizationManager

DATASET_PATH = os.path.join("data", "01_Netflix_2016_2025.csv")
OUTPUT_DIR   = "output"

def cetak_logo():
    print("\n" + "═" * 48)
    print("   🎬 NETFLIX GLOBAL CONTENT INSIGHTS SYSTEM")
    print("     Pemrograman Berorientasi Objek — Python")
    print("═" * 48)


def cetak_menu():
    print("\n  ┌=============================================┐")
    print("  │                    MENU                     │")
    print("  ├=============================================┤")
    print("  │  [1]  Tampilkan Statistik Umum              │")
    print("  │  [2]  Analisis Genre Terpopuler             │")
    print("  │  [3]  Analisis IMDb Rating                  │")
    print("  │  [4]  Analisis Viewership                   │")
    print("  │  [5]  Top Director & Lead Actor             │")
    print("  │  [6]  Visualisasi Tren Rating & Asal Negara │")
    print("  │  [7]  Cari Konten                           │")
    print("  │  [8]  Filter Konten                         │")
    print("  │  [0]  Keluar                                │")
    print("  └─────────────────────────────────────────────┘")

    
def input_pilihan(prompt="  Pilih menu (0-8): "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        return "0"


def jeda():
    input("\n  [Tekan ENTER untuk lanjut...]")


def menu_statistik_umum(repo, analyzer):
    print("\n" + "=" * 56)
    print("            STATISTIK UMUM DATASET NETFLIX")
    print("=" * 56)

    year_min, year_max = repo.get_year_range()
    analyzer.analyze()
    hasil = analyzer.get_result()

    print(f"\n  Dataset            : {os.path.basename(DATASET_PATH)}")
    print(f"  Total Konten       : {repo.get_total()} data")
    print(f"  Rentang Tahun      : {year_min} – {year_max}")
    print(f"  Rata-rata IMDb     : {hasil['avg_imdb']:.2f}")
    print(f"  Konten Rating >8.0 : {hasil['high_rated']} konten")
    print(f"  Konten Populer     : {hasil['popular']} konten")

    print(f"\n  --- 5 Konten Rating IMDb Tertinggi ---")
    for i, c in enumerate(hasil['top_rated'], 1):
        print(f"  {i}. [{c.imdb_rating:4.1f}] {c.title} ({c.year}) — {c.country}")

    print(f"\n  --- 5 Konten Paling Ditonton ---")
    for i, c in enumerate(hasil['most_viewed'], 1):
        print(f"  {i}. {c.title[:35]:<35} {c.viewership}")

    jeda()


def menu_genre(contents):
    g_analyzer = GenreAnalyzer(contents)   
    g_analyzer.analyze()
    g_analyzer.get_summary()
    jeda()


def menu_imdb(contents):
    imdb_analyzer = IMDbAnalyzer(contents)
    imdb_analyzer.analyze()
    imdb_analyzer.get_summary()
    jeda()


def menu_viewership(analyzer, contents):
    print("\n" + "=" * 60)
    print("                   ANALISIS VIEWERSHIP")
    print("=" * 60)

    top = analyzer.get_most_viewed(10)
    if not top:
        print("\n  Tidak ada data viewership.")
        jeda()
        return

    print(f"\n  Top 10 Konten Paling Banyak Ditonton:\n")
    for i, c in enumerate(top, 1):
        num = c.get_viewership_number()
        unit = c.get_viewership_unit()
        if num >= 1_000_000_000:
            tampil = f"{num/1_000_000_000:.2f}B {unit}"
        elif num >= 1_000_000:
            tampil = f"{num/1_000_000:.1f}M {unit}"
        else:
            tampil = c.viewership
        print(f"  {i:2}. {c.title[:40]:<40} {tampil}")

    jeda()


def menu_director(contents):
    d_analyzer = DirectorAnalyzer(contents)
    d_analyzer.analyze()
    d_analyzer.get_summary()
    jeda()


def menu_visualisasi(analyzer, contents):
    c_analyzer = CountryAnalyzer(contents)
    c_analyzer.get_summary()

    print("  Menyiapkan grafik... (Tutup grafik pertama untuk melihat yang kedua)")

    viz = VisualizationManager(contents)
    viz.plot_imdb_trend()
    viz.plot_top_countries()

    jeda()


def menu_cari(repo):
    print("\n" + "=" * 50)
    print("               CARI KONTEN NETFLIX")
    print("=" * 50)

    keyword = input("\n  Masukkan kata kunci judul: ").strip()
    if not keyword:
        print("  Kata kunci tidak boleh kosong.")
        jeda()
        return

    hasil = repo.search_by_title(keyword)
    if not hasil:
        print(f"\n  Tidak ditemukan konten dengan kata kunci: '{keyword}'")
    else:
        print(f"\n  Ditemukan {len(hasil)} konten:\n")
        for c in hasil[:10]:
            print(f"  • {c}")

        if len(hasil) == 1:
            tampil = input("\n  Tampilkan detail? (y/n): ").strip().lower()
            if tampil == 'y':
                hasil[0].display_info()

    jeda()


def menu_filter(repo):
    print("\n" + "=" * 50)
    print("              FILTER KONTEN NETFLIX")
    print("=" * 50)
    print("\n  Filter berdasarkan:")
    print("  [1] Genre")
    print("  [2] Negara")
    print("  [3] Tahun")
    print("  [4] Rating Tinggi (IMDb > 8.0)")

    pilihan = input_pilihan("  Pilih (1-4): ")

    if pilihan == '1':
        keyword = input("  Masukkan genre: ").strip()
        hasil   = repo.filter_by_genre(keyword)
        label   = f"genre '{keyword}'"
    elif pilihan == '2':
        keyword = input("  Masukkan negara: ").strip()
        hasil   = repo.filter_by_country(keyword)
        label   = f"negara '{keyword}'"
    elif pilihan == '3':
        try:
            tahun = int(input("  Masukkan tahun (2016-2025): ").strip())
            hasil = repo.filter_by_year(tahun)
            label = f"tahun {tahun}"
        except ValueError:
            print("  Input tahun tidak valid.")
            jeda()
            return
    elif pilihan == '4':
        hasil = repo.filter_high_rated()
        label = "rating IMDb > 8.0"
    else:
        print("  Pilihan tidak valid.")
        jeda()
        return

    print(f"\n  Ditemukan {len(hasil)} konten dengan {label}:\n")
    
    for c in hasil:
        print(f"  • [{c.year}] {c.title} | IMDb: {c.imdb_rating} | {c.country}")

    jeda()

def main():
    cetak_logo()
    print(f"\n  Memuat dataset...")
    try:
        repo = NetflixRepository(DATASET_PATH)
    except FileNotFoundError as e:
        print(f"\n   1 ERROR: {e}")
        sys.exit(1)

    contents = repo.get_all_contents()
    analyzer = NetflixAnalyzer(contents)
    year_min, year_max = repo.get_year_range()

    print(f"\n  Dataset berhasil dimuat:")
    print(f"  > Total Content  : {repo.get_total()} Data")
    print(f"  > Tahun Dataset  : {year_min} - {year_max}")
    print(f"  > Sumber File    : {DATASET_PATH}")

    while True:
        cetak_menu()
        pilihan = input_pilihan()

        if pilihan == '1':
            menu_statistik_umum(repo, analyzer)

        elif pilihan == '2':
            menu_genre(contents)

        elif pilihan == '3':
            menu_imdb(contents)

        elif pilihan == '4':
            menu_viewership(analyzer, contents)

        elif pilihan == '5':
            menu_director(contents)

        elif pilihan == '6':
            menu_visualisasi(analyzer, contents)

        elif pilihan == '7':
            menu_cari(repo)

        elif pilihan == '8':
            menu_filter(repo)

        elif pilihan == '0':
            print("\n  Terima kasih telah menggunakan Netflix Insights System! 🎬")
            print("  Sampai jumpa!\n")
            break

        else:
            print("\n    Pilihan tidak valid. Masukkan angka 0-8.")


if __name__ == "__main__":
    main()
