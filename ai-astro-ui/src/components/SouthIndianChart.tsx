import { useState } from "react"

type Props = {
  name: string
  planets: { abbr: string; house: number; degree: string; is_retrograde: boolean; houses_ruled: number[]; aspects: number[] }[]
  signsByHouse: Record<number, number>
}

const signs = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
const layout = [12, 1, 2, 3, 11, 4, 10, 5, 9, 8, 7, 6]

function wholeDegrees(degree: string) {
  return degree.replace(/^\+/, "").split(":")[0]
}

function degreeInArcseconds(degree: string) {
  const [degrees, minutes = 0, seconds = 0] = degree.split(":").map(Number)
  return degrees * 3600 + minutes * 60 + seconds
}

export default function SouthIndianChart({ name, planets, signsByHouse }: Props) {
  const [highlightedHouses, setHighlightedHouses] = useState<number[]>([])
  const housesBySign = new Map(Object.entries(signsByHouse).map(([house, sign]) => [sign, Number(house)]))

  function toggleHouses(houses: number[]) {
    setHighlightedHouses((current) => (
      current.length === houses.length && houses.every((house) => current.includes(house)) ? [] : houses
    ))
  }

  return (
    <div role="group" aria-label={`Южноиндийская карта: ${name}`} className="grid size-full grid-cols-4 grid-rows-4 gap-px overflow-hidden border border-[color:var(--chart-line)] bg-[color:var(--chart-line)]">
      <div className="col-span-2 col-start-2 row-span-2 row-start-2 grid place-items-center bg-background p-2 text-center text-sm font-semibold sm:text-base">
        {name}
      </div>
      {layout.map((sign) => {
        const house = housesBySign.get(sign)
        const isHighlighted = house !== undefined && highlightedHouses.includes(house)
        const housePlanets = planets.filter((planet) => planet.house === house).sort(
          (a, b) => degreeInArcseconds(a.degree) - degreeInArcseconds(b.degree)
        )
        const aspectingPlanets = house === undefined ? [] : planets.filter((planet) => planet.aspects.includes(house))
        return (
          <div
            key={sign}
            className="flex min-h-0 min-w-0 flex-col overflow-hidden bg-background px-1 py-1 sm:px-2"
            style={isHighlighted ? { backgroundColor: "color-mix(in srgb, var(--chart-highlight) 15%, var(--background))" } : undefined}
          >
            <div className="flex shrink-0 justify-between text-[10px] leading-4 sm:text-xs">
              <span className="text-muted-foreground">{signs[sign - 1]}</span>
              <span className={house === 1 ? "font-semibold text-primary" : "text-muted-foreground"} aria-label={`Дом ${house}`}>
                {house}
              </span>
            </div>
            <div className="grid min-h-0 flex-1 place-items-center overflow-y-auto">
              <ul className="flex flex-wrap justify-center gap-x-1.5 gap-y-1 text-center text-xs leading-tight tabular-nums sm:gap-x-2 sm:text-sm">
                {housePlanets.map((planet) => (
                  <li key={planet.abbr} className={`flex flex-col items-center ${planet.abbr === "As" ? "text-[color:var(--chart-ascendant)]" : "text-[color:var(--chart-planet)]"}`}>
                    {planet.houses_ruled.length > 0 ? (
                      <button type="button" className="cursor-pointer font-semibold" aria-label={`${planet.abbr}: подсветить дома ${planet.houses_ruled.join(", ")}`} onClick={() => toggleHouses(planet.houses_ruled)}>
                        {planet.abbr}{planet.is_retrograde && <sup>R</sup>}
                      </button>
                    ) : (
                      <span className="font-semibold">{planet.abbr}{planet.is_retrograde && <sup>R</sup>}</span>
                    )}
                    <span className={`text-[10px] sm:text-xs ${planet.abbr === "As" ? "text-current" : "text-muted-foreground"}`}>{wholeDegrees(planet.degree)}°</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="min-h-4 shrink-0 text-center text-[10px] leading-4 text-gray-500 dark:text-gray-300 sm:text-xs">
              {aspectingPlanets.length > 0 && (
                <span title="Планеты, аспектирующие этот дом">
                  <span className="sr-only">Аспекты: </span>
                  {aspectingPlanets.map((planet) => planet.abbr).join(" ")}
                </span>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
