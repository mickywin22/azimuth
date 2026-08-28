---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-08-28T18:36:21Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-08-28T18:36:21Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "CA", "firstSeenAt": 1787939775000, "id": "urlhaus:ip:165.22.225.110", "indicator": "165.22.225.110", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1787939775000, "location": {"latitude": 43.7064, "longitude": -79.3986}, "malwareFamily": "malware_download", "severity": "CRITICALITY_LEVEL_HIGH", "source": "CYBER_THREAT_SOURCE_URLHAUS", "tags": ["165-22-225-110", "exe", "ua-wget"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 474} |
