"use client";

import { useState } from "react";
import { useHoldings } from "@/hooks/useHoldings";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import HoldingForm from "@/components/holdings/HoldingForm";
import HoldingsTable from "@/components/holdings/HoldingsTable";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import ErrorMessage from "@/components/ui/ErrorMessage";
import type { Holding, HoldingCreate, HoldingUpdate } from "@/lib/types";

export default function HoldingsPage() {
  return (
    <ProtectedRoute>
      <HoldingsContent />
    </ProtectedRoute>
  );
}

function HoldingsContent() {
  const { holdings, loading, error, addHolding, editHolding, removeHolding, refetch } =
    useHoldings();
  const [editingHolding, setEditingHolding] = useState<Holding | null>(null);

  if (loading) return <LoadingSpinner className="py-20" />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Holdings</h1>

      {editingHolding ? (
        <HoldingForm
          initialData={editingHolding}
          onSubmit={(data) => editHolding(editingHolding.id, data as HoldingUpdate)}
          onCancel={() => setEditingHolding(null)}
        />
      ) : (
        <HoldingForm onSubmit={(data) => addHolding(data as HoldingCreate)} />
      )}

      <HoldingsTable holdings={holdings} onEdit={setEditingHolding} onDelete={removeHolding} />
    </div>
  );
}
