---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-09-05T10:29:43Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-09-05T10:29:43Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "TH", "firstSeenAt": 1788595483949, "id": "abuseipdb:125.25.205.75", "indicator": "125.25.205.75", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1788592622000, "location": {"latitude": 15.777485313191425, "longitude": 101.69497215228503}, "malwareFamily": "", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_ABUSEIPDB", "tags": ["score:100"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 1085} |
