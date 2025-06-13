import React from "react"

type PlanetData = {
  "Планета": string
  "Дом": number
}

type Props = {
  planets: PlanetData[]
}

const planetAbbr: Record<string, string> = {
  "Асцендент": "As",
  "Солнце": "Su",
  "Луна": "Mo",
  "Марс": "Ma",
  "Меркурий": "Me",
  "Юпитер": "Ju",
  "Венера": "Ve",
  "Сатурн": "Sa",
  "Раху": "Ra",
  "Кету": "Ke",
}

export default function AstroSvgMap({ planets }: Props) {
  const groupedByHouse: Record<number, string[]> = {}

  // Группировка планет по дому
  planets.forEach(p => {
    const abbr = planetAbbr[p["Планета"]] || p["Планета"]
    if (!groupedByHouse[p["Дом"]]) {
      groupedByHouse[p["Дом"]] = []
    }
    groupedByHouse[p["Дом"]].push(abbr)
  })

  // Утилита отрисовки подписей планет по центру домов
  const renderPlanets = (house: number, x: number, y: number) => {
    const items = groupedByHouse[house]
    if (!items) return null

    return (
      <text
        x={x}
        y={y} // смещение вниз для оптического центрирования
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize="12"
        fill="black"
        className="pointer-events-none"
      >
        {items.map((abbr, i) => (
          <tspan
            key={`${house}-${abbr}-${i}`}
            dx={i === 0 ? 0 : 6}
            fontWeight={abbr === "As" ? "bold" : "normal"}
            fill={abbr === "As" ? "#8B0000" : "black"}
          >
            {abbr}
          </tspan>
        ))}
      </text>
    )
  }

  return (
    <svg
      className="astro-chart w-full max-w-xl mx-auto"
      viewBox="0 0 500 500"
      xmlns="http://www.w3.org/2000/svg"
    >
      <style>
        {`.st0{fill:none;stroke:#000000;stroke-miterlimit:10;}`}
      </style>

      <g id="house-1">
        <rect x="161.24" y="36.23" className="st0" width="177.15" height="177.15"
              transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 338.203 389.7009)" />
        {renderPlanets(1, 250, 125)}
      </g>

      <g id="house-2">
        <polygon className="st0" points="249.96,-0.31 124.7,124.96 -0.57,-0.31" />
        {renderPlanets(2, 125, 40)}
      </g>

      <g id="house-3">
        <polygon className="st0" points="-0.42,-0.46 124.84,124.81 -0.42,250.07" />
        {renderPlanets(3, 50, 125)}
      </g>

      <g id="house-4">
        <rect x="36.12" y="161.35" className="st0" width="177.15" height="177.15"
              transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 36.1475 514.8163)" />
        {renderPlanets(4, 125, 250)}
      </g>

      <g id="house-5">
        <polygon className="st0" points="-0.42,249.77 124.84,375.04 -0.42,500.3" />
        {renderPlanets(5, 50, 375)}
      </g>

      <g id="house-6">
        <polygon className="st0" points="124.7,374.89 249.96,500.15 -0.57,500.15" />
        {renderPlanets(6, 125, 460)}
      </g>

      <g id="house-7">
        <rect x="161.24" y="286.46" className="st0" width="177.15" height="177.15"
              transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 161.263 816.8718)" />
        {renderPlanets(7, 250, 375)}
      </g>

      <g id="house-8">
        <polygon className="st0" points="374.93,374.89 500.19,500.15 249.66,500.15" />
        {renderPlanets(8, 375, 460)}
      </g>

      <g id="house-9">
        <polygon className="st0" points="500.04,249.77 500.04,500.3 374.78,375.04" />
        {renderPlanets(9, 450, 375)}
      </g>

      <g id="house-10">
        <rect x="286.35" y="161.35" className="st0" width="177.15" height="177.15"
              transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 463.3184 691.7563)" />
        {renderPlanets(10, 375, 250)}
      </g>

      <g id="house-11">
        <polygon className="st0" points="500.04,-0.46 500.04,250.07 374.78,124.81" />
        {renderPlanets(11, 450, 125)}
      </g>

      <g id="house-12">
        <polygon className="st0" points="500.19,-0.31 374.93,124.96 249.66,-0.31" />
        {renderPlanets(12, 375, 40)}
      </g>
    </svg>
  )
}
