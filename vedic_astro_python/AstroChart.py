#from jhora.utils import julian_day_number
#from jhora.horoscope.chart.charts import rasi_chart, navamsa_chart
#import jhora.const as const
#import jhora.panchanga.drik as drik
#from jhora.panchanga.drik import Place
from vedicastro.VedicAstro import VedicHoroscopeData
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import pandas as pd
import numpy as np

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

def get_birth_utc_offset_str(dt_obj, latitude, longitude):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    if not tz_name:
        raise ValueError("Не удалось определить часовой пояс для координат")
    tz = pytz.timezone(tz_name)
    localized_dt = tz.localize(dt_obj, is_dst=None)
    offset = localized_dt.utcoffset()
    hours = int(offset.total_seconds() // 3600)
    minutes = int((offset.total_seconds() % 3600) // 60)
    return f"{hours:+03d}:{abs(minutes):02d}"


class AstroChart:
    def __init__(self, birth_date: str, birth_time: str, latitude: str, longitude: str):
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.dt = datetime.strptime(f"{birth_date} {birth_time}", "%d.%m.%Y %H:%M:%S")
        self.utc_offset = get_birth_utc_offset_str(self.dt, self.latitude, self.longitude)
        self.vhd = VedicHoroscopeData(
            year=self.dt.year, month=self.dt.month, day=self.dt.day,
            hour=self.dt.hour, minute=self.dt.minute, second=self.dt.second,
            utc=self.utc_offset, latitude=self.latitude, longitude=self.longitude,
            ayanamsa="Lahiri", house_system="Placidus"
        )
    
    def get_ayanamsa(self):
        return self.vhd.get_ayanamsa()

    def build_rasi_chart(self):
        chart = self.vhd.generate_chart()
        planets_data = self.vhd.get_planets_data_from_chart(chart)
        df = pd.DataFrame(planets_data)

        possible_sign_cols = ["Sign", "Rasi", "SignName"]
        sign_col = next((col for col in possible_sign_cols if col in df.columns), None)
        if sign_col is None:
            raise ValueError("Не найдена колонка с названием знака зодиака (Sign/Rasi/SignName)")

        columns_mapping = {
            "Object": "Планета",
            sign_col: "Знак",
            "Retrograde": "Ретроградность",
            "DMS": "Градусы",
            "Nakshatra": "Накшатра",
            "RasiLord": "Управитель",
            "NakshatraLord": "Управитель накшатры"
        }

        df = df.rename(columns=columns_mapping)
        columns_to_delete = ['SubLord', 'SubSubLord', 'HouseNr']
        df = df.drop(columns=[col for col in columns_to_delete if col in df.columns])
        df = self.translate_chart_to_russian(df)
        return df

    def translate_chart_to_russian(self, df):
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
            return ", ".join(str(h) for h in sorted(ruled_houses))

        df = df.copy()
        df["Дом"] = df["Знак"].apply(planet_house)
        df["Управляет домами"] = df["Планета"].apply(planet_rules)
        return df

    def update_chart(self, df, filter_main=True):
        for col in ['LonDecDeg', 'SignLonDecDeg', 'LatDMS', 'SubLord', 'SubSubLord', 'HouseNr']:
            if col in df.columns:
                df = df.drop(columns=col)
        df = self._add_house_info(df)
        if filter_main:
            df = self._filter_main_grahas(df)
        return df

    def decimal_to_dms(self, deg):
        d = int(deg)
        m_float = (deg - d) * 60
        m = int(m_float)
        s = int(round((m_float - m) * 60))
        return f"{d:02d}°{m:02d}'{s:02d}''"

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
    
        return pd.DataFrame(records)