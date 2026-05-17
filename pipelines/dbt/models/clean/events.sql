with source_events as (
    select
        event_id,
        lower(trim(source)) as source,
        lower(trim(event_name)) as event_name,
        cast(user_id as integer) as user_id,
        cast(occurred_at as timestamp) as occurred_at,
        payload
    from {{ ref('source_events') }}
)

select
    event_id,
    source,
    event_name,
    user_id,
    occurred_at,
    cast(occurred_at as date) as event_date,
    payload
from source_events
where event_id is not null
  and event_name is not null
  and occurred_at is not null

