-- transactions table
CREATE TABLE IF NOT EXISTS mint_transactions_ver (
	transaction_id integer PRIMARY KEY,
	-- date of transaction
	transaction_date text,
	-- long description of transaction
	description text,
	-- original description of transaction
	original_description text,
	-- transaction amount
	amount numeric,
	-- type of transaction (debit or credit)
	transaction_type text,
	-- transaction category (grocceries, restaurant, clothes, etc.)
	category text,
	-- to what bank account the transaction was debited/credited
	account_name,
);