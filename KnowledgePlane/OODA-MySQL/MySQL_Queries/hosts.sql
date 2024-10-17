CREATE TABLE hosts (
    id VARCHAR(50) NOT NULL,                 -- '32:08:01:CC:BB:1B/None' (ID includes both MAC and None, so set a larger VARCHAR size)
    mac VARCHAR(50) NOT NULL,                -- '32:08:01:CC:BB:1B' (MAC address)
    vlan VARCHAR(10) NOT NULL,               -- 'None' (could be a string or a number, keeping it VARCHAR)
    innerVlan VARCHAR(10) NOT NULL,          -- 'None'
    outerTpid VARCHAR(10) NOT NULL,          -- 'None'
    configured VARCHAR(10) NOT NULL,         -- 'unknown' (could be a state indicator)
    ipAddresses JSON NOT NULL,               -- ['10.0.1.79'] (Array of IP addresses, using JSON)
    locations JSON NOT NULL,                 -- [{'elementId': 'of:000000000000001e', 'port': '3'}] (JSON data structure)
    PRIMARY KEY (id)                         -- Assuming 'id' is unique and should be the primary key
);
