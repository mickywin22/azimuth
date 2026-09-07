---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-09-07T12:21:33Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-09-07T12:21:33Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "BD", "firstSeenAt": 1788775284000, "id": "urlhaus:ip:103.156.176.162", "indicator": "103.156.176.162", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1788782538000, "location": {"latitude": 22.3384, "longitude": 91.8317}, "malwareFamily": "malware_download", "severity": "CRITICALITY_LEVEL_HIGH", "source": "CYBER_THREAT_SOURCE_URLHAUS", "tags": ["32-bit", "arm", "elf", "mozi"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 484} |
