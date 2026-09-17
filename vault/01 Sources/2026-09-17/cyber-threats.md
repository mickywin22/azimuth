---
type: "L1-source"
source: "abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)"
source_key: "cyber-threats"
endpoint: "/api/cyber/v1/list-cyber-threats"
retrieved: "2026-09-17T11:34:14Z"
license: "CC0-1.0"
attribution: "Data: abuse.ch (URLhaus + Feodo Tracker, CC0) via WorldMonitor (api.worldmonitor.app)"
---

# abuse.ch (URLhaus malware URLs + Feodo Tracker C2 indicators)

> L1 source pull — `cyber-threats` from `/api/cyber/v1/list-cyber-threats` at 2026-09-17T11:34:14Z. Verbatim transform; never edit by hand.

| field | value |
| --- | --- |
| threats | [{"country": "MY", "firstSeenAt": 1789632235960, "id": "abuseipdb:49.124.151.5", "indicator": "49.124.151.5", "indicatorType": "CYBER_THREAT_INDICATOR_TYPE_IP", "lastSeenAt": 1789629422000, "location": {"latitude": 4.420691233691921, "longitude": 101.49284351873045}, "malwareFamily": "", "severity": "CRITICALITY_LEVEL_CRITICAL", "source": "CYBER_THREAT_SOURCE_ABUSEIPDB", "tags": ["score:100"], "type": "CYBER_THREAT_TYPE_MALWARE_HOST"}] |
| pagination | {"nextCursor": "1", "totalCount": 953} |
