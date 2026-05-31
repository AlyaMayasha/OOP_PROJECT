import matplotlib.pyplot as plt
from collections import Counter

class VisualizationManager:
    def __init__(self, contents):
        self.contents = contents

    def plot_imdb_trend(self):
        #Kumpulkan rating berdasarkan tahun
        year_ratings = {}
        for c in self.contents:
            if c.year > 0 and c.imdb_rating > 0:
                year_ratings.setdefault(c.year, []).append(c.imdb_rating)
        
        #Hitung rata-rata
        avg_per_year = {y: sum(r)/len(r) for y, r in year_ratings.items()}
        
        #Urutkan dari tahun terlama ke terbaru
        tahun = sorted(avg_per_year.keys())
        rata_rata = [avg_per_year[t] for t in tahun]

        plt.figure(figsize=(10, 5))
        plt.plot(tahun, rata_rata, color='#3498DB', linewidth=3, marker='o', markersize=8)
        
        plt.title("Tren Rata-Rata Rating IMDb Netflix (2016-2025)", fontsize=14, pad=15)
        plt.xlabel("Tahun")
        plt.ylabel("Rata-Rata Rating")
        plt.xticks(tahun)
        plt.grid(axis='both', linestyle='--', alpha=0.5)
        
        for x, y in zip(tahun, rata_rata):
            plt.text(x, y + 0.05, f"{y:.1f}", ha='center', fontsize=9)

        plt.tight_layout()
        plt.show()

    def plot_top_countries(self):

        countries = [c.country for c in self.contents if c.country not in ('', '-', 'Unknown')]
        count_country = Counter(countries).most_common(10)
        
        negara = [item[0] for item in reversed(count_country)]
        jumlah = [item[1] for item in reversed(count_country)]

        plt.figure(figsize=(10, 6))
        
        warna = ['#E50914' if i == len(jumlah)-1 else '#555555' for i in range(len(jumlah))]
        
        bars = plt.barh(negara, jumlah, color=warna)
        
        plt.title("Top 10 Negara Produksi Konten Netflix", fontsize=14, pad=15)
        plt.xlabel("Total Konten")
        
        for bar, val in zip(bars, jumlah):
            plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                     str(val), va='center', fontsize=10)

        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()