"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast"
import { Loader2, Info } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { JulianDatePicker } from "@/components/ui/julian-date-picker"
import type { InventoryItem } from "@/types/inventory"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://10.22.206.2:8000"

interface EditItemDialogProps {
  item: InventoryItem
  open: boolean
  onOpenChange: (open: boolean) => void
  onItemUpdated: () => void
}

export function EditItemDialog({ item, open, onOpenChange, onItemUpdated }: EditItemDialogProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    sku: "",
    lot: "",
    uid: "",
    received_by: "",
    date: "",
    price: "",
    status: "1" as "1" | "0",
  })
  const { toast } = useToast()

  // Initialize form data when item changes
  useEffect(() => {
    if (item) {
      setFormData({
        sku: item.sku || "",
        lot: item.lot || "",
        uid: item.uid || "",
        received_by: item.received_by || "",
        date: item.date || "",
        price: item.price?.toString() || "",
        status: item.status || "1",
      })
    }
  }, [item])

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
      const updatedItem: InventoryItem = {
        sku: formData.sku.trim(),
        lot: formData.lot.trim(),
        uid: formData.uid.trim(),
        received_by: formData.received_by.trim().toUpperCase(),
        date: formData.date || generateJulianDate(),
        status: formData.status,
        price: formData.price ? Number.parseFloat(formData.price) : undefined,
      }

      const response = await fetch(`${API_BASE_URL}/update_item/${item.uid}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedItem),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      toast({
        title: "Item Updated Successfully",
        description: `Item "${formData.sku}" has been updated`,
      })

      onItemUpdated()
      onOpenChange(false)
    } catch (error) {
      console.error("Error updating item:", error)
      toast({
        title: "Error Updating Item",
        description: error instanceof Error ? error.message : "Failed to update item",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleStatusChange = (checked: boolean) => {
    setFormData({ ...formData, status: checked ? "1" : "0" })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px] max-h-[90vh] overflow-hidden flex flex-col p-0">
        <DialogHeader className="p-6 pb-2">
          <DialogTitle>Edit Item</DialogTitle>
          <DialogDescription>Update the item information</DialogDescription>
        </DialogHeader>

        <div className="overflow-y-auto px-6 flex-1" style={{ maxHeight: "calc(90vh - 180px)" }}>
          <Alert className="mb-4">
            <Info className="h-4 w-4" />
            <AlertDescription>Date format: Julian day + 2-digit year (e.g., 22125 = day 221 of 2025)</AlertDescription>
          </Alert>

          <form id="edit-item-form" onSubmit={handleSubmit} className="space-y-4 pb-4">
            <div className="grid gap-2">
              <Label htmlFor="edit-sku">SKU *</Label>
              <Input
                id="edit-sku"
                placeholder="What the item is (e.g., 5)"
                value={formData.sku}
                onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="edit-lot">Lot Number *</Label>
              <Input
                id="edit-lot"
                placeholder="Lot number for tracking (e.g., A6)"
                value={formData.lot}
                onChange={(e) => setFormData({ ...formData, lot: e.target.value })}
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="edit-uid">UID *</Label>
              <Input
                id="edit-uid"
                placeholder="Unique identifier (e.g., B3)"
                value={formData.uid}
                onChange={(e) => setFormData({ ...formData, uid: e.target.value })}
                required
                disabled // UID should not be editable as it's the primary key
                className="bg-muted"
              />
              <p className="text-xs text-muted-foreground">UID cannot be changed</p>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="edit-received_by">Received By *</Label>
              <Input
                id="edit-received_by"
                placeholder="Initials (e.g., DC)"
                value={formData.received_by}
                onChange={(e) => setFormData({ ...formData, received_by: e.target.value })}
                maxLength={5}
                style={{ textTransform: "uppercase" }}
                required
              />
            </div>

            <JulianDatePicker
              id="edit-date"
              label="Date (Julian Format)"
              value={formData.date}
              onChange={(value: any) => setFormData({ ...formData, date: value })}
              placeholder="e.g., 22125"
              disabled={isLoading}
            />

            <div className="grid gap-2">
              <Label htmlFor="edit-price">Price (Optional)</Label>
              <Input
                id="edit-price"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
              />
            </div>

            <div className="grid gap-2">
              <Label className="flex items-center gap-2">
                Status
                <Badge variant={formData.status === "1" ? "default" : "secondary"}>
                  {formData.status === "1" ? "Active" : "Exited"}
                </Badge>
              </Label>
              <div className="flex items-center space-x-2">
                <Label htmlFor="edit-status" className="text-sm">
                  Exited
                </Label>
                <Switch id="edit-status" checked={formData.status === "1"} onCheckedChange={handleStatusChange} />
                <Label htmlFor="edit-status" className="text-sm">
                  Active
                </Label>
              </div>
            </div>
          </form>
        </div>

        <DialogFooter className="p-6 pt-4 border-t">
          <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" form="edit-item-form" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Updating...
              </>
            ) : (
              "Update Item"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
