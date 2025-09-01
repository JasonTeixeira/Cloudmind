"use client";

import { ShieldCheck, Users, DollarSign, Settings } from "lucide-react";
import DashboardLayout from "@/components/layouts/DashboardLayout";
import RequireAdmin from "@/components/auth/RequireAdmin";
import api from "@/lib/api/client";
import { useEffect, useState } from "react";
import UsersTable from "@/components/admin/UsersTable";
import PricingRulesTable from "@/components/admin/PricingRulesTable";

export default function AdminPage() {
  const [serviceTokens, setServiceTokens] = useState<any[]>([]);
  useEffect(() => {
    api
      .get("/pricing/tokens")
      .then((res: any) => setServiceTokens(res.data ?? res))
      .catch(() => setServiceTokens([]));
  }, []);

  return (
    <RequireAdmin>
      <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-blue-600" /> Admin Console
          </h1>
          <p className="text-gray-600">Manage users, pricing, and platform settings.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Users</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg"><Users className="w-6 h-6 text-blue-600" /></div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Pricing Rules</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
              <div className="p-3 bg-green-100 rounded-lg"><DollarSign className="w-6 h-6 text-green-600" /></div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Settings</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg"><Settings className="w-6 h-6 text-purple-600" /></div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Users</h2>
          </div>
          <UsersTable />
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Service Tokens</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-gray-600">
                  <th className="py-2 pr-6">Name</th>
                  <th className="py-2 pr-6">Category</th>
                  <th className="py-2 pr-6">Unit</th>
                  <th className="py-2 pr-6">Base Price</th>
                  <th className="py-2 pr-6">Active</th>
                </tr>
              </thead>
              <tbody>
                {serviceTokens.map((t) => (
                  <tr key={t.id} className="border-t">
                    <td className="py-2 pr-6 text-gray-900">{t.name}</td>
                    <td className="py-2 pr-6 text-gray-700 capitalize">{t.category}</td>
                    <td className="py-2 pr-6 text-gray-700">{t.unit_type}</td>
                    <td className="py-2 pr-6 text-gray-900">${Number(t.base_price).toFixed(2)}</td>
                    <td className="py-2 pr-6 text-gray-700">{t.is_active ? 'Yes' : 'No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Pricing Rules</h2>
          </div>
          <PricingRulesTable />
        </div>
      </div>
      </DashboardLayout>
    </RequireAdmin>
  );
}


