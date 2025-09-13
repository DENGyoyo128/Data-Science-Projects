
-- 1、Table considered: <baristacoffeesalesTBL> 
-- How many product categories are there? ->7
select count(distinct(product_category))
from coffee.baristacoffeesalestbl;
-- For each product category, show the number of records.
select
    product_category,
    COUNT(*) as record_count
from coffee.baristacoffeesalestbl
group by product_category;



-- 2、Table considered: <baristacoffeesalesTBL>
-- For each customer_gender and loyalty_member type, 
-- show the number of records. Within the same outcome,
--  within each customer_gender and loyalty_member type,
--  for each is_repeat_customer type, show the number of records.

select T1.customer_gender,T1.loyalty_member,T1.records, T2.is_repeat_customer, T2.records 
from
(
	(
	select concat(customer_gender,loyalty_member,"True") as F1,customer_gender,loyalty_member,count(*) as records
	from baristacoffeesalestbl
	group by customer_gender, loyalty_member
	)
	union
	(
	select concat(customer_gender,loyalty_member,"False") as F1,customer_gender,loyalty_member,count(*) 
	from baristacoffeesalestbl
	group by customer_gender, loyalty_member
	) 
) as T1,
(
	select concat(customer_gender,loyalty_member,is_repeat_customer) as F1,customer_gender,loyalty_member,is_repeat_customer,count(*) as records
	from baristacoffeesalestbl
	group by customer_gender, loyalty_member, is_repeat_customer
) as T2
where T1.F1=T2.F1;

-- 3)Table considered: <baristacoffeesalesTBL> 
-- For each product_category and customer_discovery_source, 
-- display the sum of total_amount.


select product_category,customer_discovery_source,sum(convert(total_amount,decimal))
from baristacoffeesalestbl
group by product_category,customer_discovery_source;

-- 4)Tables considered: <caffeine_intake_tracker> 
-- Consider consuming coffee as the beverage, 
-- for each time_of_day category and gender, 
-- display the average focus_level and average sleep_quality.


(
select "morning" as time_of_day, "female" as gender,avg(convert(focus_level,decimal)),avg(convert(sleep_quality,decimal))
from caffeine_intake_tracker
where time_of_day_morning="True" and gender_female="True" and beverage_coffee="True"
)
union
(
select "afternoon" as time_of_day, "female" as gender,avg(convert(focus_level,decimal)),avg(convert(sleep_quality,decimal))
from caffeine_intake_tracker
where time_of_day_afternoon="True" and gender_female="True" and beverage_coffee="True"
)
union
(
select "morning" as time_of_day, "male" as gender,avg(convert(focus_level,decimal)),avg(convert(sleep_quality,decimal))
from caffeine_intake_tracker
where time_of_day_morning="True" and gender_male="True" and beverage_coffee="True"
)
union
(
select "afternoon" as time_of_day, "male" as gender,avg(convert(focus_level,decimal)),avg(convert(sleep_quality,decimal))
from caffeine_intake_tracker
where time_of_day_afternoon="True" and gender_male="True" and beverage_coffee="True"
)
union
(
select "evening" as time_of_day, "male" as gender,avg(convert(focus_level,decimal)),avg(convert(sleep_quality,decimal))
from caffeine_intake_tracker
where time_of_day_evening="True" and gender_male="True" and beverage_coffee="True"
)
union
(
select "evening" as time_of_day, "female" as gender,avg(convert(focus_level,decimal)),avg(convert(sleep_quality,decimal))
from caffeine_intake_tracker
where time_of_day_evening="True" and gender_female="True" and beverage_coffee="True"
);


-- 5)Tables considered: <list_coffee_shops_in_kota_bogor> 
-- There are problems with the data in this table.
-- List out the problematic records.
select location_name,count(*)
from list_coffee_shops_in_kota_bogor
group by location_name
having count(*)>1;


-- 6)Tables considered: <coffeesales> 
-- List the amount of spending (money) recorded before 12 and after 12.
-- Before 12 is defined as the time between 0 and < 12 hours.
-- After 12 is defined as the time between =12 and <24 hours.

(
	select "Before 12" as period, sum(convert(money,decimal(4,2))) as amt
	from(
	select hour(convert(datetime,time)) as hour, cash_type,card,money,coffee_name
	from coffeesales
	)as T1
	where the_hour>=0 and the_hour<12
)
union
(
	select "After 12" as period, sum(convert(money,decimal(4,2))) as amt
	from(
	select hour(convert(datetime,time)) as hour, cash_type,card,money,coffee_name
	from coffeesales
	)as T1
	where the_hour>=12 and the_hour<24
);


