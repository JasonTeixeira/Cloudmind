"use client";

import { useEffect, useState } from "react";
import api, { usersApi } from "@/lib/api/client";

export default function UsersTable() {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        // Try common users endpoint; fallback to empty
        const res: any = await usersApi.list();
        if (mounted) setRows(res ?? []);
      } catch (e: any) {
        if (mounted) {
          setRows([]);
          setError('Could not load users');
        }
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-[120px] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400" />
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      {error && <div className="mb-3 text-sm text-red-600">{error}</div>}
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-gray-600">
            <th className="py-2 pr-6">Email</th>
            <th className="py-2 pr-6">Name</th>
            <th className="py-2 pr-6">Role</th>
            <th className="py-2 pr-6">Active</th>
            <th className="py-2 pr-6">Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((u) => (
            <tr key={u.id} className="border-t">
              <td className="py-2 pr-6 text-gray-900">{u.email}</td>
              <td className="py-2 pr-6 text-gray-700">{u.full_name || u.username || "—"}</td>
              <td className="py-2 pr-6 text-gray-700">
                <select
                  className="border rounded p-1 text-xs"
                  value={u.is_master_user ? 'master' : u.is_admin ? 'admin' : 'user'}
                  onChange={async (e) => {
                    const newRole = e.target.value as 'master' | 'admin' | 'user'
                    setError(null)
                    try {
                      await usersApi.setRole(u.id, newRole)
                      setRows((prev)=> prev.map((x)=> x.id===u.id ? { ...x, is_master_user: newRole==='master', is_admin: newRole==='admin' } : x))
                    } catch {
                      setError('Failed to update role')
                    }
                  }}
                >
                  <option value="user">user</option>
                  <option value="admin">admin</option>
                  <option value="master">master</option>
                </select>
              </td>
              <td className="py-2 pr-6 text-gray-700">{u.is_active ? "Yes" : "No"}</td>
              <td className="py-2 pr-6 text-gray-700">
                {u.is_active ? (
                  <button
                    className="text-red-600 hover:underline text-xs mr-2"
                    onClick={async ()=>{
                      setError(null)
                      try {
                        await usersApi.deactivate(u.id)
                        setRows((prev)=> prev.map((x)=> x.id===u.id ? { ...x, is_active: false } : x))
                      } catch {
                        setError('Failed to deactivate user')
                      }
                    }}
                  >
                    Deactivate
                  </button>
                ) : (
                  <button
                    className="text-green-600 hover:underline text-xs mr-2"
                    onClick={async ()=>{
                      setError(null)
                      try {
                        await usersApi.activate(u.id)
                        setRows((prev)=> prev.map((x)=> x.id===u.id ? { ...x, is_active: true } : x))
                      } catch {
                        setError('Failed to activate user')
                      }
                    }}
                  >
                    Activate
                  </button>
                )}
              </td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td className="py-6 text-gray-500" colSpan={5}>No users found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}


