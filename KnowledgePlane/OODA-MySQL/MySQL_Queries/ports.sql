CREATE TABLE ports (
    port_identifier VARCHAR(100) NOT NULL,   -- Unique identifier combining device name and port number
    device_name VARCHAR(50) NOT NULL,        -- Name of the device
    port_number VARCHAR(10) NOT NULL,        -- Port number on the device
    PRIMARY KEY (port_identifier)            -- Set port_identifier as the primary key
);
