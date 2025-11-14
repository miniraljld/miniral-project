import apiClient from "./apiClient";
import type { WaterQuality, WaterQualityAlert } from "./types";

const WATER_QUALITY_API = "/water-quality";

export const waterQualityService = {
  // Получение всех данных о качестве воды
  getAllQualityData: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterQuality[]> => {
    const response = await apiClient.get<WaterQuality[]>(WATER_QUALITY_API, {
      params: { skip, limit },
    });
    return response.data;
  },

  // Получение данных о качестве воды по ID
  getQualityDataById: async (id: number): Promise<WaterQuality> => {
    const response = await apiClient.get<WaterQuality>(
      `${WATER_QUALITY_API}/${id}`
    );
    return response.data;
  },

  // Создание новых данных о качестве воды
  createQualityData: async (
    qualityData: Omit<WaterQuality, "id" | "created_at" | "updated_at">
  ): Promise<WaterQuality> => {
    const response = await apiClient.post<WaterQuality>(
      WATER_QUALITY_API,
      qualityData
    );
    return response.data;
  },

  // Обновление данных о качестве воды
  updateQualityData: async (
    id: number,
    qualityData: Partial<WaterQuality>
  ): Promise<WaterQuality> => {
    const response = await apiClient.put<WaterQuality>(
      `${WATER_QUALITY_API}/${id}`,
      qualityData
    );
    return response.data;
  },

  // Удаление данных о качестве воды
  deleteQualityData: async (id: number): Promise<void> => {
    await apiClient.delete(`${WATER_QUALITY_API}/${id}`);
  },

  // Получение всех уведомлений о качестве воды
  getAllQualityAlerts: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterQualityAlert[]> => {
    const response = await apiClient.get<WaterQualityAlert[]>(
      `${WATER_QUALITY_API}/alerts`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение уведомления о качестве воды по ID
  getQualityAlertById: async (id: number): Promise<WaterQualityAlert> => {
    const response = await apiClient.get<WaterQualityAlert>(
      `${WATER_QUALITY_API}/alerts/${id}`
    );
    return response.data;
  },

  // Создание нового уведомления о качестве воды
  createQualityAlert: async (
    alertData: Omit<WaterQualityAlert, "id" | "created_at" | "updated_at">
  ): Promise<WaterQualityAlert> => {
    const response = await apiClient.post<WaterQualityAlert>(
      `${WATER_QUALITY_API}/alerts`,
      alertData
    );
    return response.data;
  },

  // Обновление уведомления о качестве воды
  updateQualityAlert: async (
    id: number,
    alertData: Partial<WaterQualityAlert>
  ): Promise<WaterQualityAlert> => {
    const response = await apiClient.put<WaterQualityAlert>(
      `${WATER_QUALITY_API}/alerts/${id}`,
      alertData
    );
    return response.data;
  },

  // Подтверждение уведомления о качестве воды
  acknowledgeQualityAlert: async (id: number): Promise<WaterQualityAlert> => {
    const response = await apiClient.patch<WaterQualityAlert>(
      `${WATER_QUALITY_API}/alerts/${id}/acknowledge`
    );
    return response.data;
  },
};
