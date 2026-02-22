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
    <div className="text-center py-6">
      <p className="text-lg text-gray-300">Total Assets</p>
      <p className="mt-2 text-3xl font-bold text-white">{formatUSD(totalValue)}</p>
      <p className={`mt-1 text-sm ${isProfit ? "text-green-400" : "text-red-400"}`}>
        {formatUSD(totalPnl)} ({formatPercent(totalPnlPct)})
      </p>
      <p className="mt-2 text-xs text-gray-500">Last updated: {formatDateTime(lastUpdated)}</p>
    </div>
  );
}
