CREATE TABLE devices (
    id VARCHAR(50) NOT NULL,                         -- 'of:000000000000000c' (device ID, VARCHAR with max length of 50 based on examples)
    type VARCHAR(10) NOT NULL,                       -- 'SWITCH' (VARCHAR, as this is a short string)
    available BOOLEAN NOT NULL,                      -- 'TRUE' (boolean field)
    role VARCHAR(10) NOT NULL,                       -- 'MASTER' (role of the device, short string)
    mfr VARCHAR(50) NOT NULL,                        -- 'Nicira, Inc.' (manufacturer, VARCHAR with sufficient length)
    hw VARCHAR(50) NOT NULL,                         -- 'Open vSwitch' (hardware version)
    sw VARCHAR(10) NOT NULL,                         -- '2.17.9' (software version, VARCHAR for flexibility)
    serial VARCHAR(50) NOT NULL,                     -- 'None' or other serials (could be device serial numbers)
    driver VARCHAR(10) NOT NULL,                     -- 'ovs' (driver identifier)
    chassisId VARCHAR(10) NOT NULL,                  -- 'c' (chassis identifier)
    lastUpdate BIGINT NOT NULL,                      -- '1721490956392' (timestamp in milliseconds, hence BIGINT)
    humanReadableLastUpdate VARCHAR(50) NOT NULL,    -- 'connected 10d20h ago' (human-readable time, VARCHAR)
    annotations TEXT NOT NULL,                       -- JSON-like structure stored in 'annotations' (using TEXT to store)
    PRIMARY KEY (id)                                 -- Assuming 'id' is the primary key
);
