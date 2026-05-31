import re
from datetime import datetime


class NetflixContent:
    
    #Class attribute 
    CURRENT_YEAR = datetime.now().year
    HIGH_RATING_THRESHOLD = 8.0   

    #Konstruktor 
    def __init__(self, title, genre, country, director, lead_actor,
                 release_date, year, duration, imdb_rating, viewership):
        
        #Atribut public
        self.title        = str(title).strip()
        self.genre        = str(genre).strip()
        self.country      = str(country).strip()
        self.director     = str(director).strip()
        self.lead_actor   = str(lead_actor).strip()
        self.release_date = str(release_date).strip()
        self.duration     = str(duration).strip()

        #Atribut dengan validasi 
        self.__year           = 0
        self.__imdb_rating    = 0.0
        self.__viewership_raw = ""

        self.year         = year          
        self.imdb_rating  = imdb_rating  
        self.viewership   = viewership   

    #Property & Setter

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, nilai):
        try:
            nilai = int(nilai)
            if nilai < 1900 or nilai > self.CURRENT_YEAR + 1:
                raise ValueError
            self.__year = nilai
        except (ValueError, TypeError):
            self.__year = 0   

    @property
    def imdb_rating(self):
        return self.__imdb_rating

    @imdb_rating.setter
    def imdb_rating(self, nilai):
        """Setter: validasi IMDb harus float 0–10."""
        try:
            nilai = float(nilai)
            if not (0.0 <= nilai <= 10.0):
                raise ValueError
            self.__imdb_rating = round(nilai, 1)
        except (ValueError, TypeError):
            self.__imdb_rating = 0.0   

    @property
    def viewership(self):
        return self.__viewership_raw

    @viewership.setter
    def viewership(self, nilai):
        self.__viewership_raw = str(nilai).strip()

    #Method Helper

    def get_viewership_number(self):
        v = self.__viewership_raw
        match = re.search(r'([\d.]+)\s*([MBKmb]?)', v)
        if not match:
            return 0.0
        angka = float(match.group(1))
        satuan = match.group(2).upper()
        pengali = {'M': 1_000_000, 'B': 1_000_000_000, 'K': 1_000}
        
        total_angka = angka * pengali.get(satuan, 1)
        
        #Normalisasi Konversi Minutes menjadi Hours
       
        if 'minute' in v.lower():
            total_angka = total_angka / 60
            
        return total_angka

    def get_viewership_unit(self):
        v = self.__viewership_raw
        for unit in ['Streams', 'Hours', 'Views', 'Minutes']:
            if unit.lower() in v.lower():
                return unit.capitalize()
        return '-'

    #Method Utama 

    def is_high_rated(self):
        return self.__imdb_rating > self.HIGH_RATING_THRESHOLD

    def is_popular(self):
        return self.get_viewership_number() > 10_000_000

    def get_content_age(self):
        if self.__year == 0:
            return -1
        return self.CURRENT_YEAR - self.__year

    def display_info(self):
        garis = "─" * 52
        bintang = "★" * int(self.__imdb_rating) + "☆" * (10 - int(self.__imdb_rating))
        print(f"\n  {garis}")
        print(f"  🎬 {self.title}")
        print(f"  {garis}")
        print(f"  Genre       : {self.genre}")
        print(f"  Negara      : {self.country}")
        print(f"  Sutradara   : {self.director}")
        print(f"  Pemeran     : {self.lead_actor}")
        print(f"  Rilis       : {self.release_date} ({self.__year})")
        print(f"  Durasi      : {self.duration}")
        print(f"  IMDb Rating : {self.__imdb_rating} {bintang[:5]}")
        print(f"  Viewership  : {self.__viewership_raw}")
        print(f"  Umur Konten : {self.get_content_age()} tahun")
        print(f"  Rating Tinggi? : {'Ya' if self.is_high_rated() else 'Tidak'}")
        print(f"  Populer?       : {'Ya' if self.is_popular() else 'Tidak'}")
        print(f"  {garis}")

    #Dunder Methods 

    def __str__(self):
        return f"[{self.__year}] {self.title} | {self.genre} | IMDb: {self.__imdb_rating}"

    def __repr__(self):
        return (f"NetflixContent(title='{self.title}', year={self.__year}, "
                f"imdb={self.__imdb_rating}, country='{self.country}')")

    def __eq__(self, other):
        if not isinstance(other, NetflixContent):
            return False
        return self.title.lower() == other.title.lower()

    def __lt__(self, other):
        return self.__imdb_rating < other.imdb_rating