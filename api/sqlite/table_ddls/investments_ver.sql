-- investments_ver table
CREATE TABLE IF NOT EXISTS investments_ver (
	investment_id integer PRIMARY KEY,
	-- Name of the stock owned (apple, tesla, etc)
	investment_name text,
	-- Number of shares owned
	number_of_shares_owned integer,
	-- Where is this investment managed (Robinhood, Vanguard, Fidelity, etc.)
	account_name text,
	-- as of date for when the info was entered
	as_of_dt text,
	-- what industry is the stock in (tech, medical, construction, airline, etc.)
    investment_industry,
    -- overall percentage of portfolio percentage
    portfolio_diversity_percentage,
    -- overall market value of stocks owned (# of stocks * stock price)
    market_value,
    -- the average cost the stock has cost me (what did I buy the stock at, but could change overtime if I buy at different price's hence the "average")
    average_cost_of_stock
);