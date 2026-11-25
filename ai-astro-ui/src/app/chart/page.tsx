'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { ArrowDownToLine, Bomb, Crown, Gem, Handshake, Heart, House, Scale, TriangleAlert, type LucideIcon } from 'lucide-react'
import AstroSvgMap from '@/components/AstroSvgMap'
import SouthIndianChart from '@/components/SouthIndianChart'
import { Progress } from '@/components/ui/progress'
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { ThemeToggle } from "@/components/ThemeToggle"


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
  aspects: number[]
}

type ApiChart = {
  planets: PlanetData[]
  signs_by_house: Record<number, number>
}

function chartLabel(key: string) {
  if (key === "rasi") return "Раши (D1)"
  if (key === "navamsa") return "Навамша (D9)"
  if (key === "moon") return "Лунная карта"
  return key.toUpperCase()
}

function chartOrder(key: string) {
  if (key === "rasi") return 1
  if (key === "navamsa") return 9
  if (key === "moon") return 0
  return Number(key.slice(1)) || Number.MAX_SAFE_INTEGER
}

const relationIcons: Partial<Record<string, { Icon: LucideIcon; color: string; label: string }>> = {
  "Большой друг": { Icon: Heart, color: "text-pink-700 dark:text-pink-300", label: "В доме большого друга" },
  "Друг": { Icon: Handshake, color: "text-green-700 dark:text-green-300", label: "В доме друга" },
  "Нейтрально": { Icon: Scale, color: "text-slate-600 dark:text-slate-300", label: "В нейтральном доме" },
  "Враг": { Icon: TriangleAlert, color: "text-amber-700 dark:text-amber-300", label: "В доме врага" },
  "Большой враг": { Icon: Bomb, color: "text-red-700 dark:text-red-300", label: "В доме большого врага" },
  "Свой знак": { Icon: House, color: "text-sky-700 dark:text-sky-300", label: "В своем знаке" },
  "Мулатрикона": { Icon: Gem, color: "text-violet-700 dark:text-violet-300", label: "Мулатрикона" },
  "Экзальтация": { Icon: Crown, color: "text-amber-700 dark:text-amber-300", label: "Экзальтация" },
  "Падение": { Icon: ArrowDownToLine, color: "text-orange-700 dark:text-orange-300", label: "Дебилитация" },
}

function PlanetName({ planet }: { planet: PlanetData }) {
  const relation = relationIcons[planet.relation]

  return (
    <span className="inline-flex items-center gap-2">
      {planet.planet}
      {relation && (
        <span
          className="inline-flex rounded border border-border px-1 py-0.5"
          title={relation.label}
        >
          <relation.Icon className={`size-4 ${relation.color}`} aria-hidden="true" />
          <span className="sr-only">{relation.label}</span>
        </span>
      )}
    </span>
  )
}

export default function ChartPage() {
  const searchParams = useSearchParams()
  const [data, setData] = useState<Record<string, ApiChart> | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [selectedChart, setSelectedChart] = useState("rasi")
  const [chartStyle, setChartStyle] = useState("north")

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
      setError(null)
      setData(null)
      setSelectedChart("rasi")
      try {
        const apiUrl = process.env.NEXT_PUBLIC_ASTRO_API_URL || "https://ai-astrology-api.onrender.com"
        const res = await fetch(`${apiUrl}/calculate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ date, time, lat: parseFloat(lat), lon: parseFloat(lon) })
        })

        if (!res.ok) {
          throw new Error("Ошибка при получении данных")
        }

        const result = await res.json()
        if (typeof result?.error === 'string' && result.error) {
          setError(`Не удалось рассчитать карту. ${result.error}`)
          return
        }

        if (!result?.charts?.rasi || !result?.charts?.navamsa) {
          setError("Сервер не вернул данные карт D1 и D9.")
          return
        }

        setData(result.charts)
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
    return (
      <div className="mx-auto mt-10 w-full max-w-sm space-y-3 px-4 text-center">
        <p id="chart-loading-label">Загрузка карты…</p>
        <Progress aria-labelledby="chart-loading-label" />
      </div>
    )
  }

  const activeChart = data[selectedChart]
  const chartKeys = Object.keys(data).sort((a, b) => chartOrder(a) - chartOrder(b))
  const chartName = chartLabel(selectedChart)

  return (
    <div className="mx-auto mt-10 max-w-6xl px-4">
      <h1 className="mb-6 text-center text-2xl font-bold">Натальная карта</h1>
      <div className="mb-6 flex flex-wrap items-center justify-center gap-3">
        <select
          aria-label="Выбрать карту"
          className="h-9 max-w-full rounded-md border border-input bg-background px-3 text-sm text-foreground focus-visible:outline-2 focus-visible:outline-ring"
          value={selectedChart}
          onChange={(event) => setSelectedChart(event.target.value)}
        >
          {chartKeys.map((key) => (
            <option key={key} value={key}>{chartLabel(key)}</option>
          ))}
        </select>
        <select
          aria-label="Стиль карты"
          className="h-9 max-w-full rounded-md border border-input bg-background px-3 text-sm text-foreground focus-visible:outline-2 focus-visible:outline-ring"
          value={chartStyle}
          onChange={(event) => setChartStyle(event.target.value)}
        >
          <option value="north">Североиндийский</option>
          <option value="south">Южноиндийский</option>
        </select>
        <ThemeToggle />
      </div>

      <div className="mx-auto aspect-square w-full max-w-xl [--chart-line:#67a5c1] [--chart-highlight:#38bdf8] [--chart-planet:black] [--chart-ascendant:#8b0000] dark:[--chart-line:#7ab8d4] dark:[--chart-planet:#d4af37]">
        {chartStyle === "south" ? (
          <SouthIndianChart key={selectedChart} name={chartName} planets={activeChart.planets} signsByHouse={activeChart.signs_by_house} />
        ) : (
          <AstroSvgMap key={selectedChart} planets={activeChart.planets} signsByHouse={activeChart.signs_by_house} />
        )}
      </div>

      <h2 className="mb-4 mt-10 text-center text-xl font-semibold">{chartName}</h2>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Планета</TableHead>
            <TableHead>Знак</TableHead>
            <TableHead>Градус</TableHead>
            <TableHead>Дом</TableHead>
            <TableHead>Управитель</TableHead>
            <TableHead>Управляет домами</TableHead>
            <TableHead>Роль</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {activeChart.planets.map((planet) => (
            <TableRow key={planet.abbr}>
              <TableCell><PlanetName planet={planet} /></TableCell>
              <TableCell>{planet.sign}</TableCell>
              <TableCell>{planet.degree}</TableCell>
              <TableCell>{planet.house}</TableCell>
              <TableCell>{planet.sign_lord}</TableCell>
              <TableCell>{planet.houses_ruled.join(", ") || "-"}</TableCell>
              <TableCell>{planet.role || "-"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
