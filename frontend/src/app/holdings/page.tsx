"use client";

import { useState } from "react";
import { useHoldings } from "@/hooks/useHoldings";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import HoldingModal from "@/components/holdings/HoldingModal";
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
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingHolding, setEditingHolding] = useState<Holding | null>(null);

  const handleOpenAdd = () => {
    setEditingHolding(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (holding: Holding) => {
    setEditingHolding(holding);
    setIsModalOpen(true);
  };

  const handleClose = () => {
    setIsModalOpen(false);
    setEditingHolding(null);
  };

  if (loading) return <LoadingSpinner className="py-20" />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Holdings</h1>
        <button
          onClick={handleOpenAdd}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          + Add Holding
        </button>
      </div>

      <HoldingsTable holdings={holdings} onEdit={handleOpenEdit} onDelete={removeHolding} />

      {isModalOpen && (
        <HoldingModal
          initialData={editingHolding ?? undefined}
          onSubmit={
            editingHolding
              ? (data) => editHolding(editingHolding.id, data as HoldingUpdate)
              : (data) => addHolding(data as HoldingCreate)
          }
          onClose={handleClose}
        />
      )}
    </div>
  );
}
