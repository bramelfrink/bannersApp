create schema banners;

create table banners.clicks (
    click_id int4,
    banner_id int4,
    campaign_id int4,
    t int2
);

create table banners.impressions (
    banner_id int4,
    campaign_id int4,
    t int2
);

create table banners.conversions (
    conversion_id int4,
    click_id int4,
    revenue float4,
    t int2
);

create table banners.banner_performance (
    campaign_id int4,
    banner_id int4,
    total_revenue float4,
    total_clicks float4,
    total_impressions float4,
    t int2
);