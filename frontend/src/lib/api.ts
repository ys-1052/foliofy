import type { Holding, HoldingCreate, HoldingUpdate, Dashboard, DashboardHolding } from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const accessToken = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    headers,
    ...options,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// Convert string decimal fields to numbers (Pydantic serializes Decimal as string)
function parseHolding(h: Record<string, unknown>): Holding {
  return {
    ...h,
    shares: Number(h.shares),
    avg_cost: Number(h.avg_cost),
  } as Holding;
}

function parseDashboard(d: Record<string, unknown>): Dashboard {
  const raw = d as Record<string, unknown> & { holdings: Record<string, unknown>[] };
  return {
    total_value: Number(raw.total_value),
    total_cost: Number(raw.total_cost),
    total_pnl: Number(raw.total_pnl),
    total_pnl_pct: Number(raw.total_pnl_pct),
    last_updated: raw.last_updated as string,
    holdings: raw.holdings.map(
      (h): DashboardHolding => ({
        symbol: h.symbol as string,
        shares: Number(h.shares),
        avg_cost: Number(h.avg_cost),
        current_price: Number(h.current_price),
        previous_close: Number(h.previous_close),
        daily_change_pct: Number(h.daily_change_pct),
        market_value: Number(h.market_value),
        pnl: Number(h.pnl),
        pnl_pct: Number(h.pnl_pct),
        allocation_pct: Number(h.allocation_pct),
      })
    ),
  };
}

// Holdings
export const listHoldings = async (): Promise<Holding[]> => {
  const data = await request<Record<string, unknown>[]>("/holdings");
  return data.map(parseHolding);
};

export const createHolding = async (data: HoldingCreate): Promise<Holding> => {
  const raw = await request<Record<string, unknown>>("/holdings", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return parseHolding(raw);
};

export const updateHolding = async (id: string, data: HoldingUpdate): Promise<Holding> => {
  const raw = await request<Record<string, unknown>>(`/holdings/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
  return parseHolding(raw);
};

export const deleteHolding = (id: string) => request<void>(`/holdings/${id}`, { method: "DELETE" });

// Dashboard
export const getDashboard = async (): Promise<Dashboard> => {
  const raw = await request<Record<string, unknown>>("/dashboard");
  return parseDashboard(raw);
};
