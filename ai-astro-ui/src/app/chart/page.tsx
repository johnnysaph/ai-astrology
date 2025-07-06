'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import AstroSvgMap from '@/components/AstroSvgMap'


type PlanetData = {
  planet: string
  abbr: string
  house: number
  sign: string
  degree: string
  is_retrograde: boolean
  nakshatra: string | null
  sign_lord: string
  nakshatra_lord: string | null
  houses_ruled: number[]
  role: string
  relation: string
}

export default function ChartPage() {
  const searchParams = useSearchParams()
  const [data, setData] = useState<{
	  rasi: {
		planets: PlanetData[]
		signsByHouse: Record<number, number>
	  }
	  navamsa: {
		planets: PlanetData[]
		signsByHouse: Record<number, number>
	  }
	} | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<0 | 1>(0);

  useEffect(() => {
    const date = searchParams.get('date')
    const time = searchParams.get('time')
    const lat = searchParams.get('lat')
    const lon = searchParams.get('lon')

    if (!date || !time || !lat || !lon) {
      setError("Недостаточно данных для расчёта карты.")
      return
    }

    const fetchData = async () => {
      try {
        const res = await fetch("https://ai-astrology-api.onrender.com/calculate", {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ date, time, lat: parseFloat(lat), lon: parseFloat(lon) })
        })

        if (!res.ok) {
          throw new Error("Ошибка при получении данных")
        }

        const result = await res.json()
        console.log("🌟 API response:", result)

        setData({
		  rasi: {
			planets: result.charts.rasi.planets,
			signsByHouse: result.charts.rasi.signs_by_house
		  },
		  navamsa: {
			planets: result.charts.navamsa.planets,
			signsByHouse: result.charts.navamsa.signs_by_house
		  }
		})
      } catch (err) {
        console.error(err)
        setError("Произошла ошибка при загрузке данных.")
      }
    }

    fetchData()
  }, [searchParams])

  if (error) {
    return <p className="text-center mt-10 text-red-500">{error}</p>
  }

  if (!data) {
    return <p className="text-center mt-10">Загрузка...</p>
  }

	return (
	  <div className="max-w-6xl mx-auto mt-10">
		<h1 className="text-2xl font-bold mb-6 text-center">Натальная карта</h1>
		<div className="flex justify-center gap-4 mb-6">
		  <button
			onClick={() => setActiveTab(0)}
			className={`px-4 py-2 rounded ${
			  activeTab === 0
				? "bg-blue-600 text-white"
				: "bg-gray-200 text-gray-800"
			}`}
		  >
			Раши (D1)
		  </button>
		  <button
			onClick={() => setActiveTab(1)}
			className={`px-4 py-2 rounded ${
			  activeTab === 1
				? "bg-blue-600 text-white"
				: "bg-gray-200 text-gray-800"
			}`}
		  >
			Навамша (D9)
		  </button>
		</div>

		<div className="flex flex-col items-center">
		  {activeTab === 0 ? (
			<>
			  <h2 className="text-xl font-semibold mb-4">Раши (D1)</h2>
			  <AstroSvgMap
				planets={data.rasi.planets}
				signsByHouse={data.rasi.signsByHouse}
			  />
			</>
		  ) : (
			<>
			  <h2 className="text-xl font-semibold mb-4">Навамша (D9)</h2>
			  <AstroSvgMap
				planets={data.navamsa.planets}
				signsByHouse={data.navamsa.signsByHouse}
			  />
			</>
		  )}
		</div>

		<h2 className="text-xl font-semibold text-center mt-10 mb-4">
		  {activeTab === 0 ? "Таблица данных (D1)" : "Таблица данных (D9)"}
		</h2>

		<table className="w-full border text-sm">
		  <thead className="bg-gray-100">
			<tr>
			  <th className="p-2 border">Планета</th>
			  <th className="p-2 border">Знак</th>
			  <th className="p-2 border">Градус</th>
			  <th className="p-2 border">Дом</th>
			  <th className="p-2 border">Управитель</th>
			  <th className="p-2 border">Управляет домами</th>
			  <th className="p-2 border">Отношение</th>
			  <th className="p-2 border">Роль</th>
			</tr>
		  </thead>
		  <tbody>
			{(activeTab === 0 ? data.rasi.planets : data.navamsa.planets).map((planet, i) => (
			  <tr key={i}>
				<td className="p-2 border">{planet.planet}</td>
				<td className="p-2 border">{planet.sign}</td>
				<td className="p-2 border">{planet.degree}</td>
				<td className="p-2 border">{planet.house}</td>
				<td className="p-2 border">{planet.sign_lord}</td>
				<td className="p-2 border">
				  {planet.houses_ruled.length ? planet.houses_ruled.join(", ") : "-"}
				</td>
				<td className="p-2 border">{planet.relation || "-"}</td>
				<td className="p-2 border">{planet.role || "-"}</td>
			  </tr>
			))}
		  </tbody>
		</table>
	  </div>
	)