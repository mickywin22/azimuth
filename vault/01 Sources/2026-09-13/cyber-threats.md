---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-09-13T11:43:32Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-09-13T11:43:32Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "US", "firstSeenAt": 1789286610550, "id": "abuseipdb:40.117.97.0", "indicator": "40.117.97.0", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1789283821000, "location": {"latitude": 40.43222705424582, "longitude": -99.48235294117646}, "malwareFamily": "", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_ABUSEIPDB", "tags": ["score:100"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 892} |
