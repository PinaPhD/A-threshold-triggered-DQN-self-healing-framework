CREATE TABLE network_links (
    link_id VARCHAR(150) NOT NULL,           -- Unique identifier combining source and destination ports
    src_port_identifier VARCHAR(100) NOT NULL,  -- Identifier for the source port (matches ports table)
    dest_port_identifier VARCHAR(100) NOT NULL, -- Identifier for the destination port (matches ports table)
    PRIMARY KEY (link_id),                   -- Set link_id as the primary key
    FOREIGN KEY (src_port_identifier) REFERENCES ports(port_identifier),  -- Reference to ports table
    FOREIGN KEY (dest_port_identifier) REFERENCES ports(port_identifier)  -- Reference to ports table
);
