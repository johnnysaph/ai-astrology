import React, { useState } from "react";

type PlanetData = {
  planet: string;
  abbr: string;
  house: number;
  sign: string;
  degree: string;
  is_retrograde: boolean;
  nakshatra: string | null;
  sign_lord: string;
  nakshatra_lord: string | null;
  houses_ruled: number[];
  role: string;
  relation: string;
  aspects: number[];
};

type Props = {
  planets: PlanetData[];
  signsByHouse: Record<number, number>;
};

export default function AstroSvgMap({ planets, signsByHouse }: Props) {
  const [highlightedHouses, setHighlightedHouses] = useState<number[]>([]);

  const groupedByHouse: Record<number, PlanetData[]> = {};
  planets.forEach((p) => {
    if (!groupedByHouse[p.house]) {
      groupedByHouse[p.house] = [];
    }
    groupedByHouse[p.house].push(p);
  });

  const aspectsGroupedByHouse: Record<number, string[]> = {};
  planets.forEach((p) => {
    p.aspects.forEach((houseNum) => {
      if (!aspectsGroupedByHouse[houseNum]) {
        aspectsGroupedByHouse[houseNum] = [];
      }
      aspectsGroupedByHouse[houseNum].push(p.abbr);
    });
  });

  const handlePlanetClick = (abbr: string, houses: number[]) => {
    const alreadySelected =
      houses.length > 0 &&
      houses.every((h) => highlightedHouses.includes(h)) &&
      highlightedHouses.length === houses.length;

    setHighlightedHouses(alreadySelected ? [] : houses);
  };

	const renderPlanets = (house: number, x: number, y: number) => {
	  const items = groupedByHouse[house];
	  if (!items) return null;

	  const isVertical = [3, 5, 9, 11].includes(house);
	  const stepDx = 22; // шаг между планетами, можно настроить
	  const stepDy = 20;
	  const initialDy = -((items.length - 1) / 2) * stepDy;

	  if (isVertical) {
		return (
		  <text
			x={x}
			y={y}
			textAnchor="middle"
			dominantBaseline="middle"
			fontSize="15"
			fill="black"
		  >
			{items.map((p, i) => (
			  <tspan
				key={`${house}-${p.abbr}-${i}`}
				x={x}
				dy={i === 0 ? `${initialDy}px` : `${stepDy}px`}
				fontWeight={p.abbr === "As" ? "bold" : "normal"}
				fill={p.abbr === "As" ? "#8B0000" : "black"}
				style={{ cursor: "pointer" }}
				onClick={() => handlePlanetClick(p.abbr, p.houses_ruled)}
			  >
				{p.abbr}
			  </tspan>
			))}
		  </text>
		);
	  }

	  // Горизонтальные дома: фиксированные x для каждого tspan
	  const startX = x - ((items.length - 1) / 2) * stepDx;
	  const xCoords: number[] = [];

	  return (
		<text
		  y={y}
		  textAnchor="middle"
		  dominantBaseline="middle"
		  fontSize="15"
		  fill="black"
		>
		  {items.map((p, i) => {
			const thisX = startX + i * stepDx;
			xCoords.push(thisX);
			return (
			  <tspan
				key={`${house}-${p.abbr}-${i}`}
				x={thisX}
				fontWeight={p.abbr === "As" ? "bold" : "normal"}
				fill={p.abbr === "As" ? "#8B0000" : "black"}
				style={{ cursor: "pointer" }}
				onClick={() => handlePlanetClick(p.abbr, p.houses_ruled)}
			  >
				{p.abbr}
			  </tspan>
			);
		  })}
		</text>
	  );
	};

	const renderDegrees = (house: number, x: number, y: number) => {
	  const items = groupedByHouse[house];
	  if (!items) return null;

	  const isVertical = [3, 5, 9, 11].includes(house);
	  const stepDx = 22;
	  const stepDy = 20;
	  const initialDy = -((items.length - 1) / 2) * stepDy;

	  if (isVertical) {
		return (
		  <text
			x={x}
			y={y}
			textAnchor="middle"
			dominantBaseline="middle"
			fontSize="9"
			fill="#555"
		  >
			{items.map((p, i) => (
			  <tspan
				key={`${house}-${p.abbr}-deg-${i}`}
				x={x}
				dy={i === 0 ? `${initialDy}px` : `${stepDy}px`}
			  >
				{`${p.degree.replace("+", "").slice(0, 2)}°`}
			  </tspan>
			))}
		  </text>
		);
	  }

	  // Горизонтальные дома
	  const totalWidth = (items.length - 1) * stepDx;
	  const startX = x - totalWidth / 2;

	  return (
		<text
		  y={y}
		  textAnchor="middle"
		  dominantBaseline="middle"
		  fontSize="9"
		  fill="#555"
		>
		  {items.map((p, i) => (
			<tspan
			  key={`${house}-${p.abbr}-deg-${i}`}
			  x={startX + i * stepDx}
			>
			  {`${p.degree.replace("+", "").slice(0, 2)}°`}
			</tspan>
		  ))}
		</text>
	  );
	};

  const renderAspects = (house: number, x: number, y: number) => {
    const items = aspectsGroupedByHouse[house];
    if (!items) return null;

    const isVertical = [3, 5, 9, 11].includes(house);
    const stepDx = 4;
    const stepDy = 16;
    const initialDy = -((items.length - 1) / 2) * stepDy;

    const isAngleHouse = [4, 7, 10].includes(house);
	//const is7House = house === 7;
    const hasPlanets = (groupedByHouse[house]?.length || 0) > 0;
	const yCoord = isAngleHouse && !hasPlanets ? y - 30 : y
    //let yCoord = y;

	//if (!hasPlanets) {
	//	if (is4Or10House) {
	//		yCoord = y - 20;
	//	} else if (is7House) {
	//		yCoord = y + 20;
	//	}
	//}

    if (isVertical) {
      return (
        <text
          x={x}
          y={yCoord}
          textAnchor="middle"
          dominantBaseline="middle"
          fontSize="10"
          fill="#555"
        >
          {items.map((abbr, i) => (
            <tspan
              key={`${house}-aspect-${abbr}-${i}`}
              x={x}
              dy={i === 0 ? `${initialDy}px` : `${stepDy}px`}
            >
              {abbr}
            </tspan>
          ))}
        </text>
      );
    }

    return (
      <text
        x={x}
        y={yCoord}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize="10"
        fill="#555"
      >
        {items.map((abbr, i) => (
          <tspan
            key={`${house}-aspect-${abbr}-${i}`}
            dx={i === 0 ? undefined : `${stepDx}px`}
          >
            {abbr}
          </tspan>
        ))}
      </text>
    );
  };

  const renderSign = (house: number, x: number, y: number) => {
    const sign = signsByHouse[house];
    if (!sign) return null;
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
    );
  };

  const maybeGlow = (house: number, shape: React.ReactElement) => {
    const shouldGlow = highlightedHouses.includes(house);
    return React.cloneElement(shape, {
      filter: shouldGlow ? "url(#glow)" : undefined,
      fill: shouldGlow ? "gold" : "none",
      fillOpacity: shouldGlow ? 0.15 : 0,
    });
  };

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

      <style>{`.st0{stroke:#000000;stroke-miterlimit:10;}`}</style>

      {/* Все 12 домов без изменений */}
      <g id="house-1">
        {maybeGlow(1, <rect x="161.24" y="36.23" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 338.203 389.7009)" />)}
        {renderPlanets(1, 250, 125)}
		{renderDegrees(1, 250, 137)}
        {renderAspects(1, 250, 95)}
        {renderSign(1, 250, 230)}
      </g>
      <g id="house-2">
        {maybeGlow(2, <polygon className="st0" points="249.96,-0.31 124.7,124.96 -0.57,-0.31" />)}
        {renderPlanets(2, 125, 15)}
		{renderDegrees(2, 125, 27)}
        {renderAspects(2, 125, 50)}
        {renderSign(2, 125, 105)}
      </g>
      <g id="house-3">
        {maybeGlow(3, <polygon className="st0" points="-0.42,-0.46 124.84,124.81 -0.42,250.07" />)}
        {renderPlanets(3, 15, 125)}
		{renderDegrees(3, 34, 125)}
        {renderAspects(3, 50, 125)}
        {renderSign(3, 105, 125)}
      </g>
      <g id="house-4">
        {maybeGlow(4, <rect x="36.12" y="161.35" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 36.1475 514.8163)" />)}
        {renderPlanets(4, 125, 250)}
		{renderDegrees(4, 125, 262)}
        {renderAspects(4, 125, 280)}
        {renderSign(4, 230, 250)}
      </g>
      <g id="house-5">
        {maybeGlow(5, <polygon className="st0" points="-0.42,249.77 124.84,375.04 -0.42,500.3" />)}
        {renderPlanets(5, 15, 375)}
		{renderDegrees(5, 34, 375)}
        {renderAspects(5, 50, 375)}
        {renderSign(5, 105, 375)}
      </g>
      <g id="house-6">
        {maybeGlow(6, <polygon className="st0" points="124.7,374.89 249.96,500.15 -0.57,500.15" />)}
        {renderPlanets(6, 125, 485)}
		{renderDegrees(6, 125, 472)}
        {renderAspects(6, 125, 450)}
        {renderSign(6, 125, 395)}
      </g>
      <g id="house-7">
        {maybeGlow(7, <rect x="161.24" y="286.46" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 161.263 816.8718)" />)}
        {renderPlanets(7, 250, 375)}
		{renderDegrees(7, 250, 387)}
        {renderAspects(7, 250, 405)}
        {renderSign(7, 250, 270)}
      </g>
      <g id="house-8">
        {maybeGlow(8, <polygon className="st0" points="374.93,374.89 500.19,500.15 249.66,500.15" />)}
        {renderPlanets(8, 375, 485)}
		{renderDegrees(8, 375, 472)}
        {renderAspects(8, 375, 450)}
        {renderSign(8, 375, 395)}
      </g>
      <g id="house-9">
        {maybeGlow(9, <polygon className="st0" points="500.04,249.77 500.04,500.3 374.78,375.04" />)}
        {renderPlanets(9, 485, 375)}
		{renderDegrees(9, 468, 375)}
        {renderAspects(9, 450, 375)}
        {renderSign(9, 395, 375)}
      </g>
      <g id="house-10">
        {maybeGlow(10, <rect x="286.35" y="161.35" className="st0" width="177.15" height="177.15"
          transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 463.3184 691.7563)" />)}
        {renderPlanets(10, 375, 250)}
		{renderDegrees(10, 375, 262)}
        {renderAspects(10, 375, 280)}
        {renderSign(10, 270, 250)}
      </g>
      <g id="house-11">
        {maybeGlow(11, <polygon className="st0" points="500.04,-0.46 500.04,250.07 374.78,124.81" />)}
        {renderPlanets(11, 485, 125)}
		{renderDegrees(11, 468, 125)}
        {renderAspects(11, 450, 125)}
        {renderSign(11, 395, 125)}
      </g>
      <g id="house-12">
        {maybeGlow(12, <polygon className="st0" points="500.19,-0.31 374.93,124.96 249.66,-0.31" />)}
        {renderPlanets(12, 375, 15)}
		{renderDegrees(12, 375, 27)}
        {renderAspects(12, 375, 50)}
        {renderSign(12, 375, 105)}
      </g>
    </svg>
  );
}
