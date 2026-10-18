# MISSION — PR Power Rate (working name `pr-power-rate`)

> This repo (`pixel9-superdevice-`, empty and abandoned) is being REPURPOSED for this project.
> First task for the agent: rename the repo to `pr-power-rate` and replace this README context.

## Owner intent (Juan, 2026-10-18, verbatim intent)
Every electric utility elsewhere has providers/third parties exposing a registry, an API and even MCPs with the
current price of electricity. Puerto Rico (LUMA / PREPA / NEPR) has nothing — not even third-party portals.
One app seemed to show PR rates, probably humans manually keying LUMA's quarterly publications.

Goal: a **legitimate, public, real-time (to-the-minute) data source for the price of electricity in Puerto Rico**,
for the community. Any energy/automation platform that accepts a rate endpoint must be able to consume it:
Home Assistant, Emporia, Franklin, Tuya, and **all** others — not just these.

Pain today: rates change quarterly (fuel adjustment, purchased power, riders). Users must manually re-enter
them in ~4 apps every 3 months; people forget, and every energy number drifts out of orbit.

## Scope — find the problem AND build the solution
1. **Research**: exhaustively look for any existing digital source (LUMA, PREPA/AEE, NEPR/Negociado de Energía
   dockets and quarterly factor resolutions, OpenEI URDB, Genability/Arcadia, WattTime, EIA, any app or
   community project). Document findings in `docs/research.md` and a dead-ends registry.
2. **If no digital source exists**: build the digitizer — ingest the official analog/published sources
   (NEPR resolutions, LUMA tariff PDFs, quarterly factor announcements), parse, version, and publish.
3. **Model** the full PR residential (and commercial) tariff: fixed charge, energy charge, FCA (fuel),
   PPCA (purchased power), CILT, subsidies, riders, net-metering — effective dates and history.
4. **Deliver**:
   - Public REST/JSON endpoint: current price per kWh + full breakdown + effective period + history.
   - MCP server exposing the same.
   - Integrations/docs: Home Assistant (sensor/integration, OpenEI-compatible if possible), Emporia, Franklin,
     Tuya, and a generic format other platforms can consume.
   - Automated update pipeline + alerting when a new quarterly factor is published.
5. Use full GitHub features: Issues, Projects, Wiki, PRs, Releases.

## Constraints
- Owner prefers execution over questions; do not hand him work that can be deduced or automated.
- Data must be legitimate, sourced and citable (link every value to its official source).

## Related context
- Juan is in San Juan, PR (LUMA customer); uses Emporia + Franklin + Home Assistant.
- The GitHub connector used from claude.ai currently cannot create repos (403 "Resource not accessible by
  integration", known bug anthropics/claude-ai-mcp#822 and anthropics/claude-code#88713) — hence this repurpose.
