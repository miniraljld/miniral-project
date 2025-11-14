import apiClient from "./apiClient";
import type { WaterAsset, AssetMaintenance } from "./types";

const ASSETS_API = "/assets";

export const assetsService = {
  // Получение всех активов
  getAllAssets: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterAsset[]> => {
    const response = await apiClient.get<WaterAsset[]>(ASSETS_API, {
      params: { skip, limit },
    });
    return response.data;
  },

  // Получение актива по ID
  getAssetById: async (id: number): Promise<WaterAsset> => {
    const response = await apiClient.get<WaterAsset>(`${ASSETS_API}/${id}`);
    return response.data;
  },

  // Создание нового актива
  createAsset: async (
    assetData: Omit<WaterAsset, "id" | "created_at" | "updated_at">
  ): Promise<WaterAsset> => {
    const response = await apiClient.post<WaterAsset>(ASSETS_API, assetData);
    return response.data;
  },

  // Обновление актива
  updateAsset: async (
    id: number,
    assetData: Partial<WaterAsset>
  ): Promise<WaterAsset> => {
    const response = await apiClient.put<WaterAsset>(
      `${ASSETS_API}/${id}`,
      assetData
    );
    return response.data;
  },

  // Удаление актива
  deleteAsset: async (id: number): Promise<void> => {
    await apiClient.delete(`${ASSETS_API}/${id}`);
  },

  // Получение истории обслуживания актива
  getAssetMaintenanceHistory: async (
    assetId: number,
    skip: number = 0,
    limit: number = 100
  ): Promise<AssetMaintenance[]> => {
    const response = await apiClient.get<AssetMaintenance[]>(
      `${ASSETS_API}/${assetId}/maintenance`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Создание записи об обслуживании актива
  createAssetMaintenance: async (
    maintenanceData: Omit<AssetMaintenance, "id" | "created_at" | "updated_at">
  ): Promise<AssetMaintenance> => {
    const response = await apiClient.post<AssetMaintenance>(
      `${ASSETS_API}/maintenance`,
      maintenanceData
    );
    return response.data;
  },

  // Обновление записи об обслуживании актива
  updateAssetMaintenance: async (
    id: number,
    maintenanceData: Partial<AssetMaintenance>
  ): Promise<AssetMaintenance> => {
    const response = await apiClient.put<AssetMaintenance>(
      `${ASSETS_API}/maintenance/${id}`,
      maintenanceData
    );
    return response.data;
  },

  // Получение всех записей об обслуживании
  getAllMaintenanceRecords: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<AssetMaintenance[]> => {
    const response = await apiClient.get<AssetMaintenance[]>(
      `${ASSETS_API}/maintenance`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение актива с ближайшим сроком обслуживания
  getAssetNeedingMaintenance: async (): Promise<WaterAsset[]> => {
    const response = await apiClient.get<WaterAsset[]>(
      `${ASSETS_API}/maintenance-due`
    );
    return response.data;
  },
};
