"use client";

import Link from "next/link";
import { useDashboard } from "@/hooks/useDashboard";
import PortfolioSummary from "@/components/dashboard/PortfolioSummary";
import Heatmap from "@/components/dashboard/Heatmap";
import AllocationChart from "@/components/dashboard/AllocationChart";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import ErrorMessage from "@/components/ui/ErrorMessage";

export default function DashboardPage() {
  const { data, loading, error, refetch } = useDashboard();

  if (loading) return <LoadingSpinner className="py-20" />;

  if (error) {
    if (error.includes("No holdings") || error.includes("not found")) {
      return (
        <div className="py-20 text-center">
          <h2 className="text-lg font-medium text-gray-900">No holdings yet</h2>
          <p className="mt-2 text-sm text-gray-500">
            Add your first holding to see your dashboard.
          </p>
          <Link
            href="/holdings"
            className="mt-4 inline-block rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Add Holdings
          </Link>
        </div>
      );
    }
    return <ErrorMessage message={error} onRetry={refetch} />;
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <PortfolioSummary
        totalValue={data.total_value}
        totalCost={data.total_cost}
        totalPnl={data.total_pnl}
        totalPnlPct={data.total_pnl_pct}
        lastUpdated={data.last_updated}
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <Heatmap holdings={data.holdings} />
        </div>
        <div>
          <AllocationChart holdings={data.holdings} />
        </div>
      </div>
    </div>
  );
}
