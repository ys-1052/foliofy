"use client";

import { useState, useEffect } from "react";
import type { Holding, HoldingCreate, HoldingUpdate } from "@/lib/types";

interface Props {
  onSubmit: (data: HoldingCreate | HoldingUpdate) => Promise<unknown>;
  initialData?: Holding;
  onClose: () => void;
}

export default function HoldingModal({ onSubmit, initialData, onClose }: Props) {
  const isEdit = !!initialData;
  const [symbol, setSymbol] = useState(initialData?.symbol ?? "");
  const [shares, setShares] = useState(initialData?.shares?.toString() ?? "");
  const [avgCost, setAvgCost] = useState(initialData?.avg_cost?.toString() ?? "");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

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
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to save holding");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" role="dialog">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative w-full max-w-md rounded-lg border border-gray-700 bg-gray-800 p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">
            {isEdit ? `Edit ${initialData.symbol}` : "Add Holding"}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
            aria-label="Close"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isEdit && (
            <div>
              <label className="block text-xs text-gray-400 mb-1">Symbol</label>
              <input
                type="text"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
                placeholder="AAPL"
                className="w-full rounded border border-gray-600 bg-gray-700 text-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none placeholder-gray-500"
                maxLength={5}
                autoFocus
              />
            </div>
          )}
          <div>
            <label className="block text-xs text-gray-400 mb-1">Shares</label>
            <input
              type="number"
              value={shares}
              onChange={(e) => setShares(e.target.value)}
              placeholder="10"
              step="1"
              min="1"
              className="w-full rounded border border-gray-600 bg-gray-700 text-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none placeholder-gray-500"
              autoFocus={isEdit}
            />
          </div>
          <div>
            <label className="block text-xs text-gray-400 mb-1">Avg Cost ($)</label>
            <input
              type="number"
              value={avgCost}
              onChange={(e) => setAvgCost(e.target.value)}
              placeholder="150.00"
              step="0.01"
              min="0.01"
              className="w-full rounded border border-gray-600 bg-gray-700 text-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none placeholder-gray-500"
            />
          </div>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded border border-gray-600 px-4 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {submitting ? "Saving..." : isEdit ? "Update" : "Add"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
