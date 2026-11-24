'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { ArrowDownToLine, Bomb, Crown, Handshake, Heart, House, Scale, Star, TriangleAlert, type LucideIcon } from 'lucide-react'
import AstroSvgMap from '@/components/AstroSvgMap'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
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
}

const relationIcons: Partial<Record<string, { Icon: LucideIcon; color: string; label: string }>> = {
  "Большой друг": { Icon: Heart, color: "text-pink-700 dark:text-pink-300", label: "В доме большого друга" },
  "Друг": { Icon: Handshake, color: "text-green-700 dark:text-green-300", label: "В доме друга" },
  "Нейтрально": { Icon: Scale, color: "text-slate-600 dark:text-slate-300", label: "В нейтральном доме" },
  "Враг": { Icon: TriangleAlert, color: "text-amber-700 dark:text-amber-300", label: "В доме врага" },
  "Большой враг": { Icon: Bomb, color: "text-red-700 dark:text-red-300", label: "В доме большого врага" },
  "Свой знак": { Icon: House, color: "text-sky-700 dark:text-sky-300", label: "В своем знаке" },
  "Мулатрикона": { Icon: Star, color: "text-violet-700 dark:text-violet-300", label: "Мулатрикона" },
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
          <relation.Icon className={`size-3 ${relation.color}`} aria-hidden="true" />
          <span className="sr-only">{relation.label}</span>
        </span>
      )}
    </span>
  )
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
    return (
      <div className="mx-auto mt-10 w-full max-w-sm space-y-3 px-4 text-center">
        <p id="chart-loading-label">Загрузка карты…</p>
        <Progress aria-labelledby="chart-loading-label" />
      </div>
    )
  }

	return (
	  <div className="max-w-6xl mx-auto mt-10">
		<h1 className="text-2xl font-bold mb-6 text-center">Натальная карта</h1>
		<div className="flex justify-center mb-6">
		  <ThemeToggle />
		</div>
		
		<Tabs defaultValue="rasi" className="w-full">
		 <TabsList className="mb-6 mx-auto">
			<TabsTrigger value="rasi" className="px-4">Раши</TabsTrigger>
			<TabsTrigger value="navamsa" className="px-4">Навамша</TabsTrigger>
		  </TabsList>

		  <TabsContent value="rasi">
			<div className="flex flex-col items-center">
			  <h2 className="text-xl font-semibold mb-4">Раши</h2>
			  <AstroSvgMap
				planets={data.rasi.planets}
				signsByHouse={data.rasi.signsByHouse}
			  />

			  <h2 className="text-xl font-semibold text-center mt-10 mb-4">Раши</h2>
			  {/* Таблица D1 */}
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
					{data.rasi.planets.map((planet, i) => (
					  <TableRow key={i}>
						<TableCell><PlanetName planet={planet} /></TableCell>
						<TableCell>{planet.sign}</TableCell>
						<TableCell>{planet.degree}</TableCell>
						<TableCell>{planet.house}</TableCell>
						<TableCell>{planet.sign_lord}</TableCell>
						<TableCell>
						  {planet.houses_ruled.length
							? planet.houses_ruled.join(", ")
							: "-"}
						</TableCell>
						<TableCell>{planet.role || "-"}</TableCell>
					  </TableRow>
					))}
				  </TableBody>
				</Table>
			</div>
		  </TabsContent>

		  <TabsContent value="navamsa">
			<div className="flex flex-col items-center">
			  <h2 className="text-xl font-semibold mb-4">Навамша</h2>
			  <AstroSvgMap
				planets={data.navamsa.planets}
				signsByHouse={data.navamsa.signsByHouse}
			  />

			  <h2 className="text-xl font-semibold text-center mt-10 mb-4">Навамша</h2>
			  {/* Таблица D9 */}
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
					{data.navamsa.planets.map((planet, i) => (
					  <TableRow key={i}>
						<TableCell><PlanetName planet={planet} /></TableCell>
						<TableCell>{planet.sign}</TableCell>
						<TableCell>{planet.degree}</TableCell>
						<TableCell>{planet.house}</TableCell>
						<TableCell>{planet.sign_lord}</TableCell>
						<TableCell>
						  {planet.houses_ruled.length
							? planet.houses_ruled.join(", ")
							: "-"}
						</TableCell>
						<TableCell>{planet.role || "-"}</TableCell>
					  </TableRow>
					))}
				  </TableBody>
				</Table>
			</div>
		  </TabsContent>
		</Tabs>
	  </div>
	)
