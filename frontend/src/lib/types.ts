// Holding (from GET /holdings, POST /holdings, PUT /holdings/:id)
export interface Holding {
  id: string;
  user_id: string;
  symbol: string;
  name: string;
  shares: number;
  avg_cost: number;
  created_at: string;
  updated_at: string;
}

export interface HoldingCreate {
  symbol: string;
  shares: number;
  avg_cost: number;
}

export interface HoldingUpdate {
  shares?: number;
  avg_cost?: number;
}

// Dashboard (from GET /dashboard)
export interface DashboardHolding {
  symbol: string;
  shares: number;
  avg_cost: number;
  current_price: number;
  previous_close: number;
  daily_change_pct: number;
  market_value: number;
  pnl: number;
  pnl_pct: number;
  allocation_pct: number;
}

export interface Dashboard {
  total_value: number;
  total_cost: number;
  total_pnl: number;
  total_pnl_pct: number;
  last_updated: string;
  holdings: DashboardHolding[];
}
