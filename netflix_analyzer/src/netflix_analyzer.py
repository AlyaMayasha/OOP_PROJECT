from abc import ABC, abstractmethod
from collections import Counter

#ABSTRACT BASE CLASS 

class BaseAnalyzer(ABC):

    def __init__(self, contents):
        self._contents      = contents      
        self._total         = len(contents)
        self._result        = {}            

    @abstractmethod
    def analyze(self):
        pass

    @abstractmethod
    def get_summary(self):
        pass

    def get_result(self):
        return self._result

    def _cetak_header(self, judul):
        print(f"\n  {'═' * 44}")
        print(f"   {judul}")
        print(f"  {'═' * 44}")

    def _cetak_baris(self, label, nilai, lebar=24):
        print(f"  > {label:<{lebar}}: {nilai}")

    def __str__(self):
        return f"{self.__class__.__name__} | {self._total} konten dianalisis"


#CLASS UTAMA

class NetflixAnalyzer(BaseAnalyzer):
    
    def __init__(self, contents):
        super().__init__(contents)          
        self.__contents_data = contents     
        self.total_contents  = len(contents)

    def analyze(self):
        self._result = {
            'top_rated'    : self.get_top_rated(5),
            'most_viewed'  : self.get_most_viewed(5),
            'avg_imdb'     : self._hitung_rata_imdb(),
            'high_rated'   : len([c for c in self.__contents_data if c.is_high_rated()]),
            'popular'      : len([c for c in self.__contents_data if c.is_popular()]),
        }
        return self._result

    def get_summary(self):
        if not self._result:
            self.analyze()

        self._cetak_header("STATISTIK UMUM DATASET")
        self._cetak_baris("Total Konten", f"{self.total_contents} data")
        self._cetak_baris("Rating IMDb Rata-rata", f"{self._result['avg_imdb']:.2f}")
        self._cetak_baris("Konten Rating Tinggi (>8)", f"{self._result['high_rated']} konten")
        self._cetak_baris("Konten Populer (>10jt)", f"{self._result['popular']} konten")

        print(f"\n  --- Top 3 Konten Rating Tertinggi ---")
        for i, c in enumerate(self._result['top_rated'][:3], 1):
            print(f"  {i}. [{c.imdb_rating}] {c.title} ({c.year})")

        print(f"\n  --- Top 3 Konten Paling Ditonton ---")
        for i, c in enumerate(self._result['most_viewed'][:3], 1):
            print(f"  {i}. {c.title} — {c.viewership}")


    def get_top_rated(self, n=10):
        return sorted(
            self.__contents_data,
            key=lambda c: c.imdb_rating,
            reverse=True
        )[:n]

    def get_most_viewed(self, n=10):
        return sorted(
            self.__contents_data,
            key=lambda c: c.get_viewership_number(),
            reverse=True
        )[:n]

    def analyze_genre_distribution(self):
        return Counter(c.genre for c in self.__contents_data if c.genre)

    def analyze_country_production(self):
        return Counter(c.country for c in self.__contents_data if c.country)

    def analyze_yearly_trend(self):
        data = Counter(c.year for c in self.__contents_data if c.year > 0)
        return dict(sorted(data.items()))

    def average_imdb_by_genre(self):
        genre_imdb = {}
        for c in self.__contents_data:
            if c.genre and c.imdb_rating > 0:
                if c.genre not in genre_imdb:
                    genre_imdb[c.genre] = []
                genre_imdb[c.genre].append(c.imdb_rating)

        hasil = {g: round(sum(v)/len(v), 2) for g, v in genre_imdb.items()}
        return dict(sorted(hasil.items(), key=lambda x: x[1], reverse=True))

    def _hitung_rata_imdb(self):
        valid = [c.imdb_rating for c in self.__contents_data if c.imdb_rating > 0]
        return round(sum(valid) / len(valid), 2) if valid else 0.0


#SUBCLASS GenreAnalyzer

