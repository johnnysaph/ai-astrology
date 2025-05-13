from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from zoneinfo import ZoneInfo
from datetime import datetime
import swisseph as swe
import pandas as pd
from vedastro import *
from math import floor

ZODIAC_SIGNS = [
    "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
    "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
]


SIGN_RULERS = {
    "Овен": "Марс",
    "Телец": "Венера",
    "Близнецы": "Меркурий",
    "Рак": "Луна",
    "Лев": "Солнце",
    "Дева": "Меркурий",
    "Весы": "Венера",
    "Скорпион": "Марс",
    "Стрелец": "Юпитер",
    "Козерог": "Сатурн",
    "Водолей": "Сатурн",
    "Рыбы": "Юпитер",
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
    "Рыбы":      ["Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"],
}

planetName_eng_to_ru = {
    "Sun": "Солнце",
    "Moon": "Луна",
    "Mars": "Марс",
    "Mercury": "Меркурий",
    "Jupiter": "Юпитер",
    "Venus": "Венера",
    "Saturn": "Сатурн",
    "Rahu": "Раху",
    "Ketu": "Кету"
}

planet_to_power = {
    "Sun": 390,
    "Moon": 360,
    "Mars": 300,
    "Mercury": 420,
    "Jupiter": 390,
    "Venus": 330,
    "Saturn": 300
}

