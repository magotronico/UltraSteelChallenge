import type { InventoryItem } from "@/types/inventory"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://d594-131-178-102-168.ngrok-free.app"

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`

    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`)
    }

    return response.json()
  }

  async healthCheck() {
    return this.request<{ status: string; timestamp: string }>("/health")
  }

  async getAllItems() {
    return this.request<{ items: InventoryItem[] }>("/get_all_items")
  }

  async getItemByUid(uid: string) {
    return this.request<{ item: InventoryItem | string }>(`/find_item_by_uid/${uid}`)
  }

  async addItem(item: Omit<InventoryItem, "created_at"> & { created_at?: string }) {
    return this.request<{ message: string; data: InventoryItem }>("/add_manually", {
      method: "POST",
      body: JSON.stringify(item),
    })
  }

  async addFromTag(epcAscii: string) {
    return this.request<{ message: string; data: InventoryItem }>(`/add_from_tag/${epcAscii}`, {
      method: "POST",
    })
  }

  async exitItem(uid: string) {
    return this.request<{ message: string }>(`/exit_item/${uid}`, {
      method: "POST",
    })
  }

  async updateItem(uid: string, item: InventoryItem) {
    return this.request<{ message: string; data: InventoryItem }>(`/update_item/${uid}`, {
      method: "POST",
      body: JSON.stringify(item),
    })
  }

  async deleteItem(uid: string) {
    return this.request<{ message: string }>(`/delete_item/${uid}`, {
      method: "DELETE",
    })
  }

  async startReading() {
    return this.request<{ message: string }>("/start_reading")
  }

  async stopReading() {
    return this.request<{ message: string }>("/stop_reading", {
      method: "POST",
    })
  }

  async writeTag(data: string) {
    return this.request<{ message: string }>("/write_tag", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    })
  }
}

export const apiService = new ApiService()
