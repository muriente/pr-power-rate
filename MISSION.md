# MISSION — PR Power Rate (working name `pr-power-rate`)

> This repo (`pixel9-superdevice-`, empty and abandoned) is being REPURPOSED for this project.
> First task for the agent: rename the repo to `pr-power-rate` and replace this README context.

## ⚠️ RULE ZERO — Research before building (owner's explicit instruction)
Do NOT assume this doesn't exist. Juan already uses an app (he doesn't recall which) that receives PR rates
**automatically**. He assumed the vendor keys LUMA's quarterly numbers in manually to cover the gap — but that
means someone may ALREADY have digitized this data.

Order of operations:
1. Find out whether LUMA/NEPR publishes it natively in any machine-readable form.
2. Find who already digitized it (apps, energy-monitor vendors, OpenEI URDB entries, Arcadia/Genability, HA
   community, GitHub). Identify the app Juan uses — check the energy apps on his devices (Emporia, Franklin,
   Home Assistant integrations, Tuya/Smart Life, solar/battery apps) for one with auto-updating PR tariffs.
3. If a usable, legitimate source exists → reuse/wrap it. Don't rebuild.
4. Only if nothing exists → build the digitizer from scratch (scope below).

**The gift to Puerto Ricans** may simply be DISTRIBUTION: publishing where to access the endpoint in the media
and channels people in Puerto Rico actually use (local press, PR Facebook groups, PR solar/energy communities,
HA/Emporia/Franklin/Tuya forums), with copy-paste setup guides per platform.

## Owner intent (Juan, 2026-10-18)
Every electric utility elsewhere has providers/third parties exposing a registry, an API and even MCPs with the
current price of electricity. Puerto Rico (LUMA / PREPA / NEPR) appears to have nothing public.

Goal: a **legitimate, public, real-time (to-the-minute) data source for the price of electricity in Puerto Rico**,
for the community. Any energy/automation platform that accepts a rate endpoint must be able to consume it:
Home Assistant, Emporia, Franklin, Tuya, and **all** others.

Pain today: rates change quarterly (fuel adjustment, purchased power, riders). Users must manually re-enter
them in ~4 apps every 3 months; people forget, and every energy number drifts out of orbit.

## Scope
1. **Research** (Rule Zero) → `docs/research.md` + dead-ends registry.
2. **If no digital source exists**: build the digitizer — ingest official published sources (NEPR resolutions,
   LUMA tariff PDFs, quarterly factor announcements), parse, version, publish.
3. **Model** the full PR residential (and commercial) tariff: fixed charge, energy charge, FCA (fuel),
   PPCA (purchased power), CILT, subsidies, riders, net-metering — effective dates and history.
4. **Deliver**:
   - Public REST/JSON endpoint: current price per kWh + breakdown + effective period + history.
   - MCP server exposing the same.
   - Integrations/docs: Home Assistant (OpenEI-compatible if possible), Emporia, Franklin, Tuya, generic format.
   - Automated update pipeline + alerting when a new quarterly factor is published.
5. **Distribute**: get the endpoint known in Puerto Rico's media and communities.
6. Use full GitHub features: Issues, Projects, Wiki, PRs, Releases.

## Constraints
- Owner prefers execution over questions; do not hand him work that can be deduced or automated.
- Data must be legitimate, sourced and citable (link every value to its official source).

## Related context
- Juan is in San Juan, PR (LUMA customer); uses Emporia + Franklin + Home Assistant.
- The GitHub connector from claude.ai cannot create repos/issues (403, known bug anthropics/claude-ai-mcp#822,
  anthropics/claude-code#88713) — hence this repurpose and EPIC.md instead of an issue.
