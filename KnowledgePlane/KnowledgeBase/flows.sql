CREATE TABLE flows (
    id VARCHAR(100) PRIMARY KEY,    -- Unique ID for each flow
    tableId VARCHAR(45),            -- Table identifier
    appId VARCHAR(100),             -- Application ID
    groupId VARCHAR(45),            -- Group ID
    priority INT,                   -- Flow priority
    timeout VARCHAR(45),            -- Flow timeout value
    isPermanent VARCHAR(45),        -- Whether the flow is permanent
    deviceId VARCHAR(45),           -- Device identifier
    state VARCHAR(45),              -- State of the flow (e.g., ACTIVE, INACTIVE)
    life VARCHAR(45),               -- Flow life (e.g., time the flow has been active)
    packets VARCHAR(45),            -- Number of packets processed by the flow
    bytes VARCHAR(45),              -- Number of bytes processed by the flow
    liveType VARCHAR(45),           -- Type of flow (e.g., LIVE, STALE)
    lastSeen VARCHAR(45),           -- Timestamp of the last time the flow was seen
    treatment VARCHAR(200),         -- Treatment actions for the flow (e.g., OUTPUT actions)
    selector VARCHAR(200)           -- Match criteria for the flow
);
