CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,

    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),

    total_amount NUMERIC(14, 2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_sales_region
        FOREIGN KEY (region_id)
        REFERENCES regions(region_id)
);

CREATE INDEX IF NOT EXISTS idx_sales_date
    ON sales(sale_date);

CREATE INDEX IF NOT EXISTS idx_sales_product
    ON sales(product_id);

CREATE INDEX IF NOT EXISTS idx_sales_region
    ON sales(region_id);