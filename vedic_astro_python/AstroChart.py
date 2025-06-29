#from jhora.utils import julian_day_number
#from jhora.horoscope.chart.charts import rasi_chart, navamsa_chart
#import jhora.const as const
#import jhora.panchanga.drik as drik
#from jhora.panchanga.drik import Place
from vedicastro.VedicAstro import VedicHoroscopeData
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import pandas as pd
import numpy as np
import swisseph as swe
import os

# путь к ephe файлам
ETHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "ephe"))

# API keys
#TIMEZONEDB_API_KEY = "TZBRMOGUBS9J"

# === Основные объекты ===

planet_map = {
    "Sun": "Солнце", "Moon": "Луна", "Mars": "Марс", "Mercury": "Меркурий", "Jupiter": "Юпитер",
    "Venus": "Венера", "Saturn": "Сатурн", "Rahu": "Раху", "Ketu": "Кету",
    "Uranus": "Уран", "Neptune": "Нептун", "Pluto": "Плутон", "Chiron": "Хирон",
    "Asc": "Асцендент", "Syzygy": "Сизигия"
}

sign_map = {
    "Aries": "Овен", "Taurus": "Телец", "Gemini": "Близнецы", "Cancer": "Рак",
    "Leo": "Лев", "Virgo": "Дева", "Libra": "Весы", "Scorpio": "Скорпион",
    "Sagittarius": "Стрелец", "Capricorn": "Козерог", "Aquarius": "Водолей", "Pisces": "Рыбы"
}

nakshatra_map = {
    "Ashwini": "Ашвини", "Bharani": "Бхарани", "Krittika": "Криттика", "Rohini": "Рохини",
    "Mrigashīrsha": "Мригашира", "Ardra": "Ардра", "Punarvasu": "Пунарвасу",
    "Pushya": "Пушья", "Āshleshā": "Ашлеша", "Maghā": "Магха", "PūrvaPhalgunī": "Пурва Пхалгуни",
    "UttaraPhalgunī": "Уттара Пхалгуни", "Hasta": "Хаста", "Chitra": "Читра",
    "Svati": "Свати", "Vishakha": "Вишакха", "Anuradha": "Анурадха", "Jyeshtha": "Джьештха",
    "Mula": "Мула", "PurvaAshadha": "Пурва Ашадха", "UttaraAshadha": "Уттара Ашадха",
    "Shravana": "Шравана", "Dhanishta": "Дхаништха", "Shatabhisha": "Шатабхиша",
    "PurvaBhādrapadā": "Пурва Бхадрапада", "UttaraBhādrapadā": "Уттара Бхадрапада",
    "Revati": "Ревати"
}

main_grahas = [
    "Асцендент", "Солнце", "Луна", "Марс", "Меркурий",
    "Юпитер", "Венера", "Сатурн", "Раху", "Кету"
]

rasi_order = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион",
              "Стрелец", "Козерог", "Водолей", "Рыбы"]

sign_lords = {
    "Овен": "Марс", "Телец": "Венера", "Близнецы": "Меркурий", "Рак": "Луна",
    "Лев": "Солнце", "Дева": "Меркурий", "Весы": "Венера", "Скорпион": "Марс",
    "Стрелец": "Юпитер", "Козерог": "Сатурн", "Водолей": "Сатурн", "Рыбы": "Юпитер"
}

sign_order = {
    "Овен": 0, "Телец": 1, "Близнецы": 2, "Рак": 3,
    "Лев": 4, "Дева": 5, "Весы": 6, "Скорпион": 7,
    "Стрелец": 8, "Козерог": 9, "Водолей": 10, "Рыбы": 11
}

D1_TO_D9_MAP = {
    "Овен":      ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец"],
    "Телец":     ["Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева"],
    "Близнецы":  ["Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы"],
    "Рак":       ["Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"],
    "Лев":       ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец"],
    "Дева":      ["Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева"],
    "Весы":      ["Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы"],
    "Скорпион":  ["Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"],
    "Стрелец":   ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец"],
    "Козерог":   ["Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева"],
    "Водолей":   ["Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы"],
    "Рыбы":      ["Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
}

natural_relationships = {
    "Солнце": {
        "friends": ["Луна", "Марс", "Юпитер"],
        "enemies": ["Сатурн", "Венера"],
        "neutrals": ["Меркурий"]
    },
    "Луна": {
        "friends": ["Солнце", "Меркурий"],
        "enemies": [],
        "neutrals": ["Марс", "Юпитер", "Венера", "Сатурн"]
    },
    "Марс": {
        "friends": ["Солнце", "Луна", "Юпитер"],
        "enemies": ["Меркурий"],
        "neutrals": ["Сатурн", "Венера"]
    },
    "Меркурий": {
        "friends": ["Солнце", "Венера"],
        "enemies": ["Луна"],
        "neutrals": ["Марс", "Юпитер", "Сатурн"]
    },
    "Юпитер": {
        "friends": ["Солнце", "Луна", "Марс"],
        "enemies": ["Венера", "Меркурий"],
        "neutrals": ["Сатурн"]
    },
    "Венера": {
        "friends": ["Сатурн", "Меркурий"],
        "enemies": ["Солнце", "Луна"],
        "neutrals": ["Марс", "Юпитер"]
    },
    "Сатурн": {
        "friends": ["Венера", "Меркурий"],
        "enemies": ["Солнце", "Луна", "Марс"],
        "neutrals": ["Юпитер"]
    }
}

planet_sign_strengths = {
    "Солнце": {
        "exaltation": ("Овен", 0, 30),  # градус не указан
        "debilitation": ("Весы", 0, 30),
        "moolatrikona": ("Лев", 0, 20),
        "own": [("Лев", 20, 30)]
    },
    "Луна": {
        "exaltation": ("Телец", 0, 4),
        "debilitation": ("Скорпион", 0, 30),
        "moolatrikona": ("Телец", 4, 30),
        "own": [("Рак", 0, 30)]
    },
    "Марс": {
        "exaltation": ("Козерог", 0, 30),
        "debilitation": ("Рак", 0, 30),
        "moolatrikona": ("Овен", 0, 12),
        "own": [("Овен", 12, 30), ("Скорпион", 0, 30)]
    },
    "Меркурий": {
        "exaltation": ("Дева", 0, 16),
        "debilitation": ("Рыбы", 0, 30),
        "moolatrikona": ("Дева", 16, 20),
        "own": [("Дева", 20, 30), ("Близнецы", 0, 30)]
    },
    "Юпитер": {
        "exaltation": ("Рак", 0, 30),
        "debilitation": ("Козерог", 0, 30),
        "moolatrikona": ("Стрелец", 0, 10),
        "own": [("Стрелец", 10, 30), ("Рыбы", 0, 30)]
    },
    "Венера": {
        "exaltation": ("Рыбы", 0, 30),
        "debilitation": ("Дева", 0, 30),
        "moolatrikona": ("Весы", 0, 15),
        "own": [("Весы", 16, 30), ("Телец", 0, 30)]
    },
    "Сатурн": {
        "exaltation": ("Весы", 0, 30),
        "debilitation": ("Овен", 0, 30),
        "moolatrikona": ("Водолей", 0, 20),
        "own": [("Водолей", 20, 30), ("Козерог", 0, 30)]
    }
}

planet_abbr = {
    "Солнце": "Su",
    "Луна": "Mo",
    "Марс": "Ma",
    "Меркурий": "Me",
    "Юпитер": "Ju",
    "Венера": "Ve",
    "Сатурн": "Sa",
    "Раху": "Ra",
    "Кету": "Ke",
    "Асцендент": "As",
    "Уран": "Ur",
    "Нептун": "Ne",
    "Плутон": "Pl",
    "Хирон": "Ch",
    "Сизигия": "Sy",
    "Fortuna": "Fo"
}

functional_nature_by_ascendant = {
    1: {  # Овен (Меша)
        "Солнце": "Благодетель",
        "Луна": "Нейтрально",
        "Марс": "Благодетель",
        "Меркурий": "Вредитель",
        "Юпитер": "Благодетель",
        "Венера": "Нейтрально",
        "Сатурн": "Вредитель"
    },
    2: {  # Телец (Вришабха)
        "Солнце": "Благодетель",
        "Луна": "Вредитель",
        "Марс": "Вредитель",
        "Меркурий": "Благодетель",
        "Юпитер": "Вредитель",
        "Венера": "Вредитель",
        "Сатурн": "Йога-карака"
    },
    3: {  # Близнецы (Митхуна)
        "Солнце": "Вредитель",
        "Луна": "Нейтрально",
        "Марс": "Вредитель",
        "Меркурий": "Благодетель",
        "Юпитер": "Нейтрально",
        "Венера": "Благодетель",
        "Сатурн": "Благодетель"
    },
    4: {  # Рак (Карка)
        "Солнце": "Нейтрально",
        "Луна": "Благодетель",
        "Марс": "Йога-карака",
        "Меркурий": "Вредитель",
        "Юпитер": "Вредитель",
        "Венера": "Вредитель",
        "Сатурн": "Вредитель"
    },
    5: {  # Лев (Симха)
        "Солнце": "Благодетель",
        "Луна": "Вредитель",
        "Марс": "Йога-карака",
        "Меркурий": "Вредитель",
        "Юпитер": "Благодетель",
        "Венера": "Вредитель",
        "Сатурн": "Вредитель"
    },
    6: {  # Дева (Канья)
        "Солнце": "Вредитель",
        "Луна": "Вредитель",
        "Марс": "Вредитель",
        "Меркурий": "Благодетель",
        "Юпитер": "Нейтрально",
        "Венера": "Благодетель",
        "Сатурн": "Вредитель"
    },
    7: {  # Весы (Тула)
        "Солнце": "Вредитель",
        "Луна": "Нейтрально",
        "Марс": "Нейтрально",
        "Меркурий": "Вредитель",
        "Юпитер": "Вредитель",
        "Венера": "Благодетель",
        "Сатурн": "Йога-карака"
    },
    8: {  # Скорпион (Вришчика)
        "Солнце": "Нейтрально",
        "Луна": "Благодетель",
        "Марс": "Вредитель",
        "Меркурий": "Вредитель",
        "Юпитер": "Благодетель",
        "Венера": "Вредитель",
        "Сатурн": "Вредитель"
    },
    9: {  # Стрелец (Дхану)
        "Солнце": "Благодетель",
        "Луна": "Вредитель",
        "Марс": "Благодетель",
        "Меркурий": "Нейтрально",
        "Юпитер": "Благодетель",
        "Венера": "Вредитель",
        "Сатурн": "Вредитель"
    },
    10: {  # Козерог (Макара)
        "Солнце": "Вредитель",
        "Луна": "Нейтрально",
        "Марс": "Вредитель",
        "Меркурий": "Благодетель",
        "Юпитер": "Вредитель",
        "Венера": "Йога-карака",
        "Сатурн": "Благодетель"
    },
    11: {  # Водолей (Кумбха)
        "Солнце": "Нейтрально",
        "Луна": "Вредитель",
        "Марс": "Вредитель",
        "Меркурий": "Вредитель",
        "Юпитер": "Вредитель",
        "Венера": "Йога-карака",
        "Сатурн": "Благодетель"
    },
    12: {  # Рыбы (Мина)
        "Солнце": "Вредитель",
        "Луна": "Благодетель",
        "Марс": "Благодетель",
        "Меркурий": "Нейтрально",
        "Юпитер": "Благодетель",
        "Венера": "Вредитель",
        "Сатурн": "Вредитель"
    }
}

# Вспомогательные функции
def get_birth_utc_offset_str(dt_obj: datetime, latitude: float, longitude: float) -> str:
    """
    Возвращает строку смещения от UTC (в формате ±HH:MM) для заданного местного времени и координат.
    """
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    if not tz_name:
        raise ValueError("Не удалось определить часовой пояс для координат")

    tz = pytz.timezone(tz_name)

    try:
        localized_dt = tz.localize(dt_obj, is_dst=None)
    except pytz.AmbiguousTimeError:
        localized_dt = tz.localize(dt_obj, is_dst=True)

    offset = localized_dt.utcoffset()
    if offset is None:
        raise ValueError("Не удалось определить смещение UTC")

    hours = int(offset.total_seconds() // 3600)
    minutes = int((offset.total_seconds() % 3600) // 60)
    return f"{hours:+03d}:{abs(minutes):02d}"
     
def get_positional_strength(planet: str, sign: str, dms_str: str) -> str | None:
    """
    Возвращает 'Экзальтация', 'Падение', 'Мулатрикона', 'Собственный знак' или None.
    """
    try:
        parts = list(map(int, dms_str.replace("+", "").split(":")))
        #degree = parts[0] + parts[1] / 60 + parts[2] / 3600
        degree = parts[0]
    except Exception:
        return None
    
    #print('это degree')
    #print(degree)
    data = planet_sign_strengths.get(planet)
    if not data:
        return None
        
    prop_to_russian = {
        "exaltation": "Экзальтация",
        "debilitation": "Падение",
        "moolatrikona": "Мулатрикона"
    }
        
    for prop in ["exaltation", "debilitation", "moolatrikona"]:
        prop_sign, start, end  = data.get(prop)
        if sign == prop_sign:
            if start <= degree < end:
                return prop_to_russian[prop]

    # Собственный знак
    for item in data.get("own"):
        own_sign, own_start, own_end = item
        if sign == own_sign and own_start <= degree < own_end:
            return "Свой знак"
            
    return None
    
def get_temporary_relationship(planet: str, owner: str, house_planet: int, house_owner: int) -> str:
    """
    Определяет временное отношение между планетой и хозяином дома.
    Возвращает: 'Друг', 'Враг' или 'Нейтрально'
    """
    if not planet or not owner:
        return "Нейтрально"
    if not isinstance(house_planet, int) or not isinstance(house_owner, int):
        return "Нейтрально"

    offset = (house_owner - house_planet) % 12

    if offset in [1, 2, 3, 9, 10, 11]:
        return "Друг"
    elif offset in [0, 4, 5, 6, 7, 8]:
        return "Враг"
    else:
        return "Нейтрально"
        
def get_combined_relationship(row, planet_to_house_map) -> str:


    """
    Определяет финальное отношение планеты к хозяину знака:
    - сначала проверяет силу положения (экзальтация, падение, мулатрикона, own)
    - затем анализирует natural и temporary отношения к управителю знака
    """
    planet = row.get("Планета")
    sign = row.get("Знак")
    dms_str = row.get("Градусы") or row.get("SignLonDMS")
    owner = row.get("Управитель")
    house_planet = row.get("Дом")
    house_owner = planet_to_house_map.get(owner)
    if planet not in natural_relationships:
        return "-"

    # 1. Положение планеты в знаке
    strength = get_positional_strength(planet, sign, dms_str)
    if strength:
        return strength
    #print(planet)
    #print('это сила')
    #print(strength)

    # 2. Natural отношения
    nat_rel = natural_relationships.get(planet, {})
    if owner in nat_rel.get("friends", []):
        nat = "Друг"
    elif owner in nat_rel.get("enemies", []):
        nat = "Враг"
    else:
        nat = "Нейтрально"
    #print('это натуральные')
    #print(nat)

    # 3. Temporary отношения
    temp = get_temporary_relationship(planet, owner, house_planet, house_owner)
    #print('это временные')
    #print(temp)
    #print('-----------------------------')

    # 4. Итоговая квалификация
    if nat == "Друг" and temp == "Друг":
        return "Большой друг"
    elif nat == "Друг" and temp == "Враг":
        return "Нейтрально"
    elif nat == "Друг" and temp == "Нейтрально":
        return "Друг"
    elif nat == "Враг" and temp == "Друг":
        return "Нейтрально"
    elif nat == "Враг" and temp == "Враг":
        return "Большой враг"
    elif nat == "Враг" and temp == "Нейтрально":
        return "Враг"
    elif nat == "Нейтрально" and temp == "Друг":
        return "Друг"
    elif nat == "Нейтрально" and temp == "Враг":
        return "Враг"
    elif nat == "Нейтрально" and temp == "Нейтрально":
        return "Нейтрально"
    else:
        return "Нейтрально"

def get_planet_role(planet, ascendant_number):
    #print(planet)
    if planet not in ["Солнце", "Луна", "Марс", "Меркурий", "Юпитер", "Венера", "Сатурн"]:
        #print('oops')
        #print('----------------------')
        return '-'
    return functional_nature_by_ascendant[ascendant_number][planet]
  
class AstroChart:
    def __init__(self, birth_date: str, birth_time: str, latitude: str, longitude: str, ayanamsa="Lahiri"):
        swe.set_ephe_path(ETHE_PATH)
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.dt = datetime.strptime(f"{birth_date} {birth_time}", "%d.%m.%Y %H:%M:%S")
        self.utc_offset = get_birth_utc_offset_str(self.dt, self.latitude, self.longitude)
        self.vhd = VedicHoroscopeData(
            year=self.dt.year, 
            month=self.dt.month, 
            day=self.dt.day,
            hour=self.dt.hour, 
            minute=self.dt.minute, 
            second=self.dt.second,
            utc=self.utc_offset, 
            latitude=self.latitude, 
            longitude=self.longitude,
            ayanamsa=ayanamsa, 
            house_system="Placidus"
        )
        self.chart = self.vhd.generate_chart()
        self.planets_data = self.vhd.get_planets_data_from_chart(self.chart)
    
    def get_ayanamsa(self):
        return self.vhd.get_ayanamsa()

    def build_rasi_chart(self, filter_main=True):
        df = pd.DataFrame(self.planets_data)

        possible_sign_cols = ["Sign", "Rasi", "SignName"]
        sign_col = next((col for col in possible_sign_cols if col in df.columns), None)
        if sign_col is None:
            raise ValueError("Не найдена колонка с названием знака зодиака (Sign/Rasi/SignName)")

        columns_mapping = {
            "Object": "Планета",
            sign_col: "Знак",
            "isRetroGrade": "Ретроградность",
            "DMS": "Градусы",
            "Nakshatra": "Накшатра",
            "RasiLord": "Управитель",
            "NakshatraLord": "Управитель накшатры",
            "SignLonDMS": "Градусы"
        }

        df = df.rename(columns=columns_mapping)
        columns_to_delete = ['SubLord', 'SubSubLord', 'HouseNr']
        df = df.drop(columns=[col for col in columns_to_delete if col in df.columns])
        df = self._translate_chart_to_russian(df)
        df["Ретроградность"] = df["Ретроградность"].fillna(False)
        for col in ['LonDecDeg', 'SignLonDecDeg', 'LatDMS', 'SubLord', 'SubSubLord', 'HouseNr']:
            if col in df.columns:
                df = df.drop(columns=col)
                
        # Абревиатура
        df["Абр"] = df["Планета"].apply(lambda x: planet_abbr[x])
                
        # Добавление домов и управлений
        df = self._add_house_info(df)
        self.planet_to_house_map = df.set_index("Планета")["Дом"].to_dict()
        
        # Добавление аспектов
        df = self._add_aspects(df)
        
        # Добавление финального отношения
        df["Отношение"] = df.apply(lambda row: get_combined_relationship(row, self.planet_to_house_map), axis=1)
        
        # Роль
        ascendant_sign = df.at[0, 'Знак']
        ascendant_number = sign_order[ascendant_sign] + 1
        df["Роль"] = df.apply(lambda row: get_planet_role(row['Планета'], ascendant_number), axis=1)
        
        # Фильтрация по main grahas (по желанию)
        if filter_main:
            df = self._filter_main_grahas(df)
        
        return df

    def _build_sign_to_house_map(self, df):
        ascendant_sign = df.at[0, 'Знак']
        j = sign_order[ascendant_sign] + 1
        sign_to_house = {}
        for i in range(1, 13):
            sign_to_house[i] = j
            j = j+1
            if j > 12:
                j = j - 12
        return sign_to_house
        
    def _translate_chart_to_russian(self, df):
        df_translated = df.copy()
        for col, mapping in {
            "Планета": planet_map,
            "Знак": sign_map,
            "Накшатра": nakshatra_map,
            "Управитель": planet_map,
            "Управитель накшатры": planet_map
        }.items():
            if col in df_translated.columns:
                df_translated[col] = df_translated[col].map(mapping).fillna(df_translated[col])
        return df_translated

    def _filter_main_grahas(self, df):
        return df[df["Планета"].isin(main_grahas)].reset_index(drop=True)
        
    def _add_house_info(self, df):
        asc_row = df[df["Планета"] == "Асцендент"]
        if asc_row.empty:
            raise ValueError("В DataFrame нет строки с Асцендентом")
        asc_sign = asc_row.iloc[0]["Знак"]
        rasi_from_asc = rasi_order[rasi_order.index(asc_sign):] + rasi_order[:rasi_order.index(asc_sign)]
        sign_to_house = {sign: i + 1 for i, sign in enumerate(rasi_from_asc)}

        def planet_house(zodiac_sign):
            return sign_to_house.get(zodiac_sign, np.nan)

        def planet_rules(planet):
            ruled_signs = [sign for sign, lord in sign_lords.items() if lord == planet]
            ruled_houses = [sign_to_house[sign] for sign in ruled_signs]
            return sorted(ruled_houses)

        df = df.copy()
        df["Дом"] = df["Знак"].apply(planet_house)
        df["Дом"] = df["Дом"].apply(lambda x: int(x) if pd.notnull(x) else None)
        df["Управляет домами"] = df["Планета"].apply(planet_rules)
        return df
        
    def _add_aspects(self, df):
        """
        Добавляет колонку 'Аспекты' — список домов, которые аспектирует каждая планета.
        """
        aspect_rules = {
            "Солнце": [7],
            "Луна": [7],
            "Меркурий": [7],
            "Венера": [7],
            "Марс": [4, 7, 8],
            "Юпитер": [5, 7, 9],
            "Сатурн": [3, 7, 10]
        }

        def get_aspected_houses(row):
            planet = row["Планета"]
            if planet not in aspect_rules:
                return []

            current_house = row.get("Дом")
            if not isinstance(current_house, int):
                return []

            return sorted([(current_house + offset - 2) % 12 + 1 for offset in aspect_rules[planet]])

        df = df.copy()
        df["Аспекты"] = df.apply(get_aspected_houses, axis=1)
        return df

    # depricated
    def update_chart(self, df, filter_main=True):
        """
        Обновляет DataFrame с натальной картой:
        - очищает лишние колонки
        - добавляет дома и управляемые дома
        - добавляет аспекты
        - добавляет финальное отношение к хозяину знака
        """
        for col in ['LonDecDeg', 'SignLonDecDeg', 'LatDMS', 'SubLord', 'SubSubLord', 'HouseNr']:
            if col in df.columns:
                df = df.drop(columns=col)

        # 2. Добавление домов и управлений
        df = self._add_house_info(df)
        self.rasi_planet_to_house_map = df.set_index("Планета")["Дом"].to_dict()

        # 3. Добавление аспектов
        df = self._add_aspects(df)

        # 4. Добавление финального отношения
        df["Отношение"] = df.apply(lambda row: get_combined_relationship(row, self.rasi_planet_to_house_map), axis=1)

        # 5. Фильтрация по main grahas (по желанию)
        if filter_main:
            df = self._filter_main_grahas(df)

        return df

    def decimal_to_dms(self, deg: float) -> str:
        """
        Преобразует десятичные градусы в строку формата +ЧЧ:ММ:СС (как в rasi_chart).
        """
        d = int(deg)
        m_float = (deg - d) * 60
        m = int(m_float)
        s = int(round((m_float - m) * 60))
        return f"+{d:02d}:{m:02d}:{s:02d}"

    def build_navamsa_chart(self, df_d1: pd.DataFrame):
        """
        Строит таблицу D9 (Навамша) на основе D1, используя Traditional Parasara Method.
        Возвращает DataFrame с колонками: Планета, Знак D9, Градусы D9
        """
        navamsa_dict = {
            0: (1, ["Овен", "Лев", "Стрелец"]),      # fire
            3: (1, ["Рак", "Скорпион", "Рыбы"]),     # water
            6: (1, ["Близнецы", "Весы", "Водолей"]), # air
            9: (1, ["Телец", "Дева", "Козерог"]),    # earth
        }
    
        records = []
    
        for _, row in df_d1.iterrows():
            planet = row["Планета"]
            sign = row["Знак"]
            dms_str = row["Градусы"] if "Градусы" in row else row.get("SignLonDMS")
    
            if pd.isnull(dms_str) or sign not in sign_order:
                continue
    
            # Преобразование DMS в десятичные градусы
            try:
                parts = list(map(int, dms_str.replace("+", "").replace("°", "").replace("'", "").replace("\"", "").split(":")))
                deg = parts[0] + parts[1] / 60 + parts[2] / 3600
            except Exception:
                continue
    
            # 1. Промежуточные величины
            long = deg
            dvf = 9
            f1 = 30.0 / dvf
            d_long = (long * dvf) % 30
            l = int(long // f1)
            sign_index = sign_order[sign]
    
            # 2. Вычисление знака Навамши
            try:
                r = [
                    (seed + dirn * l) % 12
                    for seed, (dirn, sign_list) in navamsa_dict.items()
                    if sign in sign_list
                ][0]
            except IndexError:
                continue  # если знак не найден в navamsa_dict
    
            # 3. Запись результата
            sign_d9_eng = list(sign_map.keys())[r]
            sign_d9_rus = sign_map[sign_d9_eng]
            dms_d9 = self.decimal_to_dms(d_long)
    
            records.append({
                "Планета": planet,
                "Знак": sign_d9_rus,
                "Градусы": dms_d9
            })
            
        navamsa_chart = pd.DataFrame(records)
            
        # Абревиатура
        navamsa_chart["Абр"] = navamsa_chart["Планета"].apply(lambda x: planet_abbr[x])
            
        # управитель
        navamsa_chart["Управитель"] = navamsa_chart["Знак"].apply(lambda x: sign_lords[x])
            
        # дома
        navamsa_chart = self._add_house_info(navamsa_chart)
        self.navamsa_planet_to_house_map = navamsa_chart.set_index("Планета")["Дом"].to_dict()
            
        # аспекты
        navamsa_chart = self._add_aspects(navamsa_chart)
                
        # отношения
        navamsa_chart["Отношение"] = navamsa_chart.apply(lambda row: get_combined_relationship(row, self.navamsa_planet_to_house_map), axis=1)
        
        # роль
        ascendant_sign = navamsa_chart.at[0, 'Знак']
        ascendant_number = sign_order[ascendant_sign] + 1
        navamsa_chart["Роль"] = navamsa_chart.apply(lambda row: get_planet_role(row['Планета'], ascendant_number), axis=1)
    
        return navamsa_chart