class GenreAnalyzer(BaseAnalyzer):

    def __init__(self, contents):
        super().__init__(contents)   

    def analyze(self):
        distribusi = Counter(c.genre for c in self._contents if c.genre)
        avg_imdb   = {}

        for c in self._contents:
            if c.genre and c.imdb_rating > 0:
                avg_imdb.setdefault(c.genre, []).append(c.imdb_rating)

        self._result = {
            'distribusi'   : distribusi,
            'top_genre'    : distribusi.most_common(10),
            'avg_imdb'     : {g: round(sum(v)/len(v), 2) for g, v in avg_imdb.items()},
            'total_genre'  : len(distribusi),
        }
        return self._result

    def get_summary(self):
        if not self._result:
            self.analyze()

        self._cetak_header("       ANALISIS GENRE TERPOPULER")

        print(f"\n  Genre paling banyak:")
        for genre, jml in self._result['top_genre'][:7]:
            bar = "█" * min(jml, 20)
            print(f"  > {genre:<25} : {bar} {jml}")

        avg_sorted = sorted(
            self._result['avg_imdb'].items(),
            key=lambda x: x[1], reverse=True
        )
        print(f"\n  Rata-rata IMDb tertinggi per genre:")
        for genre, avg in avg_sorted[:5]:
            print(f"  > {genre:<25} : {avg:.1f}")

        top1 = self._result['top_genre'][0][0] if self._result['top_genre'] else '-'
        print(f"\n  💡 Insight:")
        print(f"     Genre '{top1}' menjadi genre paling dominan di Netflix")
        print(f"     dengan total {self._result['top_genre'][0][1]} konten.")
        print(f"     Dataset mencakup {self._result['total_genre']} genre unik.")


# SUBCLASS IMDbAnalyzer

class IMDbAnalyzer(BaseAnalyzer):

    def __init__(self, contents):
        super().__init__(contents)

    def analyze(self):
        ratings = [c.imdb_rating for c in self._contents if c.imdb_rating > 0]

        if not ratings:
            self._result = {}
            return self._result

        top_rated    = sorted(self._contents, key=lambda c: c.imdb_rating, reverse=True)
        bottom_rated = sorted([c for c in self._contents if c.imdb_rating > 0],
                              key=lambda c: c.imdb_rating)

        #rata-rata per tahun
        per_tahun = {}
        for c in self._contents:
            if c.year > 0 and c.imdb_rating > 0:
                per_tahun.setdefault(c.year, []).append(c.imdb_rating)
        avg_per_tahun = {t: round(sum(v)/len(v), 2) for t, v in per_tahun.items()}

        #distribusi rating (rendah < 7, sedang 7–8, tinggi > 8)
        rendah  = len([r for r in ratings if r < 7.0])
        sedang  = len([r for r in ratings if 7.0 <= r <= 8.0])
        tinggi  = len([r for r in ratings if r > 8.0])

        self._result = {
            'avg_imdb'      : round(sum(ratings) / len(ratings), 2),
            'max_imdb'      : max(ratings),
            'min_imdb'      : min(ratings),
            'top_rated'     : top_rated[:5],
            'bottom_rated'  : bottom_rated[:3],
            'avg_per_tahun' : dict(sorted(avg_per_tahun.items())),
            'distribusi'    : {'rendah': rendah, 'sedang': sedang, 'tinggi': tinggi},
        }
        return self._result

    def get_summary(self):
        if not self._result:
            self.analyze()

        self._cetak_header("          ANALISIS IMDb RATING")
        self._cetak_baris("Rata-rata IMDb", f"{self._result['avg_imdb']:.2f}")
        self._cetak_baris("Rating Tertinggi", f"{self._result['max_imdb']}")
        self._cetak_baris("Rating Terendah", f"{self._result['min_imdb']}")

        dist = self._result['distribusi']
        print(f"\n  Distribusi Rating:")
        print(f"  > Rendah (< 7.0)   : {dist['rendah']} konten")
        print(f"  > Sedang (7.0–8.0) : {dist['sedang']} konten")
        print(f"  > Tinggi (> 8.0)   : {dist['tinggi']} konten")

        print(f"\n  Top 5 Konten Rating Tertinggi:")
        for i, c in enumerate(self._result['top_rated'], 1):
            print(f"  {i}. [{c.imdb_rating}] {c.title} ({c.year}) — {c.country}")

        print(f"\n  Rata-rata IMDb per Tahun:")
        for tahun, avg in self._result['avg_per_tahun'].items():
            bar = "▓" * int(avg)
            print(f"  {tahun} : {bar} {avg:.2f}")

        print(f"\n  💡 Insight:")
        best_year = max(self._result['avg_per_tahun'].items(), key=lambda x: x[1])
        print(f"     Tahun {best_year[0]} memiliki rata-rata IMDb tertinggi ({best_year[1]:.2f}).")


#SUBCLASS CountryAnalyzer 

class CountryAnalyzer(BaseAnalyzer):
  
    def __init__(self, contents):
        super().__init__(contents)

    def analyze(self):
        distribusi = Counter(c.country for c in self._contents if c.country)

        imdb_negara = {}
        for c in self._contents:
            if c.country and c.imdb_rating > 0:
                imdb_negara.setdefault(c.country, []).append(c.imdb_rating)

        avg_imdb = {n: round(sum(v)/len(v), 2) for n, v in imdb_negara.items()}

        self._result = {
            'distribusi'   : distribusi,
            'top_country'  : distribusi.most_common(10),
            'avg_imdb'     : avg_imdb,
            'total_negara' : len(distribusi),
        }
        return self._result

    def get_summary(self):
        if not self._result:
            self.analyze()

        self._cetak_header("        ANALISIS NEGARA PRODUKSI")
        print(f"\n  Negara dengan konten terbanyak:")
        total = self._total
        for negara, jml in self._result['top_country'][:8]:
            persen = round(jml / total * 100, 1) if total > 0 else 0
            bar    = "█" * min(jml // 2, 25)
            print(f"  > {negara:<18} : {bar} {jml} ({persen}%)")

        print(f"\n  Rata-rata IMDb per Negara (min. 2 konten):")
        avg_sorted = sorted(
            [(n, v) for n, v in self._result['avg_imdb'].items()
             if self._result['distribusi'][n] >= 2],
            key=lambda x: x[1], reverse=True
        )
        for negara, avg in avg_sorted[:6]:
            print(f"  > {negara:<18} : {avg:.2f}")

        top1 = self._result['top_country'][0]
        print(f"\n  💡 Insight:")
        print(f"     {top1[0]} mendominasi dengan {top1[1]} konten.")
        print(f"     Dataset mencakup {self._result['total_negara']} negara produksi.")


#SUBCLASS DirectorAnalyzer 

class DirectorAnalyzer(BaseAnalyzer):
    def __init__(self, contents):
        super().__init__(contents)

    def analyze(self):

        #Counter sutradara
        directors = Counter(
            c.director for c in self._contents
            if c.director and c.director.strip() not in ('', '-', 'N/A', 'Unknown')
        )

        #Counter aktor 
        actors_counter = Counter()
        abaikan = ('', '-', 'N/A', 'Unknown', 'Documentary')

        for c in self._contents:
            if c.lead_actor:
                for aktor in c.lead_actor.split(','):
                    aktor = aktor.strip()
                    if aktor not in abaikan and aktor.lower() != 'documentary':
                        actors_counter[aktor] += 1

        #IMDb rata-rata per sutradara
        imdb_dir = {}
        for c in self._contents:
            if c.director and c.imdb_rating > 0 and c.director not in abaikan:
                imdb_dir.setdefault(c.director, []).append(c.imdb_rating)
        avg_imdb_dir = {d: round(sum(v)/len(v), 2) for d, v in imdb_dir.items()}

        self._result = {
            'top_director'    : directors.most_common(10),
            'top_actor'       : actors_counter.most_common(10),
            'avg_imdb_dir'    : avg_imdb_dir,
            'total_director'  : len(directors),
            'total_actor'     : len(actors_counter),
        }
        return self._result

    def get_summary(self):
        if not self._result:
            self.analyze()

        self._cetak_header("    ANALISIS TOP DIRECTOR & LEAD ACTOR")

        print(f"\n  Top Sutradara Paling Produktif:")
        for i, (dir_name, jml) in enumerate(self._result['top_director'][:7], 1):
            avg = self._result['avg_imdb_dir'].get(dir_name, 0)
            print(f"  {i}. {dir_name:<30} {jml} konten | IMDb avg: {avg:.1f}")

        print(f"\n  Top Aktor / Pemeran Paling Sering Muncul:")
        for i, (aktor, jml) in enumerate(self._result['top_actor'][:7], 1):
            print(f"  {i}. {aktor:<30} {jml}x muncul")

        print(f"\n  💡 Insight:")
        top_dir   = self._result['top_director'][0] if self._result['top_director'] else ('-', 0)
        top_actor = self._result['top_actor'][0] if self._result['top_actor'] else ('-', 0)
        print(f"     Sutradara paling produktif: {top_dir[0]} ({top_dir[1]} konten)")
        print(f"     Aktor paling sering muncul: {top_actor[0]} ({top_actor[1]}x)")
