"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

type PlaceSuggestion = {
  display_name: string
  lat: string
  lon: string
}

export function BirthForm() {
  const [date, setDate] = useState("")
  const [time, setTime] = useState("")
  const [place, setPlace] = useState("")
  const [lat, setLat] = useState("")
  const [lon, setLon] = useState("")
  const [suggestions, setSuggestions] = useState<PlaceSuggestion[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const isFormValid = Boolean(parseDate(date) && parseTime(time) && lat && lon)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const parsedDate = parseDate(date)
    const parsedTime = parseTime(time)

    if (!parsedDate || !parsedTime || !lat || !lon) {
      alert("Пожалуйста, заполните все поля корректно")
      return
    }

    const formattedDate = date
    const formattedTime = time

    try {
      setIsLoading(true)

      const response = await fetch("https://ai-astrology-api.onrender.com/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          date: formattedDate,
          time: formattedTime,
          lat: parseFloat(lat),
          lon: parseFloat(lon)
        })
      })

      const data = await response.json()
      console.log("🌟 Ответ от сервера:", data)
    } catch (error) {
      console.error("Ошибка при вызове API:", error)
      alert("Произошла ошибка при расчёте карты")
    } finally {
      setIsLoading(false)
    }
  }

  function parseDate(input: string): Date | null {
    const [d, m, y] = input.split(".")
    if (!d || !m || !y) return null
    const day = parseInt(d, 10)
    const month = parseInt(m, 10) - 1
    const year = parseInt(y, 10)
    const date = new Date(year, month, day)
    if (
      date.getFullYear() !== year ||
      date.getMonth() !== month ||
      date.getDate() !== day
    ) return null
    return date
  }

  function parseTime(input: string): { hours: number, minutes: number, seconds: number } | null {
    const [h, m, s] = input.split(":")
    if (!h || !m || !s) return null
    const hours = parseInt(h, 10)
    const minutes = parseInt(m, 10)
    const seconds = parseInt(s, 10)
    if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59 || seconds < 0 || seconds > 59) return null
    return { hours, minutes, seconds }
  }

  function formatDateInput(input: string): string {
    const digits = input.replace(/\D/g, "").slice(0, 8)
    const parts = [digits.slice(0, 2), digits.slice(2, 4), digits.slice(4, 8)]
    return parts.filter(Boolean).join(".")
  }

  function formatTimeInput(input: string): string {
    const digits = input.replace(/\D/g, "").slice(0, 6)
    const parts = [digits.slice(0, 2), digits.slice(2, 4), digits.slice(4, 6)]
    return parts.filter(Boolean).join(":")
  }

  async function fetchSuggestions(query: string) {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&accept-language=ru&limit=5`)
    const data = await res.json()
    setSuggestions(data)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-sm mx-auto p-6 bg-white dark:bg-black rounded-xl shadow relative">
      {isLoading && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center"
          style={{ backgroundColor: "rgba(0, 0, 0, 0.25)" }}
        >
          <div className="text-white text-xl">Загрузка...</div>
        </div>
      )}

      <div className="space-y-2">
        <Label>Дата рождения</Label>
        <Input
          type="text"
          placeholder="дд.мм.гггг"
          value={date}
          onChange={(e) => setDate(formatDateInput(e.target.value))}
        />
      </div>

      <div className="space-y-2">
        <Label>Время рождения</Label>
        <Input
          type="text"
          placeholder="чч:мм:сс"
          value={time}
          onChange={(e) => setTime(formatTimeInput(e.target.value))}
        />
      </div>

      <div className="space-y-2 relative">
        <Label>Место рождения</Label>
        <Input
          type="text"
          value={place}
          onChange={(e) => {
            const val = e.target.value
            setPlace(val)
            setSuggestions([])
            if (val.length > 2) fetchSuggestions(val)
          }}
        />
        {suggestions.length > 0 && (
          <div className="absolute z-10 w-full bg-white border rounded shadow mt-1 max-h-48 overflow-auto text-sm">
            {suggestions.map((s, i) => (
              <div
                key={i}
                className="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                onClick={() => {
                  setPlace(s.display_name)
                  setLat(s.lat)
                  setLon(s.lon)
                  setSuggestions([])
                }}
              >
                {s.display_name}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-2">
        <Label>Широта</Label>
        <Input
          type="text"
          value={lat}
          onChange={(e) => setLat(e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label>Долгота</Label>
        <Input
          type="text"
          value={lon}
          onChange={(e) => setLon(e.target.value)}
        />
      </div>

      <Button
        type="submit"
        className={`w-full transform transition active:scale-95 ${isFormValid ? "cursor-pointer" : "cursor-default"}`}
        disabled={!isFormValid}
      >
        Построить карту
      </Button>
    </form>
  )
}
