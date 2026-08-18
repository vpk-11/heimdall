# Graph Report - heimdall  (2026-08-18)

## Corpus Check
- 23 files · ~15,523 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 142 nodes · 212 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06d4fdfc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Customer CRM|Customer CRM]]
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
2. `detect_injection()` - 13 edges
3. `estimate_production()` - 13 edges
4. `lookup_inventory()` - 12 edges
5. `lookup_customer()` - 11 edges
6. `Heimdall` - 11 edges
7. `load_json()` - 10 edges
8. `lookup_order_history()` - 10 edges
9. `TestRedactText` - 10 edges
10. `TestDetectInjection` - 10 edges

## Surprising Connections (you probably didn't know these)
- `customer_lookup()` --calls--> `lookup_customer()`  [EXTRACTED]
  app/mcp_server/server.py → app/mcp_server/tools/customer_lookup.py
- `lookup_inventory()` --calls--> `load_json()`  [EXTRACTED]
  app/mcp_server/tools/inventory_lookup.py → app/mcp_server/tools/_shared.py
- `lookup_order_history()` --calls--> `load_json()`  [EXTRACTED]
  app/mcp_server/tools/order_history.py → app/mcp_server/tools/_shared.py
- `estimate_production()` --calls--> `load_json()`  [EXTRACTED]
  app/mcp_server/tools/production_estimate.py → app/mcp_server/tools/_shared.py
- `lookup_order_history()` --calls--> `validate_company_id()`  [EXTRACTED]
  app/mcp_server/tools/order_history.py → app/mcp_server/tools/_shared.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Tool Calls via MCP Stdio** — heimdall_gemini_2_5_flash, customer_lookup, inventory_lookup, dtc_monthly_velocity, order_history, production_estimate [EXTRACTED 0.70]
- **Mock Data Files** — mock_customers_json, mock_inventory_json, production_config_json [INFERRED 0.80]

## Communities (17 total, 4 thin omitted)

### Community 0 - "Customer CRM"
Cohesion: 0.11
Nodes (17): customer_lookup(), dtc_monthly_velocity(), inventory_lookup(), order_history(), Look up a B2B customer in the CRM by their company ID (COMP-XXX format)., Retrieve B2B order history for a customer.          Args:         company_id: Th, Retrieve the recent monthly direct-to-consumer (DTC) velocity for a product., Look up current stock levels and details for a product.          Args:         p (+9 more)

### Community 2 - "Inventory Shortfall"
Cohesion: 0.15
Nodes (16): Agent, build_test_agent(), End-to-end tests using Ollama (qwen2.5:7b via LiteLLM) instead of Gemini.  Runs, PROD-A: stock=600, DTC=400/mo, ask=100 -> shortfall=0, fulfill from stock., PROD-A: stock=600, DTC=400/mo, ask=300 -> shortfall=100, partial fulfillment., PROD-B: stock=150, DTC=100/mo, ask=500 -> shortfall=450, full production., Injection in inquiry must be blocked by before_model_callback, not reach LLM., Pipeline must not raise an unhandled exception on an unknown company ID.      Th (+8 more)

### Community 3 - "Production Estimation"
Cohesion: 0.26
Nodes (5): production_estimate(), Estimate lead time and pricing tiers for producing a given unit shortfall quanti, TestProductionEstimate, estimate_production(), Calculate lead time and cost estimates for producing a specified quantity of sho

### Community 4 - "Injection Detection"
Cohesion: 0.27
Nodes (3): detect_injection(), Detects common prompt injection keyword phrases.      Normalizes unicode (NFKC,, TestDetectInjection

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
Cohesion: 0.19
Nodes (7): TestCustomerLookup, lookup_customer(), Look up a B2B customer in the mock CRM.      Args:         company_id: The uniqu, load_json(), Loads a JSON fixture file. Shared by every tool reading mock_server/data/*.json., validate_company_id(), validate_product_id()

## Knowledge Gaps
- **16 isolated node(s):** `deploy.sh script`, `start.sh script`, `Why it exists`, `Architecture`, `How this was built` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `redact_text()` connect `PII Redaction` to `Injection Detection`, `Callback Handling`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `estimate_production()` connect `Production Estimation` to `Customer CRM`, `Mock Customers`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `detect_injection()` connect `Injection Detection` to `Callback Handling`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **What connects `Redacts PII (email, phone, address, and name patterns) from text.`, `Detects common prompt injection keyword phrases.      Normalizes unicode (NFKC,`, `Runs before the LLM call.          Redacts PII from the raw inquiry text before` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Customer CRM` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `Inventory Shortfall` be split into smaller, more focused modules?**
  _Cohesion score 0.14619883040935672 - nodes in this community are weakly interconnected._
- **Should `Inventory Lookup` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._