"use client";

import ClientPortalDashboard from '@/components/client/ClientPortalDashboard';
import { useProjects } from '@/lib/hooks/useApi';

export default function ClientPortalPage() {
  const { data, isLoading } = useProjects();
  return <ClientPortalDashboard projectCount={isLoading ? undefined : (data?.length || 0)} />;
}
