---
type: "L1-source"
source: "US EPA RadNet + Safecast (ambient radiation measurements)"
source_key: "radiation-observations"
endpoint: "/api/radiation/v1/list-radiation-observations"
retrieved: "2026-09-01T11:33:54Z"
license: "US-Gov-public-domain"
attribution: "Data: US EPA RadNet (public domain) + Safecast (CC0) via WorldMonitor (api.worldmonitor.app)"
---

# US EPA RadNet + Safecast (ambient radiation measurements)

> L1 source pull — `radiation-observations` from `/api/radiation/v1/list-radiation-observations` at 2026-09-01T11:33:54Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| observations | [{"baselineValue": 67.8, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 2.2, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:MA:BOSTON:1788259920000", "location": {"latitude": 42.3601, "longitude": -71.0589}, "locationName": "Boston", "observedAt": 1788259920000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 70, "zScore": 1.44}, {"baselineValue": 29.2, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 0.8, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:DC:WASHINGTON:1788259680000", "location": {"latitude": 38.9072, "longitude": -77.0369}, "locationName": "Washington, DC", "observedAt": 1788259680000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 30, "zScore": 0.32}, {"baselineValue": 29.9, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": 1.1, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:CA:SAN%20FRANCISCO:1788259440000", "location": {"latitude": 37.7749, "longitude": -122.4194}, "locationName": "San Francisco", "observedAt": 1788259440000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 31, "zScore": 0.82}, {"baselineValue": 39.6, "confidence": "RADIATION_CONFIDENCE_MEDIUM", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_EPA_RADNET"], "convertedFromCpm": false, "corroborated": false, "country": "United States", "delta": -0.6, "freshness": "RADIATION_FRESHNESS_LIVE", "id": "epa:TX:HOUSTON:1788257220000", "location": {"latitude": 29.7604, "longitude": -95.3698}, "locationName": "Houston", "observedAt": 1788257220000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_EPA_RADNET", "sourceCount": 1, "unit": "nSv/h", "value": 39, "zScore": -0.43}, {"baselineValue": 68.6, "confidence": "RADIATION_CONFIDENCE_LOW", "conflictingSources": false, "contributingSources": ["RADIATION_SOURCE_SAFECAST"], "convertedFromCpm": true, "corroborated": false, "country": "Japan", "delta": 5.7, "freshness": "RADIATION_FRESHNESS_HISTORICAL", "id": "safecast:jp-fukushima:276622389", "location": {"latitude": 37.760893333333335, "longitude": 140.47587666666666}, "locationName": "Fukushima", "observedAt": 1769484538000, "severity": "RADIATION_SEVERITY_NORMAL", "source": "RADIATION_SOURCE_SAFECAST", "sourceCount": 1, "unit": "nSv/h", "value": 74.3, "zScore": 0}] |
| fetchedAt | 1788262306663 |
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
