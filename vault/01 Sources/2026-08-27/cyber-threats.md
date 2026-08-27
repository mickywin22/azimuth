---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-08-27T17:35:31Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-08-27T17:35:31Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "CN", "firstSeenAt": 1787846011000, "id": "urlhaus:ip:42.235.90.191", "indicator": "42.235.90.191", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1787846011000, "location": {"latitude": 34.7578, "longitude": 113.6486}, "malwareFamily": "malware_download", "severity": "CRITICALITY_LEVEL_HIGH", "source": "CYBER_THREAT_SOURCE_URLHAUS", "tags": ["32-bit", "elf", "mips", "mozi"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 490} |
