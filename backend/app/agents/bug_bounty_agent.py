"""Autonomous LLM-driven bug bounty hunter with tool calling."""
from __future__ import annotations

import logging
from typing import Optional

from app.agents.base import AgentResult, BaseAgent
from app.services.agent_loop import run_agent_loop

logger = logging.getLogger(__name__)


class BugBountyAgent(BaseAgent):
    name = "BugBountyAgent"
    description = (
        "Autonomous bug bounty copilot: web search, CVE intel, HTTP probing, "
        "nuclei/nmap, payload generation, scope-aware finding reports"
    )

    async def run(self, target: dict, context: dict) -> AgentResult:
        url = target.get("url") or target.get("ip_address") or ""
        scope_domains = context.get("scope_domains") or []
        if not scope_domains and url:
            from urllib.parse import urlparse
            host = urlparse(url if "://" in url else f"https://{url}").hostname
            if host:
                scope_domains = [host]

        max_iterations = context.get("max_iterations", 15)
        on_event = context.get("on_event")
        findings: list[dict] = []
        tool_log: list[dict] = []

        goal = self._build_goal(target, scope_domains)

        loop_ctx = {
            "scope_domains": scope_domains,
            "target_url": url,
            "findings_collector": findings,
        }

        async def event_bridge(event_type: str, data: dict):
            tool_log.append({"event": event_type, **data})
            if on_event:
                await on_event(event_type, data)

        try:
            result = await run_agent_loop(
                goal,
                context=loop_ctx,
                max_iterations=max_iterations,
                on_event=event_bridge,
                temperature=0.35,
            )
            findings = result.findings or findings

            return AgentResult(
                agent_name=self.name,
                status="success",
                findings=findings,
                tool_outputs={
                    "final_answer": result.final_answer,
                    "iterations": result.iterations,
                    "tool_calls": result.tool_calls_made,
                    "tool_events": tool_log,
                    "status": result.status,
                },
            )
        except Exception as exc:
            logger.exception("BugBountyAgent failed")
            return AgentResult(
                agent_name=self.name,
                status="failed",
                findings=findings,
                tool_outputs={"tool_events": tool_log},
                error=str(exc),
            )

    def _build_goal(self, target: dict, scope_domains: list[str]) -> str:
        parts = [
            "Conduct a thorough bug bounty security assessment on the authorized target.",
            f"Target type: {target.get('target_type', 'web')}",
        ]
        if target.get("url"):
            parts.append(f"URL: {target['url']}")
        if target.get("ip_address"):
            parts.append(f"IP: {target['ip_address']}")
        if target.get("code_path"):
            parts.append(f"Source code path: {target['code_path']}")
        if scope_domains:
            parts.append(f"In-scope domains: {', '.join(scope_domains)}")
        if target.get("tech_stack"):
            parts.append(f"Tech stack hints: {target['tech_stack']}")
        if target.get("notes"):
            parts.append(f"Notes: {target['notes']}")

        parts.append(
            "\nWorkflow: (1) scope check (2) DNS/HTTP recon (3) web search for known vulns "
            "(4) nuclei/nmap if appropriate (5) manual hypothesis testing with payloads "
            "(6) report_finding for each vulnerability (7) final summary."
        )
        return "\n".join(parts)
