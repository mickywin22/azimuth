---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-08-26T07:04:48Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-08-26T07:04:48Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "NL", "firstSeenAt": 1787722640000, "id": "urlhaus:ip:213.232.114.14", "indicator": "213.232.114.14", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1787722640000, "location": {"latitude": 52.374, "longitude": 4.8897}, "malwareFamily": "malware_download", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_URLHAUS", "tags": ["botnet", "ddos", "elf", "iot", "khserver", "mirai"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 895} |
