CREATE VIEW port_statistics_device_diff AS
SELECT
    current.device,
    current.timestamp,
    current.total_packetsReceived - prev.total_packetsReceived AS total_packetsReceived,
    current.total_packetsSent - prev.total_packetsSent AS total_packetsSent,
    current.total_bytesReceived - prev.total_bytesReceived AS total_bytesReceived,
    current.total_bytesSent - prev.total_bytesSent AS total_bytesSent,
    current.total_packetsRxDropped - prev.total_packetsRxDropped AS total_packetsRxDropped,
    current.total_packetsTxDropped - prev.total_packetsTxDropped AS total_packetsTxDropped,
    current.total_packetsRxErrors - prev.total_packetsRxErrors AS total_packetsRxErrors,
    current.total_packetsTxErrors - prev.total_packetsTxErrors AS total_packetsTxErrors
FROM
    port_statistics_device_agg current
JOIN
    port_statistics_device_agg prev
    ON current.device = prev.device
    AND current.timestamp > prev.timestamp
    AND NOT EXISTS (
        SELECT 1 
        FROM port_statistics_device_agg p2
        WHERE p2.device = current.device
        AND p2.timestamp < current.timestamp
        AND p2.timestamp > prev.timestamp
    );
