with source_data as (

    select
    generate_uuid() as savings_id,
    savings_description as savings_description,
    monthly_budget as monthly_budget,
    institution_name as institution_name,
    account_type as account_type,
    account_name as account_name,
    account_number as account_number,
    initial_amount as initial_amount,
    current_amount as current_amount,
    initial_account_creation as initial_account_creation_dt,
    format_datetime("%m-%d-%Y", current_datetime("America/New_York")) as as_of_dt,
    format_datetime("%m-%d-%Y %T", current_datetime("America/New_York")) as etl_ts
    from {{ ref('savings') }}

)

select
*
from source_data