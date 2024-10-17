CREATE VIEW port_statistics_diff AS
SELECT
    id,
    device,
    port,
    durationSec,
    timestamp,

    -- Packets and Bytes Differences
    packetsReceived,
    packetsReceived - LAG(packetsReceived, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS packetsReceived_diff,

    packetsSent,
    packetsSent - LAG(packetsSent, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS packetsSent_diff,

    bytesReceived,
    bytesReceived - LAG(bytesReceived, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS bytesReceived_diff,

    bytesSent,
    bytesSent - LAG(bytesSent, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS bytesSent_diff,

    -- Dropped Packets Differences
    packetsRxDropped,
    packetsRxDropped - LAG(packetsRxDropped, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS packetsRxDropped_diff,

    packetsTxDropped,
    packetsTxDropped - LAG(packetsTxDropped, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS packetsTxDropped_diff,

    -- Errors Differences
    packetsRxErrors,
    packetsRxErrors - LAG(packetsRxErrors, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS packetsRxErrors_diff,

    packetsTxErrors,
    packetsTxErrors - LAG(packetsTxErrors, 1) OVER (PARTITION BY device, port ORDER BY timestamp) AS packetsTxErrors_diff

FROM
    port_statistics;
