"use client"

import { useState } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal, Search, RefreshCw, Trash2, ExternalLink, ArrowRight, Edit } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { apiService } from "@/lib/api-service"
import { EditItemDialog } from "@/components/ui/edit-item-dialog"
import type { InventoryItem } from "@/types/inventory"

interface InventoryTableProps {
  items: InventoryItem[]
  isLoading: boolean
  onRefresh: () => void
  getFormattedDate: (item: InventoryItem) => string
}

export function InventoryTable({ items, isLoading, onRefresh, getFormattedDate }: InventoryTableProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null)
  const { toast } = useToast()

  const filteredItems = items.filter(
    (item) =>
      item.uid?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.sku?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.lot?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.received_by?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.date && new Date(item.date).toLocaleDateString().includes(searchTerm)) ||
      (item.status === "1" && "Active".toLowerCase().includes(searchTerm.toLowerCase())) ||
      (item.status === "0" && "Exited".toLowerCase().includes(searchTerm.toLowerCase())),
  )

  const handleExitItem = async (uid: string) => {
    try {
      await apiService.exitItem(uid)
      toast({
        title: "Item Exited",
        description: `Item ${uid} has been marked as exited`,
      })
      onRefresh()
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to exit item",
        variant: "destructive",
      })
    }
  }

  const handleEntranceItem = async (uid: string) => {
    try {
      // Find the item to update its status back to active
      const item = items.find((i) => i.uid === uid)
      if (!item) {
        throw new Error("Item not found")
      }

      const updatedItem: InventoryItem = { ...item, status: "1" }
      await apiService.updateItem(uid, updatedItem)
      toast({
        title: "Item Re-entered",
        description: `Item ${uid} has been marked as active`,
      })
      onRefresh()
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to re-enter item",
        variant: "destructive",
      })
    }
  }

  const handleDeleteItem = async (uid: string) => {
    try {
      await apiService.deleteItem(uid)
      toast({
        title: "Item Deleted",
        description: `Item ${uid} has been deleted`,
      })
      onRefresh()
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete item",
        variant: "destructive",
      })
    }
  }

  const handleEditItem = (item: InventoryItem) => {
    setEditingItem(item)
  }

  const handleItemUpdated = () => {
    setEditingItem(null)
    onRefresh()
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="h-10 w-64 bg-muted animate-pulse rounded-md" />
          <div className="h-10 w-24 bg-muted animate-pulse rounded-md" />
        </div>
        <div className="space-y-2">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 bg-muted animate-pulse rounded-md" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="relative w-64">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search items..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-8"
          />
        </div>
        <Button onClick={onRefresh} variant="outline" size="sm">
          <RefreshCw className="mr-2 h-4 w-4" />
          Refresh
        </Button>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>UID</TableHead>
              <TableHead>SKU</TableHead>
              <TableHead>LOT</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Received</TableHead>
              <TableHead className="w-[70px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredItems.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                  No items found
                </TableCell>
              </TableRow>
            ) : (
              filteredItems.map((item) => (
                <TableRow key={item.uid}>
                  <TableCell className="font-mono text-sm">{item.uid}</TableCell>
                  <TableCell>{item.sku || "Missing SKU"}</TableCell>
                  <TableCell>{item.lot || "Missing LOT"}</TableCell>
                  <TableCell>
                    <Badge variant={item.status === "1" ? "default" : "secondary"}>
                      {item.status === "1" ? "Active" : "Exited"}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">{getFormattedDate(item)}</TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => handleEditItem(item)}>
                          <Edit className="mr-2 h-4 w-4" />
                          Edit Item
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        {item.status === "1" ? (
                          <DropdownMenuItem onClick={() => item.uid && handleExitItem(item.uid)}>
                            <ExternalLink className="mr-2 h-4 w-4" />
                            Exit Item
                          </DropdownMenuItem>
                        ) : (
                          <DropdownMenuItem onClick={() => item.uid && handleEntranceItem(item.uid)}>
                            <ArrowRight className="mr-2 h-4 w-4" />
                            Re-enter Item
                          </DropdownMenuItem>
                        )}
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                          onClick={() => item.uid && handleEntranceItem(item.uid)}
                          disabled={!item.uid}
                          className="text-destructive focus:text-destructive"
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Edit Item Dialog */}
      {editingItem && (
        <EditItemDialog
          item={editingItem}
          open={!!editingItem}
          onOpenChange={(open) => !open && setEditingItem(null)}
          onItemUpdated={handleItemUpdated}
        />
      )}
    </div>
  )
}
