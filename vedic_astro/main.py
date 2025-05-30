from fastapi import FastAPI
from pydantic import BaseModel
from AstroChart import AstroChart
from fastapi.middleware.cors import CORSMiddleware

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
        chart = AstroChart(
            birth_date=data.date,
            birth_time=data.time,
            latitude=str(data.lat),
            longitude=str(data.lon)
        )

        df_rasi = chart.build_rasi_chart()
        df_rasi = chart.update_chart(df_rasi, filter_main=True)

        # Преобразуем DataFrame в JSON
        rasi_json = df_rasi.to_dict(orient="records")

        return {
            "rasi_chart": rasi_json,
            "ayanamsa": chart.get_ayanamsa(),
            "utc_offset": chart.utc_offset
        }

    except Exception as e:
        return {"error": str(e)}
