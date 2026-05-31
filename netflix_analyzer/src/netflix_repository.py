import os
import csv
from src.netflix_content import NetflixContent


class NetflixRepository:

    def __init__(self, filepath):

        self.__filepath = filepath
        self.__contents = []
        self.__is_loaded = False

        self.load_data()

    #LOAD DATASET
    def load_data(self):

        #VALIDASI FILE
        if not os.path.exists(self.__filepath):

            raise FileNotFoundError(
                f"File dataset tidak ditemukan: {self.__filepath}"
            )

        self.__contents = []

        berhasil = 0
        gagal = 0

        #MEMBACA FILE CSV
        with open(
            self.__filepath,
            mode='r',
            encoding='latin-1',
            errors='ignore',
            newline=''
        ) as file:

            #PRE-PROCESSING 
            lines = file.readlines()
            cleaned_lines = []

            for line in lines:
                if line.startswith('"') and '";' in line:
                    line = line[1:] 
                    line = line.replace('";', ';', 1) 
                    line = line.replace('""', '"') 
                cleaned_lines.append(line)

            #PARSING
            reader = csv.reader(cleaned_lines)
            next(reader, None)

            for row in reader:

                try:

                    if not row:
                        continue

                    #MEMBERSIHKAN DATA
                    row = [
                        str(item)
                        .replace('""', '"')
                        .strip()
                        for item in row
                    ]

                    #VALIDASI MINIMAL KOLOM
                    if len(row) < 10:
                        gagal += 1
                        continue

                    #FORMAT DASAR DATASET
                    year = row[0]
                    title = row[1]
                    imdb = row[2]
                    viewership = row[3]
                    director = row[4]

                    #GABUNG SEMUA ACTOR
                    lead_actor = ", ".join(row[5:-4])

                    #DATA AKHIR
                    release_date = row[-4]
                    duration = row[-3]
                    country = row[-2]
                    genre = row[-1]

                    #DEFAULT VALUE
                    if lead_actor.strip() == "":
                        lead_actor = "Unknown"

                    if director.strip() == "":
                        director = "Unknown"

                    if genre.strip() == "":
                        genre = "Unknown"

                    if country.strip() == "":
                        country = "Unknown"

                    #MEMBUAT OBJECT
                    content = NetflixContent(
                        title=title,
                        genre=genre,
                        country=country,
                        director=director,
                        lead_actor=lead_actor,
                        release_date=release_date,
                        year=year,
                        duration=duration,
                        imdb_rating=imdb,
                        viewership=viewership
                    )

                    #SIMPAN KE LIST
                    self.__contents.append(content)
                    berhasil += 1

                except Exception as e:
                    gagal += 1
                    print("\n[WARNING] Data gagal diproses:")
                    print(e)

        #STATUS
        self.__is_loaded = True

    #GETTERS & FILTER METHODS 
    def get_all_contents(self):
        return list(self.__contents)

    def get_total(self):
        return len(self.__contents)

    def get_year_range(self):
        if not self.__contents:
            return (0, 0)
        years = [content.year for content in self.__contents if content.year != 0]
        if not years:
            return (0, 0)
        return (min(years), max(years))

    def filter_by_genre(self, keyword):
        keyword = keyword.lower().strip()
        return [content for content in self.__contents if keyword in content.genre.lower()]

    def filter_by_country(self, country):
        country = country.lower().strip()
        return [content for content in self.__contents if country in content.country.lower()]

    def filter_by_year(self, year):
        return [content for content in self.__contents if content.year == int(year)]

    def search_by_title(self, keyword):
        keyword = keyword.lower().strip()
        return [content for content in self.__contents if keyword in content.title.lower()]

    def filter_high_rated(self):
        return [content for content in self.__contents if content.is_high_rated()]

    def __len__(self):
        return len(self.__contents)

    def __iter__(self):
        return iter(self.__contents)

    def __str__(self):
        min_year, max_year = self.get_year_range()
        return (
            f"NetflixRepository | "
            f"{len(self.__contents)} contents | "
            f"{min_year}-{max_year}"
        )