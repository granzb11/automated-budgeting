with source_data as (

    select
    generate_uuid() as transaction_id,
    parse_date('%m/%d/%Y', transaction_date) as transaction_date,
    description as description,
    original_description as original_description,
    transaction_amount as transaction_amount,
    transaction_type as transaction_type,
    category as category,
    account_name as account_name,
    format_datetime("%m-%d-%Y %T", current_datetime("America/New_York")) as etl_ts,
    from {{ ref('transactions') }}

)

select
*
from source_data