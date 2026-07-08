'use client';

import { useEffect, useState } from 'react';
import {
  Download,
  FileText,
  Loader2,
  RefreshCw,
} from 'lucide-react';
import { getErrorMessage, reportsApi } from '@/lib/api';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import type { Report } from '@/lib/types';

const statusStyles: Record<Report['status'], string> = {
  generating: 'bg-warning/15 text-warning',
  ready: 'bg-success/15 text-success',
  failed: 'bg-danger/15 text-danger',
};

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [downloading, setDownloading] = useState<string | null>(null);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const data = await reportsApi.list();
      setReports(data);
      setError('');
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleDownload = async (report: Report) => {
    setDownloading(report.id);
    try {
      const blob = await reportsApi.download(report.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${report.title}.${report.format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setDownloading(null);
    }
  };

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <LoadingSpinner size="lg" label="Loading reports..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Reports</h1>
          <p className="mt-1 text-sm text-muted">
            Generated security assessment reports from engagements
          </p>
        </div>
        <button
          onClick={fetchReports}
          className="flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm text-muted transition-colors hover:border-accent/30 hover:text-white"
        >
          <RefreshCw className="h-4 w-4" />
          Refresh
        </button>
      </div>

      {error && (
        <div className="rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
          {error}
        </div>
      )}

      {reports.length === 0 ? (
        <div className="flex h-64 flex-col items-center justify-center rounded-xl border border-border bg-surface">
          <FileText className="mb-3 h-10 w-10 text-muted" />
          <p className="text-sm text-muted">No reports generated yet</p>
          <p className="mt-1 text-xs text-muted">
            Generate a report from an engagement detail page
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {reports.map((report) => (
            <div
              key={report.id}
              className="group rounded-xl border border-border bg-surface p-5 transition-all hover:border-accent/30 hover:shadow-glow-sm"
            >
              <div className="mb-3 flex items-start justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/10">
                  <FileText className="h-5 w-5 text-accent" />
                </div>
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${statusStyles[report.status]}`}
                >
                  {report.status}
                </span>
              </div>

              <h3 className="mb-1 text-sm font-semibold text-white line-clamp-2">
                {report.title}
              </h3>
              <p className="mb-4 text-xs text-muted">
                {new Date(report.created_at).toLocaleString()} · {report.format.toUpperCase()}
              </p>

              {report.status === 'ready' && (
                <button
                  onClick={() => handleDownload(report)}
                  disabled={downloading === report.id}
                  className="flex w-full items-center justify-center gap-2 rounded-lg bg-accent/10 py-2 text-sm font-medium text-accent transition-colors hover:bg-accent/20"
                >
                  {downloading === report.id ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Download className="h-4 w-4" />
                  )}
                  Download
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
