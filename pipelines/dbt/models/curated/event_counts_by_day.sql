select
    event_date,
    event_name,
    count(*) as event_count,
    count(distinct user_id) as unique_users
from {{ ref('events') }}
group by 1, 2

