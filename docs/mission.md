# MISSION — PR Power Rate (working name `pr-power-rate`)

> Original mission brief (2026-10-18). The repo was renamed from `pixel9-superdevice-` to `pr-power-rate` on 2026-11-26.

## ⚠️ RULE ZERO — Research before building (owner's explicit instruction)
Do NOT assume this doesn't exist. Juan already uses an app (he doesn't recall which) that receives PR rates
**automatically**. He assumed the vendor keys LUMA's quarterly numbers in manually to cover the gap — but that
means someone may ALREADY have digitized this data.

Order of operations:
1. Find out whether LUMA/NEPR publishes it natively in any machine-readable form.
2. Find who already digitized it (apps, energy-monitor vendors, OpenEI URDB entries, Arcadia/Genability, HA
   community, GitHub). Identify the app Juan uses — check the energy apps on his devices (Emporia, Franklin,
   Home Assistant integrations, Tuya/Smart Life, solar/battery apps) for one with auto-updating PR tariffs.
3. **AUDIT ACCURACY of any source found — existence is not enough.** A source may exist but be a half-done job
   just to say it's available. Juan recalls that when he activated that app, its number did NOT match his own
   research of the PR rates at the time. For every candidate source:
   - Rebuild the expected all-in $/kWh from official documents (LUMA tariff + current NEPR quarterly factors:
     FCA, PPCA, CILT, subsidies, riders) for several past quarters.
   - Compare against what the source reported for those same periods: does it include every component?
     Does it update on the effective date? Does it distinguish rate classes and consumption tiers?
   - Record the verdict per source in `docs/source-audit.md` (accurate / partial / wrong, with evidence).
4. If an accurate, legitimate source exists → reuse/wrap it. If it exists but is inaccurate → our product is
   the CORRECT version (and that comparison is part of the public story).
5. Only if nothing usable exists → build the digitizer from scratch.

**The gift to Puerto Ricans** may simply be DISTRIBUTION: publishing where to access an ACCURATE endpoint in the
media and channels people in Puerto Rico actually use (local press, PR Facebook groups, PR solar/energy
communities, HA/Emporia/Franklin/Tuya forums), with copy-paste setup guides per platform.

## Owner intent (Juan, 2026-10-18)
Every electric utility elsewhere has providers/third parties exposing a registry, an API and even MCPs with the
current price of electricity. Puerto Rico (LUMA / PREPA / NEPR) appears to have nothing public.

Goal: a **legitimate, accurate, public, real-time (to-the-minute) data source for the price of electricity in
Puerto Rico**, for the community. Any energy/automation platform that accepts a rate endpoint must be able to
consume it: Home Assistant, Emporia, Franklin, Tuya, and **all** others.

Pain today: rates change quarterly (fuel adjustment, purchased power, riders). Users must manually re-enter
them in ~4 apps every 3 months; people forget, and every energy number drifts out of orbit.

## Scope
1. **Research + accuracy audit** (Rule Zero) → `docs/research.md`, `docs/source-audit.md`, dead-ends registry.
2. **If no accurate digital source exists**: build the digitizer — ingest official published sources (NEPR
   resolutions, LUMA tariff PDFs, quarterly factor announcements), parse, version, publish.
3. **Model** the full PR residential (and commercial) tariff: fixed charge, energy charge, FCA (fuel),
   PPCA (purchased power), CILT, subsidies, riders, net-metering — effective dates and history.
4. **Deliver**:
   - Public REST/JSON endpoint: current price per kWh + breakdown + effective period + history.
   - MCP server exposing the same.
   - Integrations/docs: Home Assistant (OpenEI-compatible if possible), Emporia, Franklin, Tuya, generic format.
   - Automated update pipeline + alerting when a new quarterly factor is published.
   - Validation: automated checks that published values reconcile with the official documents each quarter.
5. **Distribute**: get the endpoint known in Puerto Rico's media and communities.
6. Use full GitHub features: Issues, Projects, Wiki, PRs, Releases.

## Constraints
- Owner prefers execution over questions; do not hand him work that can be deduced or automated.
- Data must be legitimate, sourced and citable (link every value to its official source).
