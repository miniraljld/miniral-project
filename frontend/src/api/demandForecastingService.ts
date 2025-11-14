import apiClient from "./apiClient";
import type {
  WaterDemand,
  WaterDistributionPlan,
  InvestmentPlan,
} from "./types";

const DEMAND_FORECASTING_API = "/demand";

export const demandForecastingService = {
  // Получение всех данных о спросе
  getAllDemandData: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterDemand[]> => {
    const response = await apiClient.get<WaterDemand[]>(
      DEMAND_FORECASTING_API,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение данных о спросе по ID
  getDemandDataById: async (id: number): Promise<WaterDemand> => {
    const response = await apiClient.get<WaterDemand>(
      `${DEMAND_FORECASTING_API}/${id}`
    );
    return response.data;
  },

  // Создание новых данных о спросе
  createDemandData: async (
    demandData: Omit<WaterDemand, "id" | "created_at" | "updated_at">
  ): Promise<WaterDemand> => {
    const response = await apiClient.post<WaterDemand>(
      DEMAND_FORECASTING_API,
      demandData
    );
    return response.data;
  },

  // Обновление данных о спросе
  updateDemandData: async (
    id: number,
    demandData: Partial<WaterDemand>
  ): Promise<WaterDemand> => {
    const response = await apiClient.put<WaterDemand>(
      `${DEMAND_FORECASTING_API}/${id}`,
      demandData
    );
    return response.data;
  },

  // Удаление данных о спросе
  deleteDemandData: async (id: number): Promise<void> => {
    await apiClient.delete(`${DEMAND_FORECASTING_API}/${id}`);
  },

  // Получение всех планов распределения воды
  getAllDistributionPlans: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<WaterDistributionPlan[]> => {
    const response = await apiClient.get<WaterDistributionPlan[]>(
      `${DEMAND_FORECASTING_API}/distribution-plans`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение плана распределения по ID
  getDistributionPlanById: async (
    id: number
  ): Promise<WaterDistributionPlan> => {
    const response = await apiClient.get<WaterDistributionPlan>(
      `${DEMAND_FORECASTING_API}/distribution-plans/${id}`
    );
    return response.data;
  },

  // Создание нового плана распределения
  createDistributionPlan: async (
    planData: Omit<WaterDistributionPlan, "id" | "created_at" | "updated_at">
  ): Promise<WaterDistributionPlan> => {
    const response = await apiClient.post<WaterDistributionPlan>(
      `${DEMAND_FORECASTING_API}/distribution-plans`,
      planData
    );
    return response.data;
  },

  // Обновление плана распределения
  updateDistributionPlan: async (
    id: number,
    planData: Partial<WaterDistributionPlan>
  ): Promise<WaterDistributionPlan> => {
    const response = await apiClient.put<WaterDistributionPlan>(
      `${DEMAND_FORECASTING_API}/distribution-plans/${id}`,
      planData
    );
    return response.data;
  },

  // Удаление плана распределения
  deleteDistributionPlan: async (id: number): Promise<void> => {
    await apiClient.delete(
      `${DEMAND_FORECASTING_API}/distribution-plans/${id}`
    );
  },

  // Получение всех инвестиционных планов
  getAllInvestmentPlans: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<InvestmentPlan[]> => {
    const response = await apiClient.get<InvestmentPlan[]>(
      `${DEMAND_FORECASTING_API}/investment-plans`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение инвестиционного плана по ID
  getInvestmentPlanById: async (id: number): Promise<InvestmentPlan> => {
    const response = await apiClient.get<InvestmentPlan>(
      `${DEMAND_FORECASTING_API}/investment-plans/${id}`
    );
    return response.data;
  },

  // Создание нового инвестиционного плана
  createInvestmentPlan: async (
    planData: Omit<InvestmentPlan, "id" | "created_at" | "updated_at">
  ): Promise<InvestmentPlan> => {
    const response = await apiClient.post<InvestmentPlan>(
      `${DEMAND_FORECASTING_API}/investment-plans`,
      planData
    );
    return response.data;
  },

  // Обновление инвестиционного плана
  updateInvestmentPlan: async (
    id: number,
    planData: Partial<InvestmentPlan>
  ): Promise<InvestmentPlan> => {
    const response = await apiClient.put<InvestmentPlan>(
      `${DEMAND_FORECASTING_API}/investment-plans/${id}`,
      planData
    );
    return response.data;
  },

  // Удаление инвестиционного плана
  deleteInvestmentPlan: async (id: number): Promise<void> => {
    await apiClient.delete(`${DEMAND_FORECASTING_API}/investment-plans/${id}`);
  },

  // Получение прогноза спроса на основе исторических данных
  getDemandForecast: async (
    location?: string,
    dateFrom?: string,
    dateTo?: string
  ): Promise<WaterDemand[]> => {
    const params: { [key: string]: string } = {};
    if (location) params.location = location;
    if (dateFrom) params.date_from = dateFrom;
    if (dateTo) params.date_to = dateTo;

    const response = await apiClient.get<WaterDemand[]>(
      `${DEMAND_FORECASTING_API}/forecast`,
      { params }
    );
    return response.data;
  },
};
