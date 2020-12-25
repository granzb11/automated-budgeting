-- savings table
CREATE TABLE IF NOT EXISTS savings_ver (
	id integer PRIMARY KEY,
	as_of_dt text,
	category text,
	budget numeric,
	actual numeric,
	starting_balance numeric,
	account_type text,
	account text
);