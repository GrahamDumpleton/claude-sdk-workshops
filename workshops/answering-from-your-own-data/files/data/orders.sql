-- The orders taken by Tidewater Books in September 2026.

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    tide_card INTEGER NOT NULL  -- 1 for a member of the loyalty scheme, 0 otherwise
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    title TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price_cents INTEGER NOT NULL,  -- the price of one copy, in cents
    ordered_on TEXT NOT NULL       -- the date, as YYYY-MM-DD
);

INSERT INTO customers (customer_id, name, tide_card) VALUES
    (1, 'Ottoline Marsh', 1),
    (2, 'Barnaby Quill', 0),
    (3, 'Persis Thackeray', 1),
    (4, 'Ignatius Pell', 0),
    (5, 'Dorothea Finch', 1);

INSERT INTO orders (order_id, customer_id, title, quantity, price_cents, ordered_on) VALUES
    (1041, 1, 'The Ferry Almanac', 2, 1099, '2026-09-02'),
    (1042, 2, 'A Field Guide to Knots', 1, 1450, '2026-09-03'),
    (1043, 3, 'Tidewater', 1, 1875, '2026-09-05'),
    (1044, 1, 'A Field Guide to Knots', 4, 1450, '2026-09-08'),
    (1045, 4, 'The Ferry Almanac', 1, 1099, '2026-09-09'),
    (1046, 5, 'Tidewater', 3, 1875, '2026-09-11'),
    (1047, 2, 'The Ferry Almanac', 1, 1099, '2026-09-12'),
    (1048, 1, 'Tidewater', 5, 1875, '2026-09-15'),
    (1049, 3, 'The Ferry Almanac', 2, 1099, '2026-09-19'),
    (1050, 5, 'A Field Guide to Knots', 1, 1450, '2026-09-22'),
    (1051, 4, 'Tidewater', 1, 1875, '2026-09-26'),
    (1052, 3, 'A Field Guide to Knots', 2, 1450, '2026-09-29');
