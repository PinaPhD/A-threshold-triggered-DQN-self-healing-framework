CREATE TABLE links (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Auto-incrementing primary key
    src_port INT NOT NULL,                    -- Port from src device
    src_device VARCHAR(50) NOT NULL,          -- Source device
    dst_port INT NOT NULL,                    -- Port from dst device
    dst_device VARCHAR(50) NOT NULL,          -- Destination device
    state VARCHAR(20) NOT NULL DEFAULT 'ACTIVE', -- Link state, default is ACTIVE
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the link was recorded
);
