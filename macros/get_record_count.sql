{%  macro create_unique_id(model, column_name) %}

with record_count as (
    select
    count(1) as total_record_count,
    from {{ model }}
),


select
total_record_count + 10000 as total_record_count
from record_count

{% endmacro %}