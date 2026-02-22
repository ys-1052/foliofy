"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

export default function Header() {
  const pathname = usePathname();
  const { signOut } = useAuth();

  const handleSignOut = async () => {
    if (confirm("Are you sure you want to sign out?")) {
      await signOut();
    }
  };

  return (
    <header className="border-b border-gray-700/50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center justify-between">
          <Link href="/" className="text-xl font-bold text-white">
            Foliofy
          </Link>
          <nav className="flex gap-4 items-center">
            <Link
              href="/holdings"
              className={`text-sm font-medium px-4 py-1.5 rounded border transition-colors ${
                pathname === "/holdings"
                  ? "border-white text-white"
                  : "border-gray-500 text-gray-300 hover:border-white hover:text-white"
              }`}
            >
              Holdings
            </Link>
            <button
              onClick={handleSignOut}
              className="text-sm font-medium px-4 py-1.5 rounded border border-gray-500 text-gray-300 hover:border-white hover:text-white transition-colors"
            >
              Sign Out
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}
