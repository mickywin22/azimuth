---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-09-03T11:07:43Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-09-03T11:07:43Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "US", "firstSeenAt": 1788422632676, "id": "abuseipdb:34.42.193.219", "indicator": "34.42.193.219", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1788419822000, "location": {"latitude": 39.20396734569314, "longitude": -98.23791866941329}, "malwareFamily": "", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_ABUSEIPDB", "tags": ["score:100"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 983} |
