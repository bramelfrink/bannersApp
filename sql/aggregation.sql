-- Creates the aggregations that are required to show the correct banners.
-- this would run on a schedule.

begin;
delete from banners.banner_performance where t = 3;

insert into banners.banner_performance
with impressions as (
    select campaign_id, banner_id, count(*) as total_impressions
    from banners.impressions
    where t = 3
    group by 1, 2
    order by 3 DESC
), rev_clicks as (
    select campaign_id, banner_id, sum(co.revenue) as total_revenue, count(*) as total_clicks
    from banners.clicks c
        -- Not all banners might have clicks, so use impressions as base
        JOIN banners.conversions co ON c.click_id = co.click_id
    where co.t = 3 and c.t = 3
    group by 1,2
    order by 3 DESC,4 DESC
)
select i.campaign_id, i.banner_id, total_revenue, total_clicks, total_impressions, 3 as t
from impressions i
    left join rev_clicks r on r.campaign_id = i.campaign_id and r.banner_id = i.banner_id;
end;

