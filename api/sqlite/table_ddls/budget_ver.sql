-- budget table
CREATE TABLE IF NOT EXISTS budget_ver (
	budget_id integer PRIMARY KEY,
	budget_category text,
	budget_amount numeric,
	amount_spent numeric,
	difference numeric
);