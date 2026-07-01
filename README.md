# kilimo-mcp

[![kilimo-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/kilimo-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/kilimo-mcp)
[![smithery badge](https://smithery.ai/badge/@gabrielmahia/kilimo-mcp)](https://smithery.ai/server/@gabrielmahia/kilimo-mcp)


---
**Compatible with `claude-sonnet-5`** (released 2026-06-30) — Anthropic's most agentic
Sonnet yet. Runs multi-step tool chains end-to-end without stopping short.
Install: `pip install kilimo-mcp` · Use with any MCP client.

---


> Kenya precision agriculture via MCP — crop calendar, fertilizer, pest alerts, KALRO varieties

[![PyPI](https://img.shields.io/badge/PyPI-v0.1.0-blue)](https://github.com/gabrielmahia/kilimo-mcp)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/gabrielmahia/kilimo-mcp)
[![Layer](https://img.shields.io/badge/Layer-Social-purple)](https://github.com/gabrielmahia/kilimo-mcp)

## Install

```bash
pip install kilimo-mcp
```

## What it does

6 MCP tools covering Kenya precision agriculture. 1st world equivalent: **Climate Corp / Granular**.

| Tool | Description |
|------|-------------|
| `crop_calendar` | Kenya crop planting and harvesting calendar by region |
| `fertilizer_guide` | Fertilizer recommendations by crop and soil type |
| `pest_disease_alert` | Crop pest and disease identification and management |
| `market_timing_guide` | Best timing to sell produce based on price cycles |
| `kalro_varieties` | KALRO improved crop variety recommendations |
| `input_cost_calculator` | Kenya farm input cost calculator and comparison |

## Usage

```bash
# Run as standalone MCP server
kilimo-mcp

# Or add to Claude Desktop / any MCP client
# Add to your MCP config: {"command": "kilimo-mcp"}
```

## Part of the Kenya Coordination Infrastructure Stack

This is one of 23 MCP servers covering the full coordination infrastructure of East Africa:

**Economic:** mpesa · mkopo · bima · soko · sifa · remit · kra · faida  
**Physical:** wapimaji · nishati · usafiri · ardhi  
**Social:** afya · afya-ya-akili · elimu · kazi · haki-ya-kazi · kilimo · jumuia  
**Civic:** nyumba · habari · mazingira · civic-agent-kit  

→ [The Nairobi Stack](https://gabrielmahia.github.io/nairobi-stack)  
→ [Full Portfolio](https://gabrielmahia.github.io)

## Trust Integrity

All data in this server is **clearly labeled DEMO** where synthetic. Verify all operational data with the relevant Kenyan government authority before use.

## License

MIT © Gabriel Mahia | [AI-KungFU](https://github.com/gabrielmahia) | contact@aikungfu.dev

> *Decision infrastructure for East Africa*

## Part of the East Africa Coordination Stack

This MCP server is one of 32 tools in the Kenya coordination infrastructure.
It connects to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) — the coordination
event bus that routes signals between domains automatically.

When this server detects a threshold condition, the bus notifies:
- `bima-mcp` — parametric insurance evaluation
- `kilimo-mcp` — agricultural advisory
- `afya-mcp` — health surveillance activation
- `county-mcp` — county office alert

```python
pip install africa-coord-bus
```

All servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)