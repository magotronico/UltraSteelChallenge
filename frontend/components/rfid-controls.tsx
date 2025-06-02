"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Play, Square, Edit3, Loader2, AlertCircle, CheckCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "https://d594-131-178-102-168.ngrok-free.app"; // Fallback to a default if not found

export function RFIDControls({ onStatusChange }: { onStatusChange: (status: "idle" | "reading" | "writing") => void }) {
  const [status, setStatus] = useState<"idle" | "reading" | "writing">("idle")
  const [tagData, setTagData] = useState("")
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const showMessage = (type: "success" | "error", text: string) => {
    setMessage({ type, text })
    setTimeout(() => setMessage(null), 5000)
  }

  const handleStartReading = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/start_reading`, {
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
      showMessage("success", data.message || "RFID reading started successfully")
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
    if (!tagData.trim()) return

    setStatus("writing")
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/write_tag?data=${encodeURIComponent(tagData.trim())}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setTagData("")
      showMessage("success", data.message || "Data written to RFID tag successfully")
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
            <CardDescription>Start or stop RFID tag scanning</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Button onClick={handleStartReading} disabled={status === "reading" || isLoading} className="flex-1">
                {status === "reading" ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Reading...
                  </>
                ) : isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Starting...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Start Reading
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
              {status === "reading" ? "RFID reader is actively scanning for tags..." : "RFID reader is stopped"}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Write to RFID Tag</CardTitle>
            <CardDescription>Manually write data to an RFID tag</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
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
              />
            </div>
            <Button
              onClick={handleWriteTag}
              disabled={!tagData.trim() || status === "writing" || isLoading}
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
