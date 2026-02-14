"use client";

import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import type { DashboardHolding } from "@/lib/types";
import { formatUSD } from "@/lib/format";

interface Props {
  holdings: DashboardHolding[];
}

const COLORS = [
  "#3b82f6",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#ec4899",
  "#06b6d4",
  "#84cc16",
  "#f97316",
  "#6366f1",
];

interface TooltipPayloadItem {
  name: string;
  value: number;
  payload: {
    symbol: string;
    marketValue: number;
    pct: number;
  };
}

function CustomTooltip({ active, payload }: { active?: boolean; payload?: TooltipPayloadItem[] }) {
  if (!active || !payload?.length) return null;
  const item = payload[0].payload;
  return (
    <div className="rounded border border-gray-200 bg-white px-3 py-2 text-sm shadow">
      <p className="font-medium">{item.symbol}</p>
      <p className="text-gray-600">{formatUSD(item.marketValue)}</p>
      <p className="text-gray-500">{item.pct.toFixed(1)}%</p>
    </div>
  );
}

export default function AllocationChart({ holdings }: Props) {
  const data = holdings.map((h) => ({
    symbol: h.symbol,
    value: h.allocation_pct,
    marketValue: h.market_value,
    pct: h.allocation_pct,
  }));

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-medium text-gray-700">Allocation</h2>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="symbol"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, value }: { name?: string; value?: number }) =>
              `${name} ${value?.toFixed(1)}%`
            }
            labelLine={false}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
