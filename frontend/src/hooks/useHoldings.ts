"use client";

import { useState, useEffect, useCallback } from "react";
import * as api from "@/lib/api";
import type { Holding, HoldingCreate, HoldingUpdate } from "@/lib/types";

export function useHoldings() {
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHoldings = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listHoldings();
      setHoldings(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load holdings");
    } finally {
      setLoading(false);
    }
  }, []);

  const addHolding = useCallback(async (data: HoldingCreate) => {
    const holding = await api.createHolding(data);
    setHoldings((prev) => {
      const filtered = prev.filter((h) => h.symbol !== holding.symbol);
      return [...filtered, holding];
    });
    return holding;
  }, []);

  const editHolding = useCallback(async (id: string, data: HoldingUpdate) => {
    const updated = await api.updateHolding(id, data);
    setHoldings((prev) => prev.map((h) => (h.id === id ? updated : h)));
    return updated;
  }, []);

  const removeHolding = useCallback(async (id: string) => {
    await api.deleteHolding(id);
    setHoldings((prev) => prev.filter((h) => h.id !== id));
  }, []);

  useEffect(() => {
    fetchHoldings();
  }, [fetchHoldings]);

  return {
    holdings,
    loading,
    error,
    addHolding,
    editHolding,
    removeHolding,
    refetch: fetchHoldings,
  };
}
