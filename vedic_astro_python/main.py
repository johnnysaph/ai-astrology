from fastapi import FastAPI
from pydantic import BaseModel
from AstroChart import AstroChart
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pandas as pd

def build_api_response(astroChart: object, charts: dict[str, pd.DataFrame], ayanamsa: str = "Lahiri") -> dict:
    """
    Формирует финальный JSON-ready ответ API.
    charts: словарь DataFrame'ов, например {"rasi": df_rasi, "navamsa": df_navamsa}
    ayanamsa: название используемой айанамсы
    """
    response = {
        "charts": {},
        "metadata": {
            "ayanamsa": ayanamsa,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
    }

    for chart_name, df in charts.items():
        # Преобразуем DataFrame в список словарей
        planet_list = []
        for _, row in df.iterrows():
            planet_data = {
                "planet": row.get("Планета"),
                "abbr": row.get("Абр"),
                "sign": row.get("Знак"),
                "degree": row.get("Градусы"),
                "house": row.get("Дом"),
                "aspects": row.get("Аспекты"),
                "role": row.get("Роль"),
                "relation": row.get("Отношение"),
                "is_retrograde": bool(row.get("Ретроградность")),
                "nakshatra": row.get("Накшатра"),
                "sign_lord": row.get("Управитель"),
                "nakshatra_lord": row.get("Управитель накшатры"),
                "houses_ruled": row.get("Управляет домами"),
            }
            planet_list.append(planet_data)
        
        response["charts"][chart_name] = {
            "type": chart_name.upper(),
            "planets": planet_list,
            "signs_by_house": astroChart._build_sign_to_house_map(df)
        }

    return response


app = FastAPI()

# CORS — чтобы фронтенд мог делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← можешь сузить до своего домена
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель входных данных
class BirthData(BaseModel):
    date: str      # формат: "20.01.1987"
    time: str      # формат: "10:50:00"
    lat: float
    lon: float

@app.post("/calculate")
def calculate(data: BirthData):
    try:
        astroChart = AstroChart(
            birth_date=data.date,
            birth_time=data.time,
            latitude=str(data.lat),
            longitude=str(data.lon)
        )

        rasi_chart = astroChart.build_rasi_chart()
        navamsa_chart = astroChart.build_navamsa_chart(rasi_chart)

        # API ответ
        api_result = build_api_response(
            astroChart,
            {
                "rasi": rasi_chart,
                "navamsa": navamsa_chart
            },
            ayanamsa="Lahiri"
        )

        return api_result

    except Exception as e:
        return {"error": str(e)}
