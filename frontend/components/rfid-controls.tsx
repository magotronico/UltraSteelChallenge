"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Play, Square, Edit3, Loader2, AlertCircle, CheckCircle, ArrowRight, ArrowLeft } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { JulianDatePicker } from "@/components/ui/julian-date-picker"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://10.22.206.2:8000"

export function RFIDControls({ onStatusChange }: { onStatusChange: (status: "idle" | "reading" | "writing") => void }) {
  const [status, setStatus] = useState<"idle" | "reading" | "writing">("idle")
  const [tagData, setTagData] = useState("")
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isExitMode, setIsExitMode] = useState(false) // false = entrance, true = exit
  const [isAdvancedWriteMode, setIsAdvancedWriteMode] = useState(false) // false = simple, true = advanced form

  // Form data for advanced write mode
  const [formData, setFormData] = useState({
    sku: "",
    lot: "",
    uid: "",
    received_by: "",
    date: "",
  })

  const showMessage = (type: "success" | "error", text: string) => {
    setMessage({ type, text })
    setTimeout(() => setMessage(null), 5000)
  }

  // Generate Julian date format (%j%y) - day of year + 2-digit year
  const generateJulianDate = () => {
    const now = new Date()
    const start = new Date(now.getFullYear(), 0, 0)
    const diff = now.getTime() - start.getTime()
    const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24))
    const twoDigitYear = now.getFullYear().toString().slice(-2)
    return `${dayOfYear.toString().padStart(3, "0")}${twoDigitYear}`
  }

  const handleAutoFillDate = () => {
    setFormData({ ...formData, date: generateJulianDate() })
  }

  // Function to generate tag data from form fields
  const generateTagDataFromForm = () => {
    // Concatenate fields, limiting to 12 characters total
    const combinedData = `${formData.sku || ""}${formData.lot || ""}${formData.uid || ""}${formData.received_by || ""}${formData.date || ""}`
    return combinedData.substring(0, 12) // Limit to 12 characters
  }

  const handleStartReading = async () => {
    setIsLoading(true)
    try {
      const endpoint = isExitMode ? "/start_reading_exits" : "/start_reading"
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setStatus("reading")
      onStatusChange("reading")
      showMessage("success", data.message || `RFID ${isExitMode ? "exit" : "entrance"} reading started successfully`)
    } catch (error) {
      console.error("Error starting RFID reading:", error)
      showMessage("error", `Failed to start RFID reading: ${error instanceof Error ? error.message : "Unknown error"}`)
      onStatusChange("idle")
    } finally {
      setIsLoading(false)
    }
  }

  const handleStopReading = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/stop_reading`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setStatus("idle")
      onStatusChange("idle")
      showMessage("success", data.message || "RFID reading stopped successfully")
    } catch (error) {
      console.error("Error stopping RFID reading:", error)
      showMessage("error", `Failed to stop RFID reading: ${error instanceof Error ? error.message : "Unknown error"}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleWriteTag = async () => {
    // Use either simple tag data or generate from form based on mode
    const dataToWrite = isAdvancedWriteMode ? generateTagDataFromForm() : tagData.trim()

    if (!dataToWrite) {
      showMessage("error", "Please enter data to write to the tag")
      return
    }

    if (dataToWrite.length > 12) {
      showMessage("error", "Tag data cannot exceed 12 characters")
      return
    }

    setStatus("writing")
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/write_tag?data=${encodeURIComponent(dataToWrite)}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      // Reset form or simple input based on mode
      if (isAdvancedWriteMode) {
        setFormData({
          sku: "",
          lot: "",
          uid: "",
          received_by: "",
          date: "",
        })
      } else {
        setTagData("")
      }

      showMessage("success", data.message || `Data "${dataToWrite}" written to RFID tag successfully`)
    } catch (error) {
      console.error("Error writing to RFID tag:", error)
      showMessage("error", `Failed to write to RFID tag: ${error instanceof Error ? error.message : "Unknown error"}`)
    } finally {
      setStatus("idle")
      onStatusChange("idle")
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      {message && (
        <Alert variant={message.type === "error" ? "destructive" : "default"}>
          {message.type === "error" ? <AlertCircle className="h-4 w-4" /> : <CheckCircle className="h-4 w-4" />}
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              RFID Reader Control
              <Badge variant={status === "reading" ? "default" : "secondary"}>
                {status === "reading" ? "Active" : "Inactive"}
              </Badge>
            </CardTitle>
            <CardDescription>
              Start or stop RFID tag scanning for {isExitMode ? "exit" : "entrance"} tracking
            </CardDescription>

            {/* Mode Toggle - moved here */}
            <div className="flex items-center justify-between pt-2 border-t">
              <div className="flex items-center space-x-2">
                <ArrowRight className="h-4 w-4 text-green-600" />
                <Label htmlFor="mode-toggle" className="text-sm font-medium">
                  Entrance
                </Label>
              </div>
              <Switch
                id="mode-toggle"
                checked={isExitMode}
                onCheckedChange={setIsExitMode}
                disabled={status === "reading"}
              />
              <div className="flex items-center space-x-2">
                <Label htmlFor="mode-toggle" className="text-sm font-medium">
                  Exit
                </Label>
                <ArrowLeft className="h-4 w-4 text-red-600" />
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Button onClick={handleStartReading} disabled={status === "reading" || isLoading} className="flex-1">
                {status === "reading" ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Reading {isExitMode ? "Exits" : "Entrances"}...
                  </>
                ) : isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Starting...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Start {isExitMode ? "Exit" : "Entrance"} Reading
                  </>
                )}
              </Button>
              <Button
                onClick={handleStopReading}
                disabled={status !== "reading" || isLoading}
                variant="outline"
                className="flex-1"
              >
                {isLoading && status === "reading" ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Stopping...
                  </>
                ) : (
                  <>
                    <Square className="mr-2 h-4 w-4" />
                    Stop Reading
                  </>
                )}
              </Button>
            </div>
            <div className="text-sm text-muted-foreground">
              {status === "reading"
                ? `RFID reader is actively scanning for ${isExitMode ? "exit" : "entrance"} tags...`
                : "RFID reader is stopped"}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Write to RFID Tag</CardTitle>
            <CardDescription>Manually write data to an RFID tag</CardDescription>

            {/* Toggle for simple/advanced write mode */}
            <div className="flex items-center justify-between pt-2 border-t">
              <div className="flex items-center space-x-2">
                <Label htmlFor="write-mode-toggle" className="text-sm font-medium">
                  Simple
                </Label>
              </div>
              <Switch
                id="write-mode-toggle"
                checked={isAdvancedWriteMode}
                onCheckedChange={setIsAdvancedWriteMode}
                disabled={status === "writing"}
              />
              <div className="flex items-center space-x-2">
                <Label htmlFor="write-mode-toggle" className="text-sm font-medium">
                  Advanced
                </Label>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {isAdvancedWriteMode ? (
              // Advanced form mode
              <>
                <div className="text-xs text-muted-foreground mb-2">
                  Fields will be concatenated and limited to 12 characters
                </div>

                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <Label htmlFor="sku" className="text-xs">
                        SKU
                      </Label>
                      <Input
                        id="sku"
                        placeholder="e.g., 5"
                        value={formData.sku}
                        onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                        disabled={status === "writing" || isLoading}
                        className="h-8 text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="lot" className="text-xs">
                        Lot
                      </Label>
                      <Input
                        id="lot"
                        placeholder="e.g., A6"
                        value={formData.lot}
                        onChange={(e) => setFormData({ ...formData, lot: e.target.value })}
                        disabled={status === "writing" || isLoading}
                        className="h-8 text-sm"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <Label htmlFor="uid" className="text-xs">
                        UID
                      </Label>
                      <Input
                        id="uid"
                        placeholder="e.g., B3"
                        value={formData.uid}
                        onChange={(e) => setFormData({ ...formData, uid: e.target.value })}
                        disabled={status === "writing" || isLoading}
                        className="h-8 text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="received_by" className="text-xs">
                        Received By
                      </Label>
                      <Input
                        id="received_by"
                        placeholder="e.g., DC"
                        value={formData.received_by}
                        onChange={(e) => setFormData({ ...formData, received_by: e.target.value.toUpperCase() })}
                        disabled={status === "writing" || isLoading}
                        className="h-8 text-sm"
                        style={{ textTransform: "uppercase" }}
                        maxLength={5}
                      />
                    </div>
                  </div>

                  <JulianDatePicker
                    id="date"
                    label="Date"
                    value={formData.date}
                    onChange={(value: any) => setFormData({ ...formData, date: value })}
                    placeholder="Julian date"
                    disabled={status === "writing" || isLoading}
                    className="flex-1"
                  />

                  <div className="pt-1">
                    <div className="flex items-center justify-between mb-1">
                      <Label className="text-xs">Preview:</Label>
                      <span className="text-xs text-muted-foreground">{generateTagDataFromForm().length}/12 chars</span>
                    </div>
                    <div className="bg-muted p-2 rounded text-sm font-mono overflow-hidden">
                      {generateTagDataFromForm() || "Empty"}
                    </div>
                  </div>
                </div>
              </>
            ) : (
              // Simple mode
              <div className="space-y-2">
                <Label htmlFor="tag-data">Tag Data</Label>
                <Input
                  id="tag-data"
                  placeholder="Enter data to write to tag..."
                  value={tagData}
                  onChange={(e) => setTagData(e.target.value)}
                  disabled={status === "writing" || isLoading}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && tagData.trim()) {
                      handleWriteTag()
                    }
                  }}
                  maxLength={12}
                />
                <div className="text-xs text-right text-muted-foreground">{tagData.length}/12 characters</div>
              </div>
            )}

            <Button
              onClick={handleWriteTag}
              disabled={
                (isAdvancedWriteMode ? !generateTagDataFromForm() : !tagData.trim()) ||
                status === "writing" ||
                isLoading
              }
              className="w-full"
            >
              {status === "writing" ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Writing...
                </>
              ) : (
                <>
                  <Edit3 className="mr-2 h-4 w-4" />
                  Write to Tag
                </>
              )}
            </Button>
            <div className="text-sm text-muted-foreground">
              Place an RFID tag near the writer and click the button above
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
