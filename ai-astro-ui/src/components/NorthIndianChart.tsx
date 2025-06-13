// components/NorthIndianChart.tsx

export default function NorthIndianChart() {
  return (
    <div className="w-full max-w-md mx-auto mt-8">
      <svg
        viewBox="0 0 100 100"
        className="w-full h-auto"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Внешний ромб */}
        <polygon points="50,0 100,50 50,100 0,50" fill="white" stroke="black" strokeWidth="1" />

        {/* Центральный крест */}
        <line x1="0" y1="50" x2="100" y2="50" stroke="black" strokeWidth="1" />
        <line x1="50" y1="0" x2="50" y2="100" stroke="black" strokeWidth="1" />

        {/* Диагональные линии */}
        <line x1="0" y1="50" x2="50" y2="100" stroke="black" strokeWidth="1" />
        <line x1="50" y1="100" x2="100" y2="50" stroke="black" strokeWidth="1" />
        <line x1="100" y1="50" x2="50" y2="0" stroke="black" strokeWidth="1" />
        <line x1="50" y1="0" x2="0" y2="50" stroke="black" strokeWidth="1" />

        {/* Правильная последовательность домов против часовой стрелки */}
        <text x="25" y="22" fontSize="4" textAnchor="middle">1</text>  {/* верхний левый треугольник */}
        <text x="12" y="35" fontSize="4" textAnchor="middle">2</text>
        <text x="10" y="55" fontSize="4" textAnchor="middle">3</text>
        <text x="20" y="70" fontSize="4" textAnchor="middle">4</text>
        <text x="33" y="85" fontSize="4" textAnchor="middle">5</text>
        <text x="50" y="93" fontSize="4" textAnchor="middle">6</text>
        <text x="67" y="85" fontSize="4" textAnchor="middle">7</text>
        <text x="80" y="70" fontSize="4" textAnchor="middle">8</text>
        <text x="90" y="55" fontSize="4" textAnchor="middle">9</text>
        <text x="88" y="35" fontSize="4" textAnchor="middle">10</text>
        <text x="75" y="22" fontSize="4" textAnchor="middle">11</text>
        <text x="50" y="10" fontSize="4" textAnchor="middle">12</text>
      </svg>
    </div>
  )
}
