CREATE TABLE port_statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- Primary key with auto-increment
    port INT,
    packetsReceived BIGINT,
    packetsSent BIGINT,
    bytesReceived BIGINT,
    bytesSent BIGINT,
    packetsRxDropped BIGINT,
    packetsTxDropped BIGINT,
    packetsRxErrors BIGINT,
    packetsTxErrors BIGINT,
    durationSec BIGINT,
    device VARCHAR(50),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Timestamp column, not null, defaults to current time
);

