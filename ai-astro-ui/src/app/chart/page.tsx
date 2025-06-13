'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import AstroSvgMap from '@/components/AstroSvgMap'

type PlanetData = {
  "Планета": string
  "Знак": string
  "Дом": number
  "Накшатра": string
  "Управитель": string
  "Управитель накшатры": string
  "Управляет домами": string
  SignLonDMS: string
  isRetroGrade?: boolean | null
}

export default function ChartPage() {
  const searchParams = useSearchParams()
  const [data, setData] = useState<PlanetData[] | null>(null)
  const [error, setError] = useState<string | null>(null)

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

        setData(result.rasi_chart)
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

      {/* SVG карта с динамической вставкой планет */}
      <AstroSvgMap planets={data} />

      <h2 className="text-xl font-semibold text-center mt-10 mb-4">Таблица данных (D1)</h2>

      <table className="w-full border text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 border">Планета</th>
            <th className="p-2 border">Знак</th>
            <th className="p-2 border">Градус</th>
            <th className="p-2 border">Дом</th>
            <th className="p-2 border">Накшатра</th>
            <th className="p-2 border">Упр. знака</th>
            <th className="p-2 border">Упр. накшатры</th>
            <th className="p-2 border">Упр. домов</th>
            <th className="p-2 border">Rx</th>
          </tr>
        </thead>
        <tbody>
          {data.map((planet, i) => (
            <tr key={i}>
              <td className="p-2 border">{planet["Планета"]}</td>
              <td className="p-2 border">{planet["Знак"]}</td>
              <td className="p-2 border">{planet.SignLonDMS}</td>
              <td className="p-2 border">{planet["Дом"]}</td>
              <td className="p-2 border">{planet["Накшатра"]}</td>
              <td className="p-2 border">{planet["Управитель"]}</td>
              <td className="p-2 border">{planet["Управитель накшатры"]}</td>
              <td className="p-2 border">{planet["Управляет домами"]}</td>
              <td className="p-2 border text-center">{planet.isRetroGrade ? 'R' : ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