def get_sign_name(degree):
    index = int(degree // 30)
    return ZODIAC_SIGNS[index % 12]

def format_longitude(degree):
    sign_index = int(degree // 30)
    sign_deg = degree % 30
    minutes = (sign_deg - int(sign_deg)) * 60
    return f"{ZODIAC_SIGNS[sign_index]} {int(sign_deg)}° {int(minutes)}′"
    
# запасной метод, координаты нужно получать на фронте
def get_coordinates_by_geo(city, country):
    geolocator = Nominatim(user_agent="vedic_chart_app")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError("Местоположение не найдено")

def get_birth_timezone(birth_datetime_str, latitude, longitude):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    if not tz_name:
        raise ValueError("Не удалось определить часовой пояс для координат")
    return tz_name

def get_utc_birth_datetime(birth_datetime_str, tz_name):
    tz = ZoneInfo(tz_name)
    dt_local = datetime.strptime(birth_datetime_str, "%d.%m.%Y %H:%M").replace(tzinfo=tz)
    return dt_local.astimezone(ZoneInfo("UTC"))

def convert_utc_to_local_string(dt_utc, tz_name):
    local_dt = dt_utc.astimezone(ZoneInfo(tz_name))
    time_str = local_dt.strftime("%H:%M %d/%m/%Y %z")  # без двоеточия в смещении
    # если хочешь формат именно "+05:00" — нужно вручную отформатировать
    offset = local_dt.strftime("%z")  # пример: +0500
    offset_formatted = f"{offset[:3]}:{offset[3:]}"  # → +05:00
    final_str = f"{local_dt.strftime('%H:%M %d/%m/%Y')} {offset_formatted}"
    return final_str

# makes request to vedicAstro API
def get_vedicAstroAPI_data(dt_utc, tz_name, location_name, latitude, longitude):
    birth_time_for_api = convert_utc_to_local_string(dt_utc, tz_name)
    print(birth_time_for_api)
    # set birth location
    geolocation = GeoLocation(location_name, latitude, longitude)
    # group all birth time data together (day/month/year)
    return Time(birth_time_for_api, geolocation)

# makes request to vedicAstro API
def get_asc(vedicAstro_data):
    houses_data = Calculate.AllHouseRasiSigns(vedicAstro_data)
    return houses_data[0]['AllHouseRasiSigns']

# makes request to vedicAstro API
def get_shad_bala(vedicAstro_data):
    shad_bala = Calculate.AllPlanetStrength(vedicAstro_data)
    # Разбиваем строку и собираем пары
    pairs = shad_bala.split("), ")
    result = {}

    for pair in pairs:
        pair = pair.strip("()")  # удаляем скобки
        value_str, planet_en = pair.split(", ")
        value = float(value_str)
        planet_ru = planetName_eng_to_ru.get(planet_en, planet_en)  # переводим на русский
        if planet_en in planet_to_power:
            planet_power = planet_to_power[planet_en]
            result[planet_ru] = int(value / planet_power * 100)
    return result

def get_planets_positions(dt_utc):
    # Юлианская дата
    hour_decimal = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_decimal)
    #ayanamsa = swe.get_ayanamsa(jd_ut)

    # Флаги для сидерических координат
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    # Список планет
    planet_ids = [
        swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
        swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
        swe.MEAN_NODE  # Раху
    ]
    planet_names = [
        "Солнце", "Луна", "Меркурий", "Венера", "Марс",
        "Юпитер", "Сатурн", "Уран", "Нептун", "Плутон", "Раху"
    ]

    result = []
    # planets positions calculation
    for i in range(len(planet_ids)):
        planet_id = planet_ids[i]
        planet_name = planet_names[i]

        calc_result = swe.calc(jd_ut, planet_id, flags)
        lon = calc_result[0][0] % 360
        sign = get_sign_name(lon)
        degree_in_sign = lon % 30
        formatted = format_longitude(lon)

        result.append({
            "Планета": planet_name,
            "Долгота (°)": round(lon, 4),
            "Знак": sign,
            "Градус в знаке": round(degree_in_sign, 4),
            "Формат": formatted
        })

    # Кету — противоположная точка Раху
    rahu_lon = result[-1]["Долгота (°)"]
    ketu_lon = (rahu_lon + 180.0) % 360
    ketu_sign = get_sign_name(ketu_lon)
    ketu_deg = ketu_lon % 30
    ketu_formatted = format_longitude(ketu_lon)
    result.append({
        "Планета": "Кету",
        "Долгота (°)": round(ketu_lon, 4),
        "Знак": ketu_sign,
        "Градус в знаке": round(ketu_deg, 4),
        "Формат": ketu_formatted
    })
    return pd.DataFrame(result)

def parse_ascendant_string(asc_str):
    sign_rus = {
        "Aries": "Овен", "Taurus": "Телец", "Gemini": "Близнецы", "Cancer": "Рак",
        "Leo": "Лев", "Virgo": "Дева", "Libra": "Весы", "Scorpio": "Скорпион",
        "Sagittarius": "Стрелец", "Capricorn": "Козерог", "Aquarius": "Водолей", "Pisces": "Рыбы"
    }
    parts = asc_str.split(":")
    eng_sign = parts[0].strip()
    deg_str = parts[1].strip().replace("°", "").replace("'", "").replace("\"", "")
    deg_parts = deg_str.split()
    deg = int(deg_parts[0])
    min_ = int(deg_parts[1])
    sec = int(deg_parts[2])
    total_deg = deg + min_ / 60 + sec / 3600
    sign = sign_rus[eng_sign]
    sign_index = list(sign_rus.values()).index(sign)
    asc_longitude = sign_index * 30 + total_deg
    return sign, asc_longitude

# Добавим столбец "Дом"
def get_house(sign):
    sign_index = list(SIGN_RULERS.keys()).index(sign)
    return (sign_index - asc_sign_index) % 12 + 1

def get_house_ruled(planet):
    signs_ruled = planet_to_signs.get(planet, [])
    houses = sorted([(list(SIGN_RULERS.keys()).index(sign) - asc_sign_index) % 12 + 1 for sign in signs_ruled])
    return ", ".join(str(h) for h in houses)

# Обновлённая версия функции с улучшениями: формат Асцендента + столбец "Управляет"
def extend_planet_df(df, asc_str):
    # Парсим асцендент
    asc_sign, asc_lon = parse_ascendant_string(asc_str)
    asc_deg = asc_lon % 30
    asc_sign_index = list(SIGN_RULERS.keys()).index(asc_sign)

    # Формат с указанием знака
    formatted_asc = f"{asc_sign} {floor(asc_deg)}°{floor((asc_deg % 1) * 60)}′"

    # Добавим строку Асцендента
    asc_row = {
        "Планета": "Асцендент",
        "Долгота (°)": round(asc_lon, 4),
        "Знак": asc_sign,
        "Градус в знаке": round(asc_deg, 4),
        "Формат": formatted_asc
    }
    df = pd.concat([df, pd.DataFrame([asc_row])], ignore_index=True)

    # Добавим столбец "Управитель"
    df["Управитель"] = df["Знак"].map(SIGN_RULERS)

    df["Дом"] = df["Знак"].apply(get_house)

    # Добавим столбец "Управляет" — для каждой планеты: какими домами она управляет
    planet_to_signs = {}
    for sign, ruler in SIGN_RULERS.items():
        planet_to_signs.setdefault(ruler, []).append(sign)

    df["Управляет домами"] = df["Планета"].apply(get_house_ruled)

    return df

def build_navamsa(df):
    navamsa_signs = []

    for i, row in df.iterrows():
        rashi_sign = row["Знак"]
        degree_in_sign = row["Градус в знаке"]
        planet = row["Планета"]

        if rashi_sign is None or degree_in_sign is None:
            navamsa_signs.append(None)
            continue

        part = int(degree_in_sign // (30 / 9))  # каждая навамша = 3°20′
        d9_sign = D1_TO_D9_MAP[rashi_sign][part]

        # Отладочный вывод для Асцендента
        if planet == "Асцендент":
            print(f"[DEBUG] Асцендент: знак={rashi_sign}, градус={degree_in_sign:.4f}, часть={part}, Навамша={d9_sign}")

        navamsa_signs.append(d9_sign)

    df["Навамша (знак)"] = navamsa_signs
    return df

