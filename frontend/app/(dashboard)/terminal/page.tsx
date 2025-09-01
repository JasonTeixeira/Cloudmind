"use client";

import { useState } from "react";
import { useAiPlan, useAiExecute } from "@/lib/hooks/useApi";
import DashboardLayout from "@/components/layouts/DashboardLayout";

export default function TerminalPage() {
  const [objective, setObjective] = useState("");
  const [command, setCommand] = useState("");
  const [logs, setLogs] = useState<string>("");
  const plan = useAiPlan();
  const exec = useAiExecute();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Terminal</h1>
          <p className="text-gray-600">Plan and dry-run commands with guardrails.</p>
        </div>

        <div className="card p-4">
          <label className="block text-sm text-gray-700 mb-2">Objective</label>
          <textarea
            className="w-full border rounded p-2"
            rows={3}
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
          />
          <div className="mt-3">
            <button
              className="btn-primary"
              onClick={async () => {
                const res: any = await plan.mutateAsync({ objective });
                setLogs(JSON.stringify(res, null, 2));
              }}
            >
              Plan
            </button>
          </div>
        </div>

        <div className="card p-4">
          <label className="block text-sm text-gray-700 mb-2">Command</label>
          <input
            className="w-full border rounded p-2"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
          />
          <div className="mt-3 flex gap-2">
            <button
              className="btn-secondary"
              onClick={async () => {
                const res: any = await exec.mutateAsync({ command, dry_run: true });
                setLogs(JSON.stringify(res, null, 2));
              }}
            >
              Dry Run
            </button>
          </div>
        </div>

        {logs && (
          <div className="card p-4">
            <pre className="text-xs whitespace-pre-wrap">{logs}</pre>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}



