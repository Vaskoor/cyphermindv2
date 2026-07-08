"""NVIDIA NIM chat completions with tool-calling support."""
from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMError(Exception):
    """Raised when the LLM API call fails."""


async def chat_completion_raw(
    messages: list[dict[str, Any]],
    *,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    top_p: float = 1.0,
    model: Optional[str] = None,
    tools: Optional[list[dict]] = None,
    tool_choice: str | dict = "auto",
) -> dict[str, Any]:
    """Return full OpenAI-compatible message object."""
    api_key = settings.nvidia_api_key
    if not api_key:
        raise LLMError("NVIDIA_API_KEY is not set. Add it to your .env file.")

    payload: dict[str, Any] = {
        "model": model or settings.llm_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stream": False,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = tool_choice

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    url = f"{settings.nvidia_api_base.rstrip('/')}/chat/completions"

    async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
        try:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:800]
            # Retry without tools if model rejects tool calling
            if tools and exc.response.status_code in (400, 422):
                logger.warning("Model rejected tools payload, retrying without tools")
                return await chat_completion_raw(
                    messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    model=model,
                    tools=None,
                )
            raise LLMError(f"NVIDIA API error {exc.response.status_code}: {detail}") from exc
        except httpx.RequestError as exc:
            raise LLMError(f"NVIDIA API unreachable: {exc}") from exc

    try:
        return data["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"Unexpected NVIDIA API response: {data}") from exc


async def chat_completion(
    messages: list[dict[str, Any]],
    *,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    top_p: float = 1.0,
    model: Optional[str] = None,
    tools: Optional[list[dict]] = None,
) -> str:
    msg = await chat_completion_raw(
        messages, temperature=temperature, max_tokens=max_tokens,
        top_p=top_p, model=model, tools=tools,
    )
    return msg.get("content") or ""


def parse_react_tool_calls(content: str) -> list[dict]:
    """
    Fallback parser when model returns text-based tool calls:
    ```json
    {"tool": "web_search", "arguments": {"query": "..."}}
    ```
    """
    calls = []
    for block in re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL):
        try:
            obj = json.loads(block)
            if "tool" in obj:
                calls.append({"name": obj["tool"], "arguments": obj.get("arguments", {})})
        except json.JSONDecodeError:
            continue
    # Also match TOOL: name / ARGS: {...} pattern
    tool_match = re.search(r"TOOL:\s*(\w+)\s+ARGS:\s*(\{.*\})", content, re.DOTALL)
    if tool_match:
        try:
            calls.append({
                "name": tool_match.group(1),
                "arguments": json.loads(tool_match.group(2)),
            })
        except json.JSONDecodeError:
            pass
    return calls


async def check_llm_health() -> dict:
    if not settings.nvidia_api_key:
        return {"online": False, "models": [], "provider": "nvidia", "error": "API key not configured"}
    try:
        reply = await chat_completion(
            [{"role": "user", "content": "Reply with exactly: ok"}],
            temperature=0,
            max_tokens=8,
        )
        search_backend = "google" if settings.google_api_key else "duckduckgo"
        return {
            "online": True,
            "models": [settings.llm_model],
            "provider": "nvidia",
            "version": settings.nvidia_api_base,
            "test_reply": reply.strip()[:32],
            "web_search_backend": search_backend,
            "tools_enabled": True,
        }
    except LLMError as exc:
        return {"online": False, "models": [settings.llm_model], "provider": "nvidia", "error": str(exc)}
