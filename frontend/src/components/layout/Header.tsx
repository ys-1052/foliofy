"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/holdings", label: "Holdings" },
];

export default function Header() {
  const pathname = usePathname();
  const { signOut } = useAuth();

  const handleSignOut = async () => {
    if (confirm("Are you sure you want to sign out?")) {
      await signOut();
    }
  };

  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center justify-between">
          <Link href="/" className="text-xl font-bold text-gray-900">
            Foliofy
          </Link>
          <nav className="flex gap-6 items-center">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`text-sm font-medium transition-colors ${
                  pathname === item.href ? "text-blue-600" : "text-gray-500 hover:text-gray-900"
                }`}
              >
                {item.label}
              </Link>
            ))}
            <button
              onClick={handleSignOut}
              className="text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors"
            >
              Sign Out
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}
