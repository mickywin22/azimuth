---
type: "L1-source"
source: "US EPA RadNet + Safecast (ambient radiation measurements)"
source_key: "radiation-observations"
endpoint: "/api/radiation/v1/list-radiation-observations"
retrieved: "2026-09-21T12:41:00Z"
license: "US-Gov-public-domain"
attribution: "Data: US EPA RadNet (public domain) + Safecast (CC0) via WorldMonitor (api.worldmonitor.app)"
---

# US EPA RadNet + Safecast (ambient radiation measurements)

> L1 source pull — `radiation-observations` from `/api/radiation/v1/list-radiation-observations` at 2026-09-21T12:41:00Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| observations | [{"baselineValue": 27.3, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0.7, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:WA:SEATTLE:1789990980000", "location": {"latitude": 47.6062, "longitude": -122.3321}, "locationName": "Seattle", "observedAt": 1789990980000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 28, "zScore": 0.73}, {"baselineValue": 68.6, "confidence": "RADIATION_CONFIDENCE_LOW", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_SAFECAST"], "convertedFromCpm": true, "corroborated": false, "country": "Japan", "delta": 5.7, "freshness": "RADIATION_FRESHNESS_HISTORICAL", "id": "safecast:jp-fukushima:276622389", "location": {"latitude": 37.760893333333335, "longitude": 140.47587666666666}, "locationName": "Fukushima", "observedAt": 1769484538000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_SAFECAST", "sourceCount": 1, "unit": "nSv/h", "value": 74.3, "zScore": 0}] |
| fetchedAt | 1789993856441 |
| epaCount | 1 |
| safecastCount | 1 |
| anomalyCount | 0 |
| elevatedCount | 0 |
| spikeCount | 0 |
| corroboratedCount | 0 |
| lowConfidenceCount | 1 |
| conflictingCount | 0 |
| convertedFromCpmCount | 1 |
| dataAvailable | true |
