"use client";

import { Treemap, ResponsiveContainer } from "recharts";
import type { DashboardHolding } from "@/lib/types";
import { formatUSD, formatPercent } from "@/lib/format";

interface Props {
  holdings: DashboardHolding[];
}

function getHeatmapColor(dailyChangePct: number): string {
  if (dailyChangePct > 0) {
    const intensity = Math.min(dailyChangePct / 5, 1);
    const r = Math.round(34 + (1 - intensity) * 180);
    const g = Math.round(197 - (1 - intensity) * 40);
    const b = Math.round(94 - (1 - intensity) * 60);
    return `rgb(${r}, ${g}, ${b})`;
  } else if (dailyChangePct < 0) {
    const intensity = Math.min(Math.abs(dailyChangePct) / 5, 1);
    const r = Math.round(239 - (1 - intensity) * 40);
    const g = Math.round(68 + (1 - intensity) * 130);
    const b = Math.round(68 + (1 - intensity) * 130);
    return `rgb(${r}, ${g}, ${b})`;
  }
  return "#9ca3af";
}

interface CustomContentProps {
  x: number;
  y: number;
  width: number;
  height: number;
  name: string;
  dailyChangePct: number;
  marketValue: number;
}

function CustomContent({
  x,
  y,
  width,
  height,
  name,
  dailyChangePct,
  marketValue,
}: CustomContentProps) {
  const showLabel = width > 50 && height > 40;
  const showDetails = width > 80 && height > 60;

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill={getHeatmapColor(dailyChangePct)}
        stroke="#0a0e2a"
        strokeWidth={2}
        rx={4}
      />
      {showLabel && (
        <>
          <text
            x={x + width / 2}
            y={y + height / 2 - (showDetails ? 12 : 0)}
            textAnchor="middle"
            dominantBaseline="central"
            fill="#fff"
            fontSize={14}
            fontWeight="bold"
          >
            {name}
          </text>
          {showDetails && (
            <>
              <text
                x={x + width / 2}
                y={y + height / 2 + 6}
                textAnchor="middle"
                dominantBaseline="central"
                fill="rgba(255,255,255,0.9)"
                fontSize={11}
              >
                {formatPercent(dailyChangePct)}
              </text>
              <text
                x={x + width / 2}
                y={y + height / 2 + 22}
                textAnchor="middle"
                dominantBaseline="central"
                fill="rgba(255,255,255,0.8)"
                fontSize={10}
              >
                {formatUSD(marketValue)}
              </text>
            </>
          )}
        </>
      )}
    </g>
  );
}

export default function Heatmap({ holdings }: Props) {
  const data = holdings.map((h) => ({
    name: h.symbol,
    size: Math.max(h.market_value, 1),
    dailyChangePct: h.daily_change_pct,
    marketValue: h.market_value,
  }));

  return (
    <div>
      <ResponsiveContainer width="100%" height={400}>
        <Treemap
          data={data}
          dataKey="size"
          content={
            <CustomContent
              x={0}
              y={0}
              width={0}
              height={0}
              name=""
              dailyChangePct={0}
              marketValue={0}
            />
          }
        />
      </ResponsiveContainer>
    </div>
  );
}
