import apiClient from "./apiClient";
import type { Complaint, ComplaintCategory } from "./types";

const COMPLAINTS_API = "/complaints";

export const complaintsService = {
  // Получение всех жалоб
  getAllComplaints: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<Complaint[]> => {
    const response = await apiClient.get<Complaint[]>(COMPLAINTS_API, {
      params: { skip, limit },
    });
    return response.data;
  },

  // Получение жалобы по ID
  getComplaintById: async (id: number): Promise<Complaint> => {
    const response = await apiClient.get<Complaint>(`${COMPLAINTS_API}/${id}`);
    return response.data;
  },

  // Создание новой жалобы
  createComplaint: async (
    complaintData: Omit<Complaint, "id" | "created_at" | "updated_at">
  ): Promise<Complaint> => {
    const response = await apiClient.post<Complaint>(
      COMPLAINTS_API,
      complaintData
    );
    return response.data;
  },

  // Обновление жалобы
  updateComplaint: async (
    id: number,
    complaintData: Partial<Complaint>
  ): Promise<Complaint> => {
    const response = await apiClient.put<Complaint>(
      `${COMPLAINTS_API}/${id}`,
      complaintData
    );
    return response.data;
  },

  // Удаление жалобы
  deleteComplaint: async (id: number): Promise<void> => {
    await apiClient.delete(`${COMPLAINTS_API}/${id}`);
  },

  // Назначение жалобы на исполнение
  assignComplaint: async (
    id: number,
    assignedTo: number
  ): Promise<Complaint> => {
    const response = await apiClient.patch<Complaint>(
      `${COMPLAINTS_API}/${id}/assign`,
      { assigned_to: assignedTo }
    );
    return response.data;
  },

  // Отметка жалобы как решенной
  resolveComplaint: async (id: number): Promise<Complaint> => {
    const response = await apiClient.patch<Complaint>(
      `${COMPLAINTS_API}/${id}/resolve`
    );
    return response.data;
  },

  // Получение всех категорий жалоб
  getAllComplaintCategories: async (): Promise<ComplaintCategory[]> => {
    const response = await apiClient.get<ComplaintCategory[]>(
      `${COMPLAINTS_API}/categories`
    );
    return response.data;
  },

  // Создание новой категории жалоб
  createComplaintCategory: async (
    categoryData: Omit<ComplaintCategory, "id" | "created_at" | "updated_at">
  ): Promise<ComplaintCategory> => {
    const response = await apiClient.post<ComplaintCategory>(
      `${COMPLAINTS_API}/categories`,
      categoryData
    );
    return response.data;
  },

  // Обновление категории жалоб
  updateComplaintCategory: async (
    id: number,
    categoryData: Partial<ComplaintCategory>
  ): Promise<ComplaintCategory> => {
    const response = await apiClient.put<ComplaintCategory>(
      `${COMPLAINTS_API}/categories/${id}`,
      categoryData
    );
    return response.data;
  },

  // Удаление категории жалоб
  deleteComplaintCategory: async (id: number): Promise<void> => {
    await apiClient.delete(`${COMPLAINTS_API}/categories/${id}`);
  },
};
