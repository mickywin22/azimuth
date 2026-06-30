---
type: "L1-Source"
resource: "https://api.worldmonitor.app/api/cyber/v1/list-cyber-threats"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-06-27T07:20:54Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-06-27T07:20:54Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "KZ", "firstSeenAt": 1782540104818, "id": "abuseipdb:37.151.58.74", "indicator": "37.151.58.74", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1782537421000, "location": {"latitude": 48.18971541924163, "longitude": 67.28451972228581}, "malwareFamily": "", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_ABUSEIPDB", "tags": ["score:100"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 974} |
