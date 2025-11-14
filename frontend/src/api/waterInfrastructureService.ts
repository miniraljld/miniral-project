import apiClient from "./apiClient";
import type { WaterInfrastructure, WaterLeak } from "./types";

const WATER_INFRASTRUCTURE_API = "/water-infrastructure";

export const waterInfrastructureService = {
  // Получение всех объектов инфраструктуры
  getAllInfrastructure: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterInfrastructure[]> => {
    const response = await apiClient.get<WaterInfrastructure[]>(
      WATER_INFRASTRUCTURE_API,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение объекта инфраструктуры по ID
  getInfrastructureById: async (id: number): Promise<WaterInfrastructure> => {
    const response = await apiClient.get<WaterInfrastructure>(
      `${WATER_INFRASTRUCTURE_API}/${id}`
    );
    return response.data;
  },

  // Создание нового объекта инфраструктуры
  createInfrastructure: async (
    infrastructureData: Omit<
      WaterInfrastructure,
      "id" | "created_at" | "updated_at"
    >
  ): Promise<WaterInfrastructure> => {
    const response = await apiClient.post<WaterInfrastructure>(
      WATER_INFRASTRUCTURE_API,
      infrastructureData
    );
    return response.data;
  },

  // Обновление объекта инфраструктуры
  updateInfrastructure: async (
    id: number,
    infrastructureData: Partial<WaterInfrastructure>
  ): Promise<WaterInfrastructure> => {
    const response = await apiClient.put<WaterInfrastructure>(
      `${WATER_INFRASTRUCTURE_API}/${id}`,
      infrastructureData
    );
    return response.data;
  },

  // Удаление объекта инфраструктуры
  deleteInfrastructure: async (id: number): Promise<void> => {
    await apiClient.delete(`${WATER_INFRASTRUCTURE_API}/${id}`);
  },

  // Получение утечек для конкретного объекта инфраструктуры
  getLeaksByInfrastructure: async (
    infrastructureId: number
  ): Promise<WaterLeak[]> => {
    const response = await apiClient.get<WaterLeak[]>(
      `${WATER_INFRASTRUCTURE_API}/${infrastructureId}/leaks`
    );
    return response.data;
  },

  // Создание новой утечки
  createLeak: async (
    leakData: Omit<WaterLeak, "id" | "created_at" | "updated_at">
  ): Promise<WaterLeak> => {
    const response = await apiClient.post<WaterLeak>(
      `${WATER_INFRASTRUCTURE_API}/leaks`,
      leakData
    );
    return response.data;
  },

  // Обновление информации об утечке
  updateLeak: async (
    id: number,
    leakData: Partial<WaterLeak>
  ): Promise<WaterLeak> => {
    const response = await apiClient.put<WaterLeak>(
      `${WATER_INFRASTRUCTURE_API}/leaks/${id}`,
      leakData
    );
    return response.data;
  },

  // Получение всех утечек
  getAllLeaks: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterLeak[]> => {
    const response = await apiClient.get<WaterLeak[]>(
      `${WATER_INFRASTRUCTURE_API}/leaks`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },
};
