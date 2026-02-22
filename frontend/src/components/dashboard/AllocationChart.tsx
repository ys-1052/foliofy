"use client";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
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
    <div className="rounded bg-gray-800 px-3 py-2 text-sm shadow border border-gray-600">
      <p className="font-medium text-white">{item.symbol}</p>
      <p className="text-gray-300">{formatUSD(item.marketValue)}</p>
      <p className="text-gray-400">{item.pct.toFixed(1)}%</p>
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
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="symbol"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            labelLine={false}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
      <div className="mt-4 space-y-2">
        {data.map((item, index) => (
          <div key={item.symbol} className="flex items-center gap-2 text-sm">
            <span
              className="w-3 h-3 rounded-full shrink-0"
              style={{ backgroundColor: COLORS[index % COLORS.length] }}
            />
            <span className="text-gray-300">
              {item.symbol} ({item.pct.toFixed(0)}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
