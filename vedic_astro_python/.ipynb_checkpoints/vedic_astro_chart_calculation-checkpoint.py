from vedicastro.VedicAstro import VedicHoroscopeData
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import pandas as pd
import numpy as np

# === Вспомогательные функции ===

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

def translate_chart_to_russian(df):
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
        "Pushya": "Пушья", "Ashlesha": "Ашлеша", "Magha": "Магха", "PurvaPhalgunī": "Пурва Пхалгуни",
        "UttaraPhalgunī": "Уттара Пхалгуни", "Hasta": "Хаста", "Chitra": "Читра",
        "Svati": "Свати", "Vishakha": "Вишакха", "Anuradha": "Анурадха", "Jyeshtha": "Джьештха",
        "Mula": "Мула", "PurvaAshadha": "Пурва Ашадха", "UttaraAshadha": "Уттара Ашадха",
        "Shravana": "Шравана", "Dhanishta": "Дхаништха", "Shatabhishak": "Шатабхиша",
        "PurvaBhādrapadā": "Пурва Бхадрапада", "UttaraBhādrapadā": "Уттара Бхадрапада",
        "Revati": "Ревати"
    }

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

def filter_main_grahas(df):
    main_grahas = [
        "Асцендент", "Солнце", "Луна", "Марс", "Меркурий",
        "Юпитер", "Венера", "Сатурн", "Раху", "Кету"
    ]
    return df[df["Планета"].isin(main_grahas)].reset_index(drop=True)

def add_house_info(df):
    rasi_order = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион",
                  "Стрелец", "Козерог", "Водолей", "Рыбы"]
    sign_lords = {
        "Овен": "Марс", "Телец": "Венера", "Близнецы": "Меркурий", "Рак": "Луна",
        "Лев": "Солнце", "Дева": "Меркурий", "Весы": "Венера", "Скорпион": "Марс",
        "Стрелец": "Юпитер", "Козерог": "Сатурн", "Водолей": "Сатурн", "Рыбы": "Юпитер"
    }

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

# === Главная функция ===

def build_chart(birth_date: str, birth_time: str, latitude: str, longitude: str):
    dt = datetime.strptime(f"{birth_date} {birth_time}", "%d.%m.%Y %H:%M:%S")
    lat = float(latitude)
    lon = float(longitude)
    utc_offset = get_birth_utc_offset_str(dt, lat, lon)

    vhd = VedicHoroscopeData(
        year=dt.year, month=dt.month, day=dt.day,
        hour=dt.hour, minute=dt.minute, second=dt.second,
        utc=utc_offset, latitude=lat, longitude=lon,
        ayanamsa="Lahiri", house_system="Placidus"
    )

    vhd.get_ayanamsa()
    chart = vhd.generate_chart()
    planets_data = vhd.get_planets_data_from_chart(chart)
    df = pd.DataFrame(planets_data)

    # Определим колонку знака
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

    # Удалим неиспользуемые колонки, если они есть
    for col in ['LonDecDeg', 'SignLonDecDeg', 'LatDMS', 'SubLord', 'SubSubLord', 'HouseNr']:
        if col in df.columns:
            df = df.drop(columns=col)

    df = translate_chart_to_russian(df)
    df = filter_main_grahas(df)
    df = add_house_info(df)

    return df