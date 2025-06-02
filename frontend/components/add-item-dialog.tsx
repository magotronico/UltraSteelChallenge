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
import { Plus, Loader2, Calendar, Info } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { InventoryItem } from "@/types/inventory"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "https://d594-131-178-102-168.ngrok-free.app"; // Fallback to a default if not found

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
    e.preventDefault();
    setIsLoading(true);

    try {
      const item: InventoryItem = {
        sku: formData.sku.trim(),
        lot: formData.lot.trim(),
        uid: formData.uid.trim(),
        received_by: formData.received_by.trim().toUpperCase(),
        date: formData.date || generateJulianDate(),
        status: "1", // Active by default
        price: formData.price ? Number.parseFloat(formData.price) : undefined, // Convert to number if provided
      };

      const response = await fetch(`${API_BASE_URL}/add_manually`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(item),
      });

      // Check if response is ok
      if (!response.ok) {
        // Read the response to see what the server says
        const errorData = await response.json();
        console.error("Server Response Error: ", errorData); // Add this for debugging
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      toast({
        title: "Item Added Successfully",
        description: `Item "${formData.sku}" has been added to inventory`,
      });

      // Reset form
      setFormData({
        sku: "",
        lot: "",
        uid: "",
        received_by: "",
        date: "",
        price: "",
      });
      setOpen(false);
      onItemAdded();
    } catch (error) {
      console.error("Error adding item:", error); // This will log the error to the console for debugging
      toast({
        title: "Error Adding Item",
        description: error instanceof Error ? error.message : "Failed to add item to inventory",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };



  const handleAutoFillDate = () => {
    setFormData({ ...formData, date: generateJulianDate() })
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="sm" className="w-full">
          <Plus className="mr-2 h-4 w-4" />
          Add Item
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Add New Item</DialogTitle>
          <DialogDescription>Add a new item to your inventory manually</DialogDescription>
        </DialogHeader>

        <Alert>
          <Info className="h-4 w-4" />
          <AlertDescription>Date format: Julian day + 2-digit year (e.g., 22125 = day 221 of 2025)</AlertDescription>
        </Alert>

        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
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

            <div className="grid gap-2">
              <Label htmlFor="date" className="flex items-center gap-2">
                Date (Julian Format)
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleAutoFillDate}
                  className="h-6 px-2 text-xs"
                >
                  <Calendar className="mr-1 h-3 w-3" />
                  Today
                </Button>
              </Label>
              <Input
                id="date"
                placeholder="e.g., 22125 (leave empty for today)"
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                pattern="[0-9]{5}"
                maxLength={5}
              />
            </div>

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
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={isLoading}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
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
        </form>
      </DialogContent>
    </Dialog>
  )
}
