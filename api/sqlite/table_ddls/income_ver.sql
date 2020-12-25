-- income table
CREATE TABLE IF NOT EXISTS budget_ver (
	income_id integer PRIMARY KEY,
	income_source text,
	income_category text,
	paycheck_dt text,
	paycheck_amount integer
);