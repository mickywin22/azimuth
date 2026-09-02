---
type: "L1-source"
source: "US EPA RadNet + Safecast (ambient radiation measurements)"
source_key: "radiation-observations"
endpoint: "/api/radiation/v1/list-radiation-observations"
retrieved: "2026-09-02T11:11:18Z"
license: "US-Gov-public-domain"
attribution: "Data: US EPA RadNet (public domain) + Safecast (CC0) via WorldMonitor (api.worldmonitor.app)"
---

# US EPA RadNet + Safecast (ambient radiation measurements)

> L1 source pull — `radiation-observations` from `/api/radiation/v1/list-radiation-observations` at 2026-09-02T11:11:18Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| observations | [{"baselineValue": 29.5, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0.5, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:DC:WASHINGTON:1788342540000", "location": {"latitude": 38.9072, "longitude": -77.0369}, "locationName": "Washington, DC", "observedAt": 1788342540000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 30, "zScore": 0.2}, {"baselineValue": 39.8, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -0.8, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:TX:HOUSTON:1788341340000", "location": {"latitude": 29.7604, "longitude": -95.3698}, "locationName": "Houston", "observedAt": 1788341340000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 39, "zScore": -0.54}, {"baselineValue": 45.2, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -1.2, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:NY:ALBANY:1788341100000", "location": {"latitude": 42.6526, "longitude": -73.7562}, "locationName": "Albany", "observedAt": 1788341100000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 44, "zScore": -0.16}, {"baselineValue": 42.1, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0.9, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:PA:PHILADELPHIA:1788339900000", "location": {"latitude": 39.9526, "longitude": -75.1652}, "locationName": "Philadelphia", "observedAt": 1788339900000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 43, "zScore": 0.32}, {"baselineValue": 68, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -2, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:MA:BOSTON:1788339840000", "location": {"latitude": 42.3601, "longitude": -71.0589}, "locationName": "Boston", "observedAt": 1788339840000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 66, "zScore": -0.94}, {"baselineValue": 27.6, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -0.6, "freshness": "RADIATION_FRESHNESS_RECENT", "id": "epa:HI:HONOLULU:1788287700000", "location": {"latitude": 21.3099, "longitude": -157.8581}, "locationName": "Honolulu", "observedAt": 1788287700000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 27, "zScore": -0.77}, {"baselineValue": 68.6, "confidence": "RADIATION_CONFIDENCE_LOW", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_SAFECAST"], "convertedFromCpm": true, "corroborated": false, "country": "Japan", "delta": 5.7, "freshness": "RADIATION_FRESHNESS_HISTORICAL", "id": "safecast:jp-fukushima:276622389", "location": {"latitude": 37.760893333333335, "longitude": 140.47587666666666}, "locationName": "Fukushima", "observedAt": 1769484538000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_SAFECAST", "sourceCount": 1, "unit": "nSv/h", "value": 74.3, "zScore": 0}] |
| fetchedAt | 1788346837177 |
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
