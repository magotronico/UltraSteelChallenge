"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/hooks/use-toast"
import { InventoryTable } from "@/components/inventory-table"
import { RFIDControls } from "@/components/rfid-controls"
import { AddItemDialog } from "@/components/add-item-dialog"
import { Activity, Package, Scan, TrendingUp } from "lucide-react"
import { apiService } from "@/lib/api-service"
import type { InventoryItem } from "@/types/inventory"

export default function DashboardPage() {
  const [items, setItems] = useState<InventoryItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [rfidStatus, setRfidStatus] = useState<"idle" | "reading" | "writing">("idle")
  const { toast } = useToast()

  const fetchItems = async () => {
    try {
      const data = await apiService.getAllItems()
      setItems(data.items)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch inventory items",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchItems()
  }, [])

  const convertJulianToDate = (julianDate: string): string => {
    // Expecting format: %j%y (3 digits for Julian day, 2 digits for year)
    if (!/^\d{5}$/.test(julianDate)) return "Invalid date";
    const dayOfYear = parseInt(julianDate.slice(0, 3), 10); // First 3 digits
    const year = 2000 + parseInt(julianDate.slice(3, 5), 10); // Last 2 digits, assume 2000+
    const date = new Date(year, 0); // Jan 1st of year
    date.setDate(dayOfYear); // Set day of year

    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    return `${day}/${month}/${date.getFullYear()}`;
  }

  // Convert and format the date for each item
  const getFormattedDate = (item: InventoryItem): string => {
    if (item.date) {
      return convertJulianToDate(item.date); // Convert the Julian date format
    }
    return "N/A"; // Return "N/A" if the date is not provided
  }

  const activeItems = items.filter((item) => item.status === "1")
  const totalValue = activeItems.reduce((sum, item) => sum + (item.price || 0), 0)

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Items</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{items.length}</div>
            <p className="text-xs text-muted-foreground">{activeItems.length} active items</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Value</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalValue.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Active inventory value</p>
          </CardContent>
        </Card>

        {/* RFID Status Card */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">RFID Status</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              {/* Display the current RFID status */}
              <Badge variant={rfidStatus === "reading" ? "default" : "secondary"}>{rfidStatus}</Badge>
            </div>
            <p className="text-xs text-muted-foreground">Current RFID state</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Quick Actions</CardTitle>
            <Scan className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <AddItemDialog onItemAdded={fetchItems} />
          </CardContent>
        </Card>
      </div>

      {/* RFID Controls */}
      <RFIDControls
        onStatusChange={setRfidStatus} // Update RFID status
      />

      {/* Inventory Table */}
      <Card>
        <CardHeader>
          <CardTitle>Inventory Items</CardTitle>
          <CardDescription>Manage your RFID-tracked inventory items</CardDescription>
        </CardHeader>
        <CardContent>
          <InventoryTable 
            items={items} 
            isLoading={isLoading} 
            onRefresh={fetchItems} 
            getFormattedDate={getFormattedDate}
          />
        </CardContent>
      </Card>
    </div>
  )
}
