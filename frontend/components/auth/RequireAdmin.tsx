"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api/client";

export default function RequireAdmin({ children }: { children: React.ReactNode }) {
  const [allowed, setAllowed] = useState<boolean | null>(null);

  useEffect(() => {
    let mounted = true;
    api
      .get("/auth/me")
      .then((res: any) => {
        const user = res.data ?? res;
        const ok = !!user && (user.is_admin || user.is_master_user);
        if (mounted) setAllowed(ok);
        if (!ok && typeof window !== "undefined") {
          window.location.href = "/login";
        }
      })
      .catch(() => {
        if (mounted) setAllowed(false);
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      });
    return () => {
      mounted = false;
    };
  }, []);

  if (allowed === null) {
    return (
      <div className="min-h-[40vh] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400" />
      </div>
    );
  }

  if (!allowed) return null;
  return <>{children}</>;
}


