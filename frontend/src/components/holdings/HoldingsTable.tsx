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
      <div className="py-8 text-center text-sm text-gray-400">
        No holdings yet. Add your first holding to get started.
      </div>
    );
  }

  const handleDelete = (id: string, symbol: string) => {
    if (window.confirm(`Delete ${symbol}?`)) {
      onDelete(id);
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-700 text-left text-xs font-medium uppercase text-gray-400">
            <th className="px-4 py-3">Symbol</th>
            <th className="px-4 py-3 text-right">Shares</th>
            <th className="px-4 py-3 text-right">Avg.</th>
            <th className="px-4 py-3 text-right"></th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((holding) => (
            <tr key={holding.id} className="border-b border-gray-700/50">
              <td className="px-4 py-3 font-medium text-white">{holding.symbol}</td>
              <td className="px-4 py-3 text-right text-gray-300">{formatShares(holding.shares)}</td>
              <td className="px-4 py-3 text-right text-gray-300">{formatUSD(holding.avg_cost)}</td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => onEdit(holding)}
                  className="mr-3 text-gray-400 hover:text-white transition-colors"
                  title="Edit"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                  </svg>
                </button>
                <button
                  onClick={() => handleDelete(holding.id, holding.symbol)}
                  className="text-gray-400 hover:text-red-400 transition-colors"
                  title="Delete"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                  </svg>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
