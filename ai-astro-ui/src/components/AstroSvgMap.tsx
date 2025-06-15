import React, { useState } from "react"

type PlanetData = {
  "Планета": string
  "Дом": number
  "Управляет домами"?: string | number[]
}

type Props = {
  planets: PlanetData[]
}

const signToNumber: Record<string, number> = {
  "Овен": 1, "Телец": 2, "Близнецы": 3, "Рак": 4,
  "Лев": 5, "Дева": 6, "Весы": 7, "Скорпион": 8,
  "Стрелец": 9, "Козерог": 10, "Водолей": 11, "Рыбы": 12,
}

const signsByHouse: Record<number, number> = {
  1: 12, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5,
  7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11,
}

const planetAbbr: Record<string, string> = {
  "Асцендент": "As", "Солнце": "Su", "Луна": "Mo", "Марс": "Ma",
  "Меркурий": "Me", "Юпитер": "Ju", "Венера": "Ve", "Сатурн": "Sa",
  "Раху": "Ra", "Кету": "Ke",
}

export default function AstroSvgMap({ planets }: Props) {
  const [highlightedHouses, setHighlightedHouses] = useState<number[]>([])
  const groupedByHouse: Record<number, string[]> = {}

  planets.forEach(p => {
    const abbr = planetAbbr[p["Планета"]] || p["Планета"]
    if (!groupedByHouse[p["Дом"]]) {
      groupedByHouse[p["Дом"]] = []
    }
    groupedByHouse[p["Дом"]].push(abbr)
  })

  const handlePlanetClick = (abbr: string) => {
    const match = planets.find(p => planetAbbr[p["Планета"]] === abbr)
    const raw = match?.["Управляет домами"]

    let ids: number[] = []

    if (typeof raw === "string") {
      ids = raw.split(",").map(s => parseInt(s.trim())).filter(n => !isNaN(n))
    } else if (Array.isArray(raw)) {
      ids = raw
    }

    const alreadySelected = ids.length > 0 &&
      ids.every(h => highlightedHouses.includes(h)) &&
      highlightedHouses.length === ids.length

    setHighlightedHouses(alreadySelected ? [] : ids)
  }

  const renderPlanets = (house: number, x: number, y: number) => {
    const items = groupedByHouse[house]
    if (!items) return null

    return (
      <text
        x={x}
        y={y}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize="12"
        fill="black"
      >
        {items.map((abbr, i) => (
          <tspan
            key={`${house}-${abbr}-${i}`}
            dx={i === 0 ? 0 : 6}
            fontWeight={abbr === "As" ? "bold" : "normal"}
            fill={abbr === "As" ? "#8B0000" : "black"}
            style={{ cursor: "pointer" }}
            onClick={() => handlePlanetClick(abbr)}
          >
            {abbr}
          </tspan>
        ))}
      </text>
    )
  }

  const renderSign = (house: number, x: number, y: number) => {
    const sign = signsByHouse[house]
    if (!sign) return null
    return (
      <text
        x={x}
        y={y}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize="10"
        fill="#999"
        className="pointer-events-none"
      >
        {sign}
      </text>
    )
  }

  const maybeGlow = (house: number, shape: React.ReactElement) => {
    const shouldGlow = highlightedHouses.includes(house)
    return React.cloneElement(shape, {
      filter: shouldGlow ? "url(#glow)" : undefined,
      fill: shouldGlow ? "gold" : "none",
      fillOpacity: shouldGlow ? 0.15 : 0,
    })
  }

  return (
    <svg
      className="astro-chart w-full max-w-xl mx-auto"
      viewBox="0 0 500 500"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor="gold" />
        </filter>
      </defs>

      <style>
        {`.st0{stroke:#000000;stroke-miterlimit:10;}`}
      </style>

      <g id="house-1">
        {maybeGlow(1, <rect x="161.24" y="36.23" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 338.203 389.7009)" />)}
        {renderPlanets(1, 250, 125)}
        {renderSign(1, 250, 230)}
      </g>

      <g id="house-2">
        {maybeGlow(2, <polygon className="st0" points="249.96,-0.31 124.7,124.96 -0.57,-0.31" />)}
        {renderPlanets(2, 125, 40)}
        {renderSign(2, 125, 105)}
      </g>

      <g id="house-3">
        {maybeGlow(3, <polygon className="st0" points="-0.42,-0.46 124.84,124.81 -0.42,250.07" />)}
        {renderPlanets(3, 50, 125)}
        {renderSign(3, 105, 125)}
      </g>

      <g id="house-4">
        {maybeGlow(4, <rect x="36.12" y="161.35" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 36.1475 514.8163)" />)}
        {renderPlanets(4, 125, 250)}
        {renderSign(4, 230, 250)}
      </g>

      <g id="house-5">
        {maybeGlow(5, <polygon className="st0" points="-0.42,249.77 124.84,375.04 -0.42,500.3" />)}
        {renderPlanets(5, 50, 375)}
        {renderSign(5, 105, 375)}
      </g>

      <g id="house-6">
        {maybeGlow(6, <polygon className="st0" points="124.7,374.89 249.96,500.15 -0.57,500.15" />)}
        {renderPlanets(6, 125, 460)}
        {renderSign(6, 125, 395)}
      </g>

      <g id="house-7">
        {maybeGlow(7, <rect x="161.24" y="286.46" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 161.263 816.8718)" />)}
        {renderPlanets(7, 250, 375)}
        {renderSign(7, 250, 270)}
      </g>

      <g id="house-8">
        {maybeGlow(8, <polygon className="st0" points="374.93,374.89 500.19,500.15 249.66,500.15" />)}
        {renderPlanets(8, 375, 460)}
        {renderSign(8, 375, 395)}
      </g>

      <g id="house-9">
        {maybeGlow(9, <polygon className="st0" points="500.04,249.77 500.04,500.3 374.78,375.04" />)}
        {renderPlanets(9, 450, 375)}
        {renderSign(9, 395, 375)}
      </g>

      <g id="house-10">
        {maybeGlow(10, <rect x="286.35" y="161.35" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 463.3184 691.7563)" />)}
        {renderPlanets(10, 375, 250)}
        {renderSign(10, 270, 250)}
      </g>

      <g id="house-11">
        {maybeGlow(11, <polygon className="st0" points="500.04,-0.46 500.04,250.07 374.78,124.81" />)}
        {renderPlanets(11, 450, 125)}
        {renderSign(11, 395, 125)}
      </g>

      <g id="house-12">
        {maybeGlow(12, <polygon className="st0" points="500.19,-0.31 374.93,124.96 249.66,-0.31" />)}
        {renderPlanets(12, 375, 40)}
        {renderSign(12, 375, 105)}
      </g>
    </svg>
  )
}
