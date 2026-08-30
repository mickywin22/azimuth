---
type: "L1-source"
source: "US EPA RadNet + Safecast (ambient radiation measurements)"
source_key: "radiation-observations"
endpoint: "/api/radiation/v1/list-radiation-observations"
retrieved: "2026-08-30T11:50:08Z"
license: "US-Gov-public-domain"
attribution: "Data: US EPA RadNet (public domain) + Safecast (CC0) via WorldMonitor (api.worldmonitor.app)"
---

# US EPA RadNet + Safecast (ambient radiation measurements)

> L1 source pull — `radiation-observations` from `/api/radiation/v1/list-radiation-observations` at 2026-08-30T11:50:08Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| observations | [{"baselineValue": 27, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -1, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:WA:SEATTLE:1788087120000", "location": {"latitude": 47.6062, "longitude": -122.3321}, "locationName": "Seattle", "observedAt": 1788087120000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 26, "zScore": -1.01}, {"baselineValue": 44.9, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0.1, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:NY:ALBANY:1788086820000", "location": {"latitude": 42.6526, "longitude": -73.7562}, "locationName": "Albany", "observedAt": 1788086820000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 45, "zScore": 0.01}, {"baselineValue": 42, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 1, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:PA:PHILADELPHIA:1788084900000", "location": {"latitude": 39.9526, "longitude": -75.1652}, "locationName": "Philadelphia", "observedAt": 1788084900000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 43, "zScore": 0.46}, {"baselineValue": 38.7, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 3.3, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:IL:CHICAGO:1788083460000", "location": {"latitude": 41.8781, "longitude": -87.6298}, "locationName": "Chicago", "observedAt": 1788083460000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 42, "zScore": 1.2}, {"baselineValue": 68.6, "confidence": "RADIATION_CONFIDENCE_LOW", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_SAFECAST"], "convertedFromCpm": true, "corroborated": false, "country": "Japan", "delta": 5.7, "freshness": "RADIATION_FRESHNESS_HISTORICAL", "id": "safecast:jp-fukushima:276622389", "location": {"latitude": 37.760893333333335, "longitude": 140.47587666666666}, "locationName": "Fukushima", "observedAt": 1769484538000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_SAFECAST", "sourceCount": 1, "unit": "nSv/h", "value": 74.3, "zScore": 0}] |
| fetchedAt | 1788090369384 |
| epaCount | 4 |
| safecastCount | 1 |
| anomalyCount | 0 |
| elevatedCount | 0 |
| spikeCount | 0 |
| corroboratedCount | 0 |
| lowConfidenceCount | 1 |
| conflictingCount | 0 |
| convertedFromCpmCount | 1 |
| dataAvailable | true |
