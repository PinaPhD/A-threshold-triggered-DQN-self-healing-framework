CREATE VIEW port_statistics_device_agg AS
SELECT
    device,
    timestamp,
    
    -- Sum of packets and bytes
    SUM(packetsReceived) AS total_packetsReceived,
    SUM(packetsSent) AS total_packetsSent,
    SUM(bytesReceived) AS total_bytesReceived,
    SUM(bytesSent) AS total_bytesSent,
    
    -- Sum of dropped packets
    SUM(packetsRxDropped) AS total_packetsRxDropped,
    SUM(packetsTxDropped) AS total_packetsTxDropped,
    
    -- Sum of errors
    SUM(packetsRxErrors) AS total_packetsRxErrors,
    SUM(packetsTxErrors) AS total_packetsTxErrors

FROM
    port_statistics
GROUP BY
    device, timestamp;

