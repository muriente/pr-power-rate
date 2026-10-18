# EPIC: Public real-time Puerto Rico electricity rate API + MCP (pr-power-rate)

> Could not be created as a GitHub Issue from claude.ai (connector form: "failed to load this connector").
> FIRST TASK for the agent: convert this file into Issue #1 (epic) + sub-issues, add to a Project board, then delete this file.

Full brief: [MISSION.md](MISSION.md)

## Checklist
- [ ] Rename repo to `pr-power-rate`; replace README; set up Project board + Wiki
- [ ] Research every existing digital source for PR rates (LUMA, NEPR, OpenEI URDB, Arcadia/Genability, apps) → docs/research.md + dead-ends registry
- [ ] Model full PR tariff (fixed, energy, FCA, PPCA, CILT, subsidies, riders, net metering) with effective dates + history
- [ ] Build digitizer for official published/analog sources if no digital source exists
- [ ] Public REST endpoint (current price + breakdown + history)
- [ ] MCP server
- [ ] Integrations: Home Assistant, Emporia, Franklin, Tuya + generic format for any platform
- [ ] Automated update pipeline + alert on new quarterly factors
- [ ] Every value cited to official source

Delegated by Juan on 2026-10-18 for a Claude Code session (latest model). Execute end-to-end: find the problem AND ship the solution.
