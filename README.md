# PKHosting Competitor Pricing Intelligence (TPT-2026-03786)

New project built from scratch on 2026-10-26. Previous repository untouched.

## STATUS (read first)
**Incomplete against the 15-provider requirement: 6 verified (GoDaddy, HostArmada, Namecheap, Hostinger, Hostedium, HostCry).** The validator reports the shortfall honestly. See [research log](data/research_log.csv) for every excluded provider and why. No third-party price is used.

## Files
- [Competitor pricing](data/competitor_pricing.csv) - verified rows only
- [Feature comparison](data/feature_comparison.csv)
- [Source register](data/source_register.csv)
- [PKHosting baseline](data/pkhosting_baseline.csv)
- [Research log](data/research_log.csv)
- [Positioning report](report/competitive_positioning_report.md)
- [Executive summary](report/executive_summary.md)
- [Methodology](report/methodology.md)
- [Validation script](validation/validate.py) and [results](validation/validation_results.txt)
- [Changelog](CHANGELOG.md)

Rebuild data: `python3 build_data.py`; validate: `python3 validation/validate.py`.

## Main findings (verified rows only)
- PKHosting Personal (Rs 699/mo; Rs 6,990 annual) vs HostCry Starter (Rs 1,500 first year, Rs 2,499 renewal) with similar specs; vs Hostedium Budget Rs 799/mo. USD hosts shown separately; no currency conversion.
- Both verified competitors advertise promotional rates that renew far higher; PKHosting shows one recurring rate.
## Limitations
Only 6 of 15 competitors verified; findings are indicative, not a market view.
