'use client';

import { useEffect, useState } from 'react';
import {
  Bug,
  Globe,
  Loader2,
  Play,
  Search,
  Shield,
  Wrench,
} from 'lucide-react';
import { bugBountyApi, getErrorMessage, toolsApi } from '@/lib/api';
import { useToast } from '@/components/ui/Toast';
import SeverityBadge from '@/components/ui/SeverityBadge';
import type { Finding, HuntJob, ToolInfo } from '@/lib/types';

export default function BugBountyPage() {
  const { success, error: toastError } = useToast();
  const [targetUrl, setTargetUrl] = useState('https://');
  const [scope, setScope] = useState('');
  const [notes, setNotes] = useState('');
  const [maxIter, setMaxIter] = useState(15);
  const [loading, setLoading] = useState(false);
  const [job, setJob] = useState<HuntJob | null>(null);
  const [tools, setTools] = useState<ToolInfo[]>([]);

  useEffect(() => {
    toolsApi.list().then((d) => setTools(d.tools)).catch(() => {});
  }, []);

  const startHunt = async () => {
    if (!targetUrl.trim()) return;
    setLoading(true);
    setJob(null);
    try {
      const scopeDomains = scope.split(',').map((s) => s.trim()).filter(Boolean);
      const { job_id } = await bugBountyApi.startHunt(targetUrl, scopeDomains, maxIter, notes);
      success('Hunt started', `Job ${job_id} — autonomous agent running`);
      poll(job_id);
    } catch (err) {
      toastError('Failed to start hunt', getErrorMessage(err));
      setLoading(false);
    }
  };

  const poll = (jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const status = await bugBountyApi.getHunt(jobId);
        setJob(status as HuntJob);
        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
        }
      } catch {
        clearInterval(interval);
        setLoading(false);
      }
    }, 4000);
  };

  const findings = (job?.findings || []) as Finding[];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Bug className="h-7 w-7 text-accent" />
          Autonomous Bug Bounty Copilot
        </h1>
        <p className="mt-1 text-sm text-muted">
          LLM-driven hunter with web search, CVE intel, HTTP probing, nuclei/nmap, and scope-aware reporting
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-4 rounded-xl border border-border bg-surface p-6">
          <div>
            <label className="text-sm text-muted flex items-center gap-2 mb-1">
              <Globe className="h-4 w-4" /> Target URL
            </label>
            <input
              className="w-full bg-background border border-border rounded-lg px-3 py-2 text-white"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              placeholder="https://target.example.com"
            />
          </div>
          <div>
            <label className="text-sm text-muted mb-1 block">Scope domains (comma-separated)</label>
            <input
              className="w-full bg-background border border-border rounded-lg px-3 py-2 text-white"
              value={scope}
              onChange={(e) => setScope(e.target.value)}
              placeholder="example.com, *.example.com"
            />
          </div>
          <div>
            <label className="text-sm text-muted mb-1 block">Program notes / rules</label>
            <textarea
              className="w-full h-20 bg-background border border-border rounded-lg px-3 py-2 text-white text-sm"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Out of scope: social engineering, DoS..."
            />
          </div>
          <div className="flex items-center gap-4">
            <label className="text-sm text-muted">Max iterations</label>
            <input
              type="number"
              min={5}
              max={30}
              value={maxIter}
              onChange={(e) => setMaxIter(parseInt(e.target.value, 10))}
              className="w-20 bg-background border border-border rounded px-2 py-1 text-white"
            />
          </div>
          <button
            onClick={startHunt}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-accent hover:bg-accent-hover disabled:opacity-50 text-white py-3 rounded-lg font-semibold"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Play className="h-5 w-5" />}
            {loading ? 'Autonomous hunt in progress...' : 'Launch Autonomous Hunt'}
          </button>
        </div>

        <div className="rounded-xl border border-border bg-surface p-5">
          <h2 className="text-white font-semibold flex items-center gap-2 mb-3">
            <Wrench className="h-4 w-4 text-accent" />
            Tools ({tools.length})
          </h2>
          <ul className="space-y-2 max-h-80 overflow-y-auto text-xs">
            {tools.map((t) => (
              <li key={t.name} className="rounded-lg bg-background/50 px-2 py-1.5">
                <span className="font-mono text-accent">{t.name}</span>
                <span className="ml-2 text-muted capitalize">[{t.category}]</span>
                <p className="text-muted mt-0.5 line-clamp-2">{t.description}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {job && (
        <div className="rounded-xl border border-border bg-surface p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Hunt Status: {job.job_id}
            </h2>
            <span className={`text-sm font-medium capitalize ${
              job.status === 'completed' ? 'text-green-400' : job.status === 'failed' ? 'text-red-400' : 'text-yellow-400'
            }`}>
              {job.status}
            </span>
          </div>

          {job.summary && (
            <div className="rounded-lg bg-background/50 p-4 text-sm text-slate-300 whitespace-pre-wrap">
              {job.summary}
            </div>
          )}

          {job.error && <p className="text-red-400 text-sm">{job.error}</p>}

          {findings.length > 0 && (
            <div>
              <h3 className="text-white font-medium mb-2">Findings ({findings.length})</h3>
              <div className="space-y-2">
                {findings.map((f, i) => (
                  <div key={i} className="rounded-lg border border-border bg-background/30 p-3">
                    <div className="flex items-center gap-2 mb-1">
                      <SeverityBadge severity={f.severity as 'high'} />
                      <span className="font-medium text-white">{f.title}</span>
                    </div>
                    <p className="text-sm text-muted">{f.description}</p>
                    {f.payload && <pre className="mt-2 text-xs text-green-400 overflow-x-auto">{f.payload}</pre>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {job.tool_calls && job.tool_calls.length > 0 && (
            <details className="text-sm">
              <summary className="cursor-pointer text-muted flex items-center gap-1">
                <Search className="h-4 w-4" />
                Tool calls ({job.tool_calls.length})
              </summary>
              <pre className="mt-2 max-h-64 overflow-auto text-xs bg-background p-3 rounded">
                {JSON.stringify(job.tool_calls, null, 2)}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
