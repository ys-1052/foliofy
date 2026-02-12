import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Foliofy - 保有株管理ツール",
  description: "米国株の保有資産を視覚化・管理",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
