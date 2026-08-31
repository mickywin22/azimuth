---
type: "L1-source"
source: "US EPA RadNet + Safecast (ambient radiation measurements)"
source_key: "radiation-observations"
endpoint: "/api/radiation/v1/list-radiation-observations"
retrieved: "2026-08-31T13:36:36Z"
license: "US-Gov-public-domain"
attribution: "Data: US EPA RadNet (public domain) + Safecast (CC0) via WorldMonitor (api.worldmonitor.app)"
---

# US EPA RadNet + Safecast (ambient radiation measurements)

> L1 source pull — `radiation-observations` from `/api/radiation/v1/list-radiation-observations` at 2026-08-31T13:36:36Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| observations | [{"baselineValue": 27, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:WA:SEATTLE:1788180840000", "location": {"latitude": 47.6062, "longitude": -122.3321}, "locationName": "Seattle", "observedAt": 1788180840000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 27, "zScore": -0.01}, {"baselineValue": 44.7, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0.3, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:NY:ALBANY:1788180480000", "location": {"latitude": 42.6526, "longitude": -73.7562}, "locationName": "Albany", "observedAt": 1788180480000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 45, "zScore": 0.04}, {"baselineValue": 27.7, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -0.7, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:HI:HONOLULU:1788179640000", "location": {"latitude": 21.3099, "longitude": -157.8581}, "locationName": "Honolulu", "observedAt": 1788179640000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 27, "zScore": -0.78}, {"baselineValue": 39.5, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 2.5, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:IL:CHICAGO:1788177420000", "location": {"latitude": 41.8781, "longitude": -87.6298}, "locationName": "Chicago", "observedAt": 1788177420000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 42, "zScore": 0.68}, {"baselineValue": 28.9, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 2.1, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:DC:WASHINGTON:1788177300000", "location": {"latitude": 38.9072, "longitude": -77.0369}, "locationName": "Washington, DC", "observedAt": 1788177300000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 31, "zScore": 1.31}, {"baselineValue": 67.9, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -0.9, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:MA:BOSTON:1788177060000", "location": {"latitude": 42.3601, "longitude": -71.0589}, "locationName": "Boston", "observedAt": 1788177060000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 67, "zScore": -0.58}, {"baselineValue": 68.6, "confidence": "RADIATION_CONFIDENCE_LOW", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_SAFECAST"], "convertedFromCpm": true, "corroborated": false, "country": "Japan", "delta": 5.7, "freshness": "RADIATION_FRESHNESS_HISTORICAL", "id": "safecast:jp-fukushima:276622389", "location": {"latitude": 37.760893333333335, "longitude": 140.47587666666666}, "locationName": "Fukushima", "observedAt": 1769484538000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_SAFECAST", "sourceCount": 1, "unit": "nSv/h", "value": 74.3, "zScore": 0}] |
| fetchedAt | 1788183071788 |
| epaCount | 6 |
| safecastCount | 1 |
| anomalyCount | 0 |
| elevatedCount | 0 |
| spikeCount | 0 |
| corroboratedCount | 0 |
| lowConfidenceCount | 1 |
| conflictingCount | 0 |
| convertedFromCpmCount | 1 |
| dataAvailable | true |
