# Graph Report - heimdall  (2026-07-05)

## Corpus Check
- 22 files · ~14,238 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 163 nodes · 214 edges · 20 communities (15 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4a35f88`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Customer CRM|Customer CRM]]
- [[_COMMUNITY_Model Callbacks|Model Callbacks]]
- [[_COMMUNITY_Inventory Shortfall|Inventory Shortfall]]
- [[_COMMUNITY_Production Estimation|Production Estimation]]
- [[_COMMUNITY_Injection Detection|Injection Detection]]
- [[_COMMUNITY_PII Redaction|PII Redaction]]
- [[_COMMUNITY_Callback Handling|Callback Handling]]
- [[_COMMUNITY_Inventory Lookup|Inventory Lookup]]
- [[_COMMUNITY_Feasibility Math|Feasibility Math]]
- [[_COMMUNITY_Deployment Script|Deployment Script]]
- [[_COMMUNITY_Start Script|Start Script]]
- [[_COMMUNITY_MCP Integration|MCP Integration]]
- [[_COMMUNITY_Mock Customers|Mock Customers]]
- [[_COMMUNITY_Requirements|Requirements]]
- [[_COMMUNITY_Community 21|Community 21]]

## God Nodes (most connected - your core abstractions)
1. `redact_text()` - 14 edges
2. `Heimdall` - 13 edges
3. `detect_injection()` - 12 edges
4. `estimate_production()` - 12 edges
5. `Heimdall` - 10 edges
6. `TestRedactText` - 10 edges
7. `before_model_callback()` - 9 edges
8. `lookup_customer()` - 9 edges
9. `TestDetectInjection` - 9 edges
10. `lookup_inventory()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `customer_lookup()` --calls--> `lookup_customer()`  [EXTRACTED]
  mcp_server/server.py → mcp_server/tools/customer_lookup.py
- `Cloud Run Deployment` ----> `Heimdall Agent`  [EXTRACTED]
  heimdall/scripts/deploy.sh → heimdall/app/agent.py
- `Heimdall Agent` ----> `After Model Callback`  [EXTRACTED]
  heimdall/app/agent.py → heimdall/app/callbacks.py
- `Heimdall Agent` ----> `Before Model Callback`  [EXTRACTED]
  heimdall/app/agent.py → heimdall/app/callbacks.py
- `Heimdall Agent` ----> `Customer Lookup Tool`  [EXTRACTED]
  heimdall/app/agent.py → heimdall/mcp_server/tools/customer_lookup.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Tool Calls via MCP Stdio** — heimdall_gemini_2_5_flash, customer_lookup, inventory_lookup, dtc_monthly_velocity, order_history, production_estimate [EXTRACTED 0.70]
- **Mock Data Files** — mock_customers_json, mock_inventory_json, production_config_json [INFERRED 0.80]

## Communities (20 total, 5 thin omitted)

### Community 0 - "Customer CRM"
Cohesion: 0.10
Nodes (17): customer_lookup(), dtc_monthly_velocity(), inventory_lookup(), order_history(), Look up a B2B customer in the CRM by their company ID (COMP-XXX format)., Retrieve B2B order history for a customer.          Args:         company_id: Th, Retrieve the recent monthly direct-to-consumer (DTC) velocity for a product., Look up current stock levels and details for a product.          Args:         p (+9 more)

### Community 1 - "Model Callbacks"
Cohesion: 0.17
Nodes (12): After Model Callback, After Model Callback Signatures, Before Model Callback, Before Model Callback Signatures, Cloud Run Deployment, Customer Lookup Tool, Heimdall Agent, Inventory Lookup Tool (+4 more)

### Community 2 - "Inventory Shortfall"
Cohesion: 0.16
Nodes (16): Agent, build_test_agent(), End-to-end tests using Ollama (qwen2.5:7b via LiteLLM) instead of Gemini.  Runs, PROD-A: stock=600, DTC=400/mo, ask=100 -> shortfall=0, fulfill from stock., PROD-A: stock=600, DTC=400/mo, ask=300 -> shortfall=100, partial fulfillment., PROD-B: stock=150, DTC=100/mo, ask=500 -> shortfall=450, full production., Injection in inquiry must be blocked by before_model_callback, not reach LLM., Pipeline must not raise an unhandled exception on an unknown company ID.      Th (+8 more)

### Community 3 - "Production Estimation"
Cohesion: 0.23
Nodes (5): production_estimate(), Estimate lead time and pricing tiers for producing a given unit shortfall quanti, TestProductionEstimate, estimate_production(), Calculate lead time and cost estimates for producing a specified quantity of sho

### Community 4 - "Injection Detection"
Cohesion: 0.29
Nodes (3): detect_injection(), Detects common prompt injection keyword phrases., TestDetectInjection

### Community 5 - "PII Redaction"
Cohesion: 0.29
Nodes (3): Redacts PII (email, phone, address, and name patterns) from text., redact_text(), TestRedactText

### Community 6 - "Callback Handling"
Cohesion: 0.33
Nodes (7): after_model_callback(), before_model_callback(), Runs after the LLM call.          Checks the drafted response for leaked PII or, Runs before the LLM call.          Redacts PII from the raw inquiry text before, CallbackContext, LlmRequest, LlmResponse

### Community 7 - "Inventory Lookup"
Cohesion: 0.13
Nodes (14): Architecture, Deployment, Environment variables, Heimdall, How this was built, Local dev, Mock data, Quickstart (+6 more)

### Community 15 - "Mock Customers"
Cohesion: 0.36
Nodes (3): TestCustomerLookup, lookup_customer(), Look up a B2B customer in the mock CRM.          Args:         company_id: The u

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (16): 2026-06-26 — Initial Build, Changelog, Critical Snippets, Environment Modes, graphify, Heimdall, Implementation Phases, Local Dev (+8 more)

## Knowledge Gaps
- **37 isolated node(s):** `Why it exists`, `Architecture`, `How this was built`, `Requirements`, `Local dev` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `redact_text()` connect `PII Redaction` to `Injection Detection`, `Callback Handling`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `estimate_production()` connect `Production Estimation` to `Customer CRM`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `detect_injection()` connect `Injection Detection` to `Callback Handling`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **What connects `Why it exists`, `Architecture`, `How this was built` to the rest of the system?**
  _59 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Customer CRM` be split into smaller, more focused modules?**
  _Cohesion score 0.10114942528735632 - nodes in this community are weakly interconnected._
- **Should `Inventory Lookup` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `Community 21` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._