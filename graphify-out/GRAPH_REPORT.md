# Graph Report - heimdall  (2026-07-16)

## Corpus Check
- 22 files · ~15,423 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 136 nodes · 190 edges · 18 communities (14 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `123d4213`
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
- [[_COMMUNITY_Mock Customers|Mock Customers]]
- [[_COMMUNITY_Requirements|Requirements]]

## God Nodes (most connected - your core abstractions)
1. `redact_text()` - 14 edges
2. `detect_injection()` - 12 edges
3. `estimate_production()` - 12 edges
4. `Heimdall` - 11 edges
5. `TestRedactText` - 10 edges
6. `before_model_callback()` - 9 edges
7. `lookup_customer()` - 9 edges
8. `TestDetectInjection` - 9 edges
9. `run_inquiry()` - 8 edges
10. `lookup_inventory()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `order_history()` --calls--> `lookup_order_history()`  [EXTRACTED]
  mcp_server/server.py → mcp_server/tools/order_history.py
- `dtc_monthly_velocity()` --calls--> `get_dtc_monthly_velocity()`  [EXTRACTED]
  mcp_server/server.py → mcp_server/tools/order_history.py
- `customer_lookup()` --calls--> `lookup_customer()`  [EXTRACTED]
  mcp_server/server.py → mcp_server/tools/customer_lookup.py
- `inventory_lookup()` --calls--> `lookup_inventory()`  [EXTRACTED]
  mcp_server/server.py → mcp_server/tools/inventory_lookup.py
- `production_estimate()` --calls--> `estimate_production()`  [EXTRACTED]
  mcp_server/server.py → mcp_server/tools/production_estimate.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Tool Calls via MCP Stdio** — heimdall_gemini_2_5_flash, customer_lookup, inventory_lookup, dtc_monthly_velocity, order_history, production_estimate [EXTRACTED 0.70]
- **Mock Data Files** — mock_customers_json, mock_inventory_json, production_config_json [INFERRED 0.80]

## Communities (18 total, 4 thin omitted)

### Community 0 - "Customer CRM"
Cohesion: 0.22
Nodes (6): TestDtcVelocity, TestOrderHistory, get_dtc_monthly_velocity(), lookup_order_history(), Get the recent direct-to-consumer (DTC) monthly order velocity for a product., Look up order history for a specific company ID.          Args:         company_

### Community 1 - "Model Callbacks"
Cohesion: 0.28
Nodes (5): inventory_lookup(), Look up current stock levels and details for a product.          Args:         p, TestInventoryLookup, lookup_inventory(), Look up current stock level and details for a given product.          Args:

### Community 2 - "Inventory Shortfall"
Cohesion: 0.15
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
Cohesion: 0.12
Nodes (15): Architecture, Changelog, Deployment, Environment variables, Heimdall, How this was built, Local dev, Mock data (+7 more)

### Community 15 - "Mock Customers"
Cohesion: 0.17
Nodes (9): customer_lookup(), dtc_monthly_velocity(), order_history(), Look up a B2B customer in the CRM by their company ID (COMP-XXX format)., Retrieve B2B order history for a customer.          Args:         company_id: Th, Retrieve the recent monthly direct-to-consumer (DTC) velocity for a product., TestCustomerLookup, lookup_customer() (+1 more)

## Knowledge Gaps
- **16 isolated node(s):** `Why it exists`, `Architecture`, `How this was built`, `Requirements`, `Local dev` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `redact_text()` connect `PII Redaction` to `Injection Detection`, `Callback Handling`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `detect_injection()` connect `Injection Detection` to `Callback Handling`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `estimate_production()` connect `Production Estimation` to `Customer CRM`, `Mock Customers`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **What connects `Why it exists`, `Architecture`, `How this was built` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Inventory Shortfall` be split into smaller, more focused modules?**
  _Cohesion score 0.14619883040935672 - nodes in this community are weakly interconnected._
- **Should `Inventory Lookup` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._