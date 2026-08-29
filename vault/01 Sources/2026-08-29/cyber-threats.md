---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-08-29T12:38:37Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-08-29T12:38:37Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "US", "firstSeenAt": 1787990501065, "id": "abuseipdb:66.132.186.217", "indicator": "66.132.186.217", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1787995030000, "location": {"latitude": 40.01907377737087, "longitude": -99.1533073929961}, "malwareFamily": "", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_ABUSEIPDB", "tags": ["score:100"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 804} |
