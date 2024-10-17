CREATE TABLE link_port_stats (
    link_stats_id VARCHAR(100) NOT NULL,    -- Unique identifier for each record
    link_id VARCHAR(150) NOT NULL,          -- Reference to the network link
    timestamp TIMESTAMP NOT NULL,           -- Timestamp of the statistics
    PacketsReceived BIGINT NOT NULL,        -- Number of packets received
    PacketsSent BIGINT NOT NULL,            -- Number of packets sent
    BytesReceived BIGINT NOT NULL,          -- Number of bytes received
    BytesSent BIGINT NOT NULL,              -- Number of bytes sent
    PacketsRxDropped BIGINT NOT NULL,       -- Number of dropped packets on receive
    PacketsTxDropped BIGINT NOT NULL,       -- Number of dropped packets on transmit
    PacketsRxErrors BIGINT NOT NULL,        -- Number of receive errors
    PacketsTxErrors BIGINT NOT NULL,        -- Number of transmit errors
    PRIMARY KEY (link_stats_id),            -- Set link_stats_id as the primary key
    FOREIGN KEY (link_id) REFERENCES network_links(link_id)  -- Reference to network_links table
);
