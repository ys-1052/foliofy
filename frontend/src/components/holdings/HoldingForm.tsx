"use client";

import { useState } from "react";
import type { Holding, HoldingCreate, HoldingUpdate } from "@/lib/types";

interface Props {
  onSubmit: (data: HoldingCreate | HoldingUpdate) => Promise<unknown>;
  initialData?: Holding;
  onCancel?: () => void;
}

export default function HoldingForm({ onSubmit, initialData, onCancel }: Props) {
  const isEdit = !!initialData;
  const [symbol, setSymbol] = useState(initialData?.symbol ?? "");
  const [shares, setShares] = useState(initialData?.shares?.toString() ?? "");
  const [avgCost, setAvgCost] = useState(initialData?.avg_cost?.toString() ?? "");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const sharesNum = parseFloat(shares);
    const avgCostNum = parseFloat(avgCost);

    if (!isEdit && !symbol.trim()) {
      setError("Symbol is required");
      return;
    }
    if (isNaN(sharesNum) || sharesNum <= 0) {
      setError("Shares must be a positive number");
      return;
    }
    if (isNaN(avgCostNum) || avgCostNum <= 0) {
      setError("Avg cost must be a positive number");
      return;
    }

    setSubmitting(true);
    try {
      if (isEdit) {
        await onSubmit({ shares: sharesNum, avg_cost: avgCostNum } as HoldingUpdate);
      } else {
        await onSubmit({
          symbol: symbol.toUpperCase().trim(),
          shares: sharesNum,
          avg_cost: avgCostNum,
        } as HoldingCreate);
      }
      if (!isEdit) {
        setSymbol("");
        setShares("");
        setAvgCost("");
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to save holding");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-gray-200 bg-white p-4">
      <h3 className="text-sm font-medium text-gray-700 mb-3">
        {isEdit ? `Edit ${initialData.symbol}` : "Add Holding"}
      </h3>
      <div className="flex flex-wrap gap-3 items-end">
        {!isEdit && (
          <div className="flex-1 min-w-[120px]">
            <label className="block text-xs text-gray-500 mb-1">Symbol</label>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="AAPL"
              className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
              maxLength={5}
            />
          </div>
        )}
        <div className="flex-1 min-w-[120px]">
          <label className="block text-xs text-gray-500 mb-1">Shares</label>
          <input
            type="number"
            value={shares}
            onChange={(e) => setShares(e.target.value)}
            placeholder="10"
            step="0.01"
            min="0.01"
            className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          />
        </div>
        <div className="flex-1 min-w-[120px]">
          <label className="block text-xs text-gray-500 mb-1">Avg Cost ($)</label>
          <input
            type="number"
            value={avgCost}
            onChange={(e) => setAvgCost(e.target.value)}
            placeholder="150.00"
            step="0.01"
            min="0.01"
            className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          />
        </div>
        <div className="flex gap-2">
          <button
            type="submit"
            disabled={submitting}
            className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {submitting ? "Saving..." : isEdit ? "Update" : "Add"}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="rounded border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
          )}
        </div>
      </div>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </form>
  );
}
