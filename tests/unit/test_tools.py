"""Unit tests for tool registry."""
import pytest

import app.tools.bootstrap  # noqa: F401
from app.tools.registry import tool_registry
from app.tools.security_tools import check_scope, generate_payloads


def test_tools_registered():
    tools = tool_registry.list_tools()
    names = {t.name for t in tools}
    assert "web_search" in names
    assert "http_probe" in names
    assert "report_finding" in names
    assert len(tools) >= 10


@pytest.mark.anyio
async def test_check_scope_in_scope():
    result = check_scope("https://api.example.com/v1", ["example.com"])
    assert result["in_scope"] is True


@pytest.mark.anyio
async def test_check_scope_out_of_scope():
    result = check_scope("https://evil.com", ["example.com"])
    assert result["in_scope"] is False


def test_generate_payloads():
    r = generate_payloads("xss")
    assert r["count"] > 0
    assert any("script" in p.lower() for p in r["payloads"])


@pytest.mark.anyio
async def test_report_finding_tool():
    collector = []
    result = await tool_registry.execute(
        "report_finding",
        {
            "title": "Test XSS",
            "severity": "high",
            "description": "Reflected XSS in search param",
        },
        {"findings_collector": collector},
    )
    assert result["success"] is True
    assert len(collector) == 1
