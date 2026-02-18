"use client";

import { Button } from "@/components/ui/button";
import { Sparkles, User, LogOut } from "lucide-react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function Navigation() {
  const { user, logout } = useAuth();

  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link
            href={user ? "/dashboard" : "/"}
            className="flex items-center gap-2"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-semibold">DataClean</span>
          </Link>

          {!user ? (
            <>
              <div className="hidden md:flex items-center gap-8">
                <Link
                  href="#features"
                  className="text-sm text-gray-600 hover:text-gray-900 transition"
                >
                  Features
                </Link>
                <Link
                  href="#pricing"
                  className="text-sm text-gray-600 hover:text-gray-900 transition"
                >
                  Pricing
                </Link>
              </div>

              <div className="flex items-center gap-3">
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    Sign In
                  </Button>
                </Link>
                <Link href="/signup">
                  <Button size="sm">Get Started</Button>
                </Link>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">
                  Dashboard
                </Button>
              </Link>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" className="gap-2">
                    <User className="w-4 h-4" />
                    <span className="hidden md:inline">
                      {user.full_name || user.email}
                    </span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>
                    <div className="flex flex-col">
                      <span className="text-sm font-medium">
                        {user.full_name}
                      </span>
                      <span className="text-xs text-gray-500">
                        {user.email}
                      </span>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href="/dashboard" className="cursor-pointer">
                      Dashboard
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/upload" className="cursor-pointer">
                      Upload File
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={logout}
                    className="text-red-600 cursor-pointer"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
