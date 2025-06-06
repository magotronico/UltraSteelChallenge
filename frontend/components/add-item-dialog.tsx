"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast"
import { Plus, Loader2, Info } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { JulianDatePicker } from "@/components/ui/julian-date-picker"
import type { InventoryItem } from "@/types/inventory"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://10.22.193.238:8000"

interface AddItemDialogProps {
  onItemAdded: () => void
}

export function AddItemDialog({ onItemAdded }: AddItemDialogProps) {
  const [open, setOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    sku: "",
    lot: "",
    uid: "",
    received_by: "",
    date: "",
    price: "",
  })
  const { toast } = useToast()

  // Generate Julian date format (%j%y) - day of year + 2-digit year
  const generateJulianDate = () => {
    const now = new Date()
    const start = new Date(now.getFullYear(), 0, 0)
    const diff = now.getTime() - start.getTime()
    const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24))
    const twoDigitYear = now.getFullYear().toString().slice(-2)
    return `${dayOfYear.toString().padStart(3, "0")}${twoDigitYear}`
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const item: InventoryItem = {
        sku: formData.sku.trim(),
        lot: formData.lot.trim(),
        uid: formData.uid.trim(),
        received_by: formData.received_by.trim().toUpperCase(),
        date: formData.date || generateJulianDate(),
        status: "1", // Active by default
        price: formData.price ? Number.parseFloat(formData.price) : undefined,
      }

      const response = await fetch(`${API_BASE_URL}/add_manually`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(item),
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error("Server Response Error: ", errorData)
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      toast({
        title: "Item Added Successfully",
        description: `Item "${formData.sku}" has been added to inventory`,
      })

      // Reset form
      setFormData({
        sku: "",
        lot: "",
        uid: "",
        received_by: "",
        date: "",
        price: "",
      })
      setOpen(false)
      onItemAdded()
    } catch (error) {
      console.error("Error adding item:", error)
      toast({
        title: "Error Adding Item",
        description: error instanceof Error ? error.message : "Failed to add item to inventory",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="sm" className="w-full">
          <Plus className="mr-2 h-4 w-4" />
          Add Item
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px] max-h-[90vh] overflow-hidden flex flex-col p-0">
        <DialogHeader className="p-6 pb-2">
          <DialogTitle>Add New Item</DialogTitle>
          <DialogDescription>Add a new item to your inventory manually</DialogDescription>
        </DialogHeader>

        <div className="overflow-y-auto px-6 flex-1" style={{ maxHeight: "calc(90vh - 180px)" }}>
          <Alert className="mb-4">
            <Info className="h-4 w-4" />
            <AlertDescription>Date format: Julian day + 2-digit year (e.g., 22125 = day 221 of 2025)</AlertDescription>
          </Alert>

          <form id="add-item-form" onSubmit={handleSubmit} className="space-y-4 pb-4">
            <div className="grid gap-2">
              <Label htmlFor="sku">SKU *</Label>
              <Input
                id="sku"
                placeholder="What the item is (e.g., 5)"
                value={formData.sku}
                onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="lot">Lot Number *</Label>
              <Input
                id="lot"
                placeholder="Lot number for tracking (e.g., A6)"
                value={formData.lot}
                onChange={(e) => setFormData({ ...formData, lot: e.target.value })}
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="uid">UID *</Label>
              <Input
                id="uid"
                placeholder="Unique identifier (e.g., B3)"
                value={formData.uid}
                onChange={(e) => setFormData({ ...formData, uid: e.target.value })}
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="received_by">Received By *</Label>
              <Input
                id="received_by"
                placeholder="Initials (e.g., DC)"
                value={formData.received_by}
                onChange={(e) => setFormData({ ...formData, received_by: e.target.value })}
                maxLength={5}
                style={{ textTransform: "uppercase" }}
                required
              />
            </div>

            <JulianDatePicker
              id="date"
              label="Date (Julian Format)"
              value={formData.date}
              onChange={(value: any) => setFormData({ ...formData, date: value })}
              placeholder="e.g., 22125 (leave empty for today)"
              disabled={isLoading}
            />

            <div className="grid gap-2">
              <Label htmlFor="price">Price (Optional)</Label>
              <Input
                id="price"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
              />
            </div>
          </form>
        </div>

        <DialogFooter className="p-6 pt-4 border-t">
          <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" form="add-item-form" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Adding...
              </>
            ) : (
              "Add Item"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
