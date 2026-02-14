"use client";

import type { Holding } from "@/lib/types";
import { formatUSD, formatShares } from "@/lib/format";

interface Props {
  holdings: Holding[];
  onEdit: (holding: Holding) => void;
  onDelete: (id: string) => void;
}

export default function HoldingsTable({ holdings, onEdit, onDelete }: Props) {
  if (holdings.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-8 text-center text-sm text-gray-500">
        No holdings yet. Add your first holding above.
      </div>
    );
  }

  const handleDelete = (id: string, symbol: string) => {
    if (window.confirm(`Delete ${symbol}?`)) {
      onDelete(id);
    }
  };

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50 text-left text-xs font-medium uppercase text-gray-500">
            <th className="px-4 py-3">Symbol</th>
            <th className="px-4 py-3">Name</th>
            <th className="px-4 py-3 text-right">Shares</th>
            <th className="px-4 py-3 text-right">Avg Cost</th>
            <th className="px-4 py-3 text-right">Total Cost</th>
            <th className="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((holding) => (
            <tr key={holding.id} className="border-b border-gray-100 last:border-0">
              <td className="px-4 py-3 font-medium">{holding.symbol}</td>
              <td className="px-4 py-3 text-gray-600">{holding.name}</td>
              <td className="px-4 py-3 text-right">{formatShares(holding.shares)}</td>
              <td className="px-4 py-3 text-right">{formatUSD(holding.avg_cost)}</td>
              <td className="px-4 py-3 text-right">
                {formatUSD(holding.shares * holding.avg_cost)}
              </td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => onEdit(holding)}
                  className="mr-2 text-blue-600 hover:text-blue-800"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(holding.id, holding.symbol)}
                  className="text-red-600 hover:text-red-800"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