-- 7、For each category of Ph values, 
-- show the average Liking, Flavor.intensity, Acidity, and Mouthfeel. 


(
select "4 to 5" as pH,convert(avg(Liking),decimal(4,2)) as avgLiking,avg(Flavorintensity) as avgflavorintensity,
avg(acidity) as avgacidity,avg(mouthfeel) as avgmouthfeel
from consumerpreference
where pH>=4.0 and pH<5.0
)
union
(
select "5 to 6" as pH,convert(avg(Liking),decimal(4,2)) as avgLiking,avg(Flavor.intensity) as avgflavorintensity,
avg(acidity) as avgacidity,avg(mouthfeel) as avgmouthfeel
from consumerpreference
where pH>=5.0 and pH<6.0
);


-- 8)Tables considered: <coffeesales> + <list_coffee_shops_in_kota_bogor> + <top-rated-coffee> + <baristacoffeesalestbl>
(
	select "MAR",store_id,store_location,location_name,avg(agtron),count(*) as trans_amt,sum(money) as totalmoney
	from coffeesales,list_coffee_shops_in_kota_bogor,`top-rated-coffee`,baristacoffeesalestbl
	where coffeesales.coffeeID =`top-rated-coffee`.ID AND
	coffeesales.shopID=list_coffee_shops_in_kota_bogor.no and
	coffeesales.customer_id=substring(baristacoffeesalestbl.customer_id,6) and
	extract(month from str_to_date(date,'%d%m%y'))=3
	group by store_id,shop_id
	order by sum(money) DESC
	limit 3
)
union 
(
	select "APR",store_id,store_location,location_name,avg(agtron),count(*) as trans_amt,sum(money) as totalmoney
	from coffeesales,list_coffee_shops_in_kota_bogor,`top-rated-coffee`,baristacoffeesalestbl
	where coffeesales.coffeeID =`top-rated-coffee`.ID AND
	coffeesales.shopID=list_coffee_shops_in_kota_bogor.no and
	coffeesales.customer_id=substring(baristacoffeesalestbl.customer_id,6) and
	extract(month from str_to_date(date,'%d%m%y'))=4
	group by store_id,shop_id
	order by sum(money) DESC
	limit 3
)
union
(
	select "MAY",store_id,store_location,location_name,avg(agtron),count(*) as trans_amt,sum(money) as totalmoney
	from coffeesales,list_coffee_shops_in_kota_bogor,`top-rated-coffee`,baristacoffeesalestbl
	where coffeesales.coffeeID =`top-rated-coffee`.ID AND
	coffeesales.shopID=list_coffee_shops_in_kota_bogor.no and
	coffeesales.customer_id=substring(baristacoffeesalestbl.customer_id,6) and
	extract(month from str_to_date(date,'%d%m%y'))=5
	group by store_id,shop_id
	order by sum(money) DESC
	limit 3
)
union
(
	select "JUN",store_id,store_location,location_name,avg(agtron),count(*) as trans_amt,sum(money) as totalmoney
	from coffeesales,list_coffee_shops_in_kota_bogor,`top-rated-coffee`,baristacoffeesalestbl
	where coffeesales.coffeeID =`top-rated-coffee`.ID AND
	coffeesales.shopID=list_coffee_shops_in_kota_bogor.no and
	coffeesales.customer_id=substring(baristacoffeesalestbl.customer_id,6) and
	extract(month from str_to_date(date,'%d%m%y'))=6
	group by store_id,shop_id
	order by sum(money) DESC
	limit 3
)
union
(
	select "JUL",store_id,store_location,location_name,avg(agtron),count(*) as trans_amt,sum(money) as totalmoney
	from coffeesales,list_coffee_shops_in_kota_bogor,`top-rated-coffee`,baristacoffeesalestbl
	where coffeesales.coffeeID =`top-rated-coffee`.ID AND
	coffeesales.shopID=list_coffee_shops_in_kota_bogor.no and
	coffeesales.customer_id=substring(baristacoffeesalestbl.customer_id,6) and
	extract(month from str_to_date(date,'%d%m%y'))=7
	group by store_id,shop_id
	order by sum(money) DESC
	limit 3
);





