// Типы для пользователя
export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  role: "user" | "engineer" | "admin";
  created_at: string;
  updated_at?: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserLoginResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  username: string;
}

export interface UserCreate {
  username: string;
  email: string;
  full_name?: string;
  password: string;
  is_active?: boolean;
  role?: 'user' | 'engineer' | 'admin';
}

export interface UserUpdate {
  username?: string;
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_admin?: boolean;
}

// Типы для инфраструктуры водоснабжения
export interface WaterInfrastructure {
  id: number;
  name: string;
  type: string;
  location: string;
  latitude?: number;
  longitude?: number;
  pressure?: number;
  temperature?: number;
  leak_detected: boolean;
  last_inspection?: string;
  condition_status: string;
  installation_date?: string;
  created_at: string;
  updated_at?: string;
}

export interface WaterLeak {
  id: number;
  infrastructure_id: number;
  leak_detected_at: string;
  severity: string;
  description?: string;
  repaired: boolean;
  repair_date?: string;
  created_at: string;
  updated_at?: string;
}

// Типы для качества воды
export interface WaterQuality {
  id: number;
  location: string;
  latitude?: number;
  longitude?: number;
  ph_level?: number;
  chlorine_level?: number;
  turbidity?: number;
  temperature?: number;
  dissolved_oxygen?: number;
  e_coli?: number;
  total_solids?: number;
  chemical_oxygen_demand?: number;
  biological_oxygen_demand?: number;
  date_measured: string;
  measured_by?: string;
  notes?: string;
  quality_status: string;
  created_at: string;
  updated_at?: string;
}

export interface WaterQualityAlert {
  id: number;
  quality_id: number;
  alert_type: string;
  message: string;
  is_active: boolean;
  acknowledged: boolean;
  acknowledged_by?: number;
  acknowledged_at?: string;
  created_at: string;
  updated_at?: string;
}

// Типы для санитарии
export interface SanitationFacility {
  id: number;
  name: string;
  type: string;
  location: string;
  latitude?: number;
  longitude?: number;
  capacity?: number;
  is_accessible: boolean;
  is_operational: boolean;
  last_maintenance?: string;
  condition_status: string;
  installation_date?: string;
  created_at: string;
  updated_at?: string;
}

export interface SanitationReport {
  id: number;
  facility_id: number;
  reported_by: number;
  report_date: string;
  hygiene_rating?: number;
  cleanliness_rating?: number;
  accessibility_rating?: number;
  description?: string;
  photo_url?: string;
  is_resolved: boolean;
  resolved_by?: number;
  resolved_at?: string;
  created_at: string;
  updated_at?: string;
}

// Типы для жалоб
export interface Complaint {
  id: number;
  user_id?: number;
  full_name: string;
  email?: string;
  phone?: string;
  category: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  description: string;
  photo_url?: string;
  priority: string;
  status: string;
  assigned_to?: number;
  resolved_at?: string;
  created_at: string;
  updated_at?: string;
}

export interface ComplaintCategory {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

// Типы для тарифов
export interface Tariff {
  id: number;
  name: string;
  description?: string;
  price_per_unit: number;
  unit_type: string;
  is_active: boolean;
  start_date: string;
  end_date?: string;
  created_at: string;
  updated_at?: string;
}

export interface PaymentMethod {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  is_online: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UserPayment {
  id: number;
  user_id: number;
  amount: number;
  tariff_id: number;
  payment_method_id: number;
  payment_date: string;
  payment_reference?: string;
  status: string;
  created_at: string;
  updated_at?: string;
}

// Типы для активов
export interface WaterAsset {
  id: number;
  name: string;
  asset_type: string;
  description?: string;
  location: string;
  latitude?: number;
  longitude?: number;
  installation_date?: string;
  last_maintenance?: string;
  next_maintenance?: string;
  status: string;
  is_operational: boolean;
  asset_value?: number;
  depreciation_rate: number;
  created_at: string;
  updated_at?: string;
}

export interface AssetMaintenance {
  id: number;
  asset_id: number;
  maintenance_type: string;
  description?: string;
  performed_by?: string;
  cost?: number;
  maintenance_date: string;
  next_maintenance_date?: string;
  created_at: string;
  updated_at?: string;
}

// Типы для прогнозирования спроса
export interface WaterDemand {
  id: number;
  location: string;
  latitude?: number;
  longitude?: number;
  demand_amount: number;
  demand_date: string;
  demand_type: string;
  forecasted: boolean;
  created_at: string;
  updated_at?: string;
}

export interface WaterDistributionPlan {
  id: number;
  plan_name: string;
  description?: string;
  start_date: string;
  end_date: string;
  total_water_allocated: number;
  allocated_to_residential: number;
  allocated_to_commercial: number;
  allocated_to_industrial: number;
  allocated_to_public: number;
  status: string;
  created_by: number;
  created_at: string;
  updated_at?: string;
}

export interface InvestmentPlan {
  id: number;
  plan_name: string;
  description?: string;
  total_investment: number;
  allocated_for_infrastructure: number;
  allocated_for_equipment: number;
  allocated_for_maintenance: number;
  allocated_for_human_resources: number;
  start_date: string;
  end_date: string;
  status: string;
  created_by: number;
  created_at: string;
  updated_at?: string;
}

// Типы для уведомлений
export interface Notification {
  id: number;
  user_id?: number;
  title: string;
  message: string;
  notification_type: string;
  priority: string;
  is_read: boolean;
  target_audience: string;
  created_at: string;
  updated_at?: string;
}

export interface NotificationSetting {
  id: number;
  user_id: number;
  notification_type: string;
  enabled: boolean;
  channel_email: boolean;
  channel_sms: boolean;
  channel_push: boolean;
  created_at: string;
  updated_at?: string;
}
