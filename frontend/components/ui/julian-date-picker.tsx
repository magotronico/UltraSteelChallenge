"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { CalendarIcon, Clock, ChevronLeft, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"

interface JulianDatePickerProps {
  id: string
  label: string
  value: string
  onChange: (value: string) => void
  placeholder?: string
  required?: boolean
  disabled?: boolean
  className?: string
}

export function JulianDatePicker({
  id,
  label,
  value,
  onChange,
  placeholder = "e.g., 22125",
  required = false,
  disabled = false,
  className,
}: JulianDatePickerProps) {
  const [isCalendarOpen, setIsCalendarOpen] = useState(false)
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth())
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear())

  // Generate Julian date format (%j%y) - day of year + 2-digit year
  const generateJulianDate = (selectedDate?: Date) => {
    const targetDate = selectedDate || new Date()
    const start = new Date(targetDate.getFullYear(), 0, 0)
    const diff = targetDate.getTime() - start.getTime()
    const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24))
    const twoDigitYear = targetDate.getFullYear().toString().slice(-2)
    return `${dayOfYear.toString().padStart(3, "0")}${twoDigitYear}`
  }

  // Convert Julian date back to regular date for display
  const parseJulianDate = (julianStr: string) => {
    if (!julianStr || julianStr.length !== 5) return null

    try {
      const dayOfYear = Number.parseInt(julianStr.substring(0, 3))
      const year = 2000 + Number.parseInt(julianStr.substring(3, 5))

      const date = new Date(year, 0, dayOfYear)
      return date
    } catch {
      return null
    }
  }

  const handleDateSelect = (day: number) => {
    const selectedDate = new Date(currentYear, currentMonth, day)
    const julianDate = generateJulianDate(selectedDate)
    onChange(julianDate)
    setIsCalendarOpen(false)
  }

  const handleTodayClick = () => {
    const today = new Date()
    setCurrentMonth(today.getMonth())
    setCurrentYear(today.getFullYear())
    onChange(generateJulianDate(today))
  }

  const handleInputChange = (inputValue: string) => {
    onChange(inputValue)
  }

  // Get display date for the calendar
  const displayDate = parseJulianDate(value)

  // Calendar generation
  const getDaysInMonth = (month: number, year: number) => {
    return new Date(year, month + 1, 0).getDate()
  }

  const getFirstDayOfMonth = (month: number, year: number) => {
    return new Date(year, month, 1).getDay()
  }

  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ]

  const renderCalendar = () => {
    const daysInMonth = getDaysInMonth(currentMonth, currentYear)
    const firstDay = getFirstDayOfMonth(currentMonth, currentYear)
    const days = []

    // Empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="w-8 h-8" />)
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const isSelected =
        displayDate &&
        displayDate.getDate() === day &&
        displayDate.getMonth() === currentMonth &&
        displayDate.getFullYear() === currentYear

      const isToday =
        new Date().getDate() === day &&
        new Date().getMonth() === currentMonth &&
        new Date().getFullYear() === currentYear

      days.push(
        <button
          key={day}
          type="button"
          onClick={() => handleDateSelect(day)}
          className={cn(
            "w-8 h-8 text-sm rounded-md hover:bg-accent hover:text-accent-foreground",
            isSelected && "bg-primary text-primary-foreground",
            isToday && !isSelected && "bg-accent text-accent-foreground font-medium",
          )}
        >
          {day}
        </button>,
      )
    }

    return days
  }

  const navigateMonth = (direction: "prev" | "next") => {
    if (direction === "prev") {
      if (currentMonth === 0) {
        setCurrentMonth(11)
        setCurrentYear(currentYear - 1)
      } else {
        setCurrentMonth(currentMonth - 1)
      }
    } else {
      if (currentMonth === 11) {
        setCurrentMonth(0)
        setCurrentYear(currentYear + 1)
      } else {
        setCurrentMonth(currentMonth + 1)
      }
    }
  }

  const formatDisplayDate = (date: Date) => {
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  return (
    <div className={cn("grid gap-2", className)}>
      <Label htmlFor={id} className="flex items-center gap-2">
        {label}
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={handleTodayClick}
          disabled={disabled}
          className="h-6 px-2 text-xs"
        >
          <Clock className="mr-1 h-3 w-3" />
          Today
        </Button>
      </Label>

      <div className="flex gap-2">
        <Input
          id={id}
          placeholder={placeholder}
          value={value}
          onChange={(e) => handleInputChange(e.target.value)}
          pattern="[0-9]{5}"
          maxLength={5}
          required={required}
          disabled={disabled}
          className="flex-1"
        />

        <Popover open={isCalendarOpen} onOpenChange={setIsCalendarOpen}>
          <PopoverTrigger asChild>
            <Button variant="outline" size="sm" disabled={disabled} className="w-10 p-0">
              <CalendarIcon className="h-4 w-4" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0" align="end">
            <div className="p-3 border-b">
              <p className="text-sm font-medium">Select Date</p>
              {displayDate && (
                <p className="text-xs text-muted-foreground">
                  Current: {formatDisplayDate(displayDate)} → {value}
                </p>
              )}
            </div>

            {/* Calendar Header */}
            <div className="flex items-center justify-between p-3 border-b">
              <Button variant="outline" size="sm" onClick={() => navigateMonth("prev")} className="h-7 w-7 p-0">
                <ChevronLeft className="h-4 w-4" />
              </Button>

              <div className="text-sm font-medium">
                {monthNames[currentMonth]} {currentYear}
              </div>

              <Button variant="outline" size="sm" onClick={() => navigateMonth("next")} className="h-7 w-7 p-0">
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>

            {/* Calendar Grid */}
            <div className="p-3">
              {/* Day headers */}
              <div className="grid grid-cols-7 gap-1 mb-2">
                {["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"].map((day) => (
                  <div
                    key={day}
                    className="w-8 h-6 text-xs font-medium text-muted-foreground flex items-center justify-center"
                  >
                    {day}
                  </div>
                ))}
              </div>

              {/* Calendar days */}
              <div className="grid grid-cols-7 gap-1">{renderCalendar()}</div>
            </div>
          </PopoverContent>
        </Popover>
      </div>

      {value && (
        <div className="text-xs text-muted-foreground">
          Julian: {value}
          {displayDate && ` (${formatDisplayDate(displayDate)})`}
        </div>
      )}
    </div>
  )
}
