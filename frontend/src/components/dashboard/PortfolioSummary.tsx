"use client";

import { formatUSD, formatPercent, formatDateTime } from "@/lib/format";

interface Props {
  totalValue: number;
  totalCost: number;
  totalPnl: number;
  totalPnlPct: number;
  lastUpdated: string;
}

export default function PortfolioSummary({
  totalValue,
  totalCost,
  totalPnl,
  totalPnlPct,
  lastUpdated,
}: Props) {
  const isProfit = totalPnl >= 0;

  return (
    <div>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <p className="text-xs text-gray-500">Total Value</p>
          <p className="mt-1 text-xl font-semibold">{formatUSD(totalValue)}</p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <p className="text-xs text-gray-500">Total Cost</p>
          <p className="mt-1 text-xl font-semibold">{formatUSD(totalCost)}</p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <p className="text-xs text-gray-500">Total P&L</p>
          <p
            className={`mt-1 text-xl font-semibold ${isProfit ? "text-green-600" : "text-red-600"}`}
          >
            {formatUSD(totalPnl)}
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <p className="text-xs text-gray-500">Return</p>
          <p
            className={`mt-1 text-xl font-semibold ${isProfit ? "text-green-600" : "text-red-600"}`}
          >
            {formatPercent(totalPnlPct)}
          </p>
        </div>
      </div>
      <p className="mt-2 text-xs text-gray-400">Last updated: {formatDateTime(lastUpdated)}</p>
    </div>
  );
}
