use coffee


// 1)Collection considered: <baristacoffeesalesTBL> 
// How many product categories are there? 
// For each product category, show the number of records.
db.baristacoffeesalestbl.find()

db.baristacoffeesalestbl.aggregate(
[
    {
        $group:{
            _id:"$product_category",records:{$sum:1}
        }
    }
    ]
    )
// 2)Collectionconsidered: <caffeine_intake_tracker>
// What is the average caffeine per beverage type (coffee/tea/energy drink)?
// Hint: $switch
db.caffeine_intake_tracker.find()
db.caffeine_intake_tracker.aggregate(
[
    {
            $project:{
                beverage:{
                    $switch: {
                    branches: [
                    {case:{$eq:["$beverage_coffee","True"]}, then: "coffee" }, 
                    {case:{$eq:["$beverage_energy_drink","True"]}, then: "energy_drink" },
                    {case:{$eq:["$beverage_tea","True"]}, then: "tea" },
                    ],
                    default: "none"
                }
            },
            caffeine_mg:1
        }
    },
    {
        $match:{}
    },
    {
        $group:{_id:"$beverage",avg_caffeine:{$avg:"$caffeine_mg"},count: { $sum: 1 }}
    },
    {$sort:{avg_caffeine:-1}}
]
    )


// 3)Collection considered: <caffeine_intake_tracker> 
// How does sleep impact rate vary by time of day (morning/afternoon/evening)?
// Hint: $switch
db.caffeine_intake_tracker.aggregate(
[
    {
            $project:{
                time_of_day:{
                    $switch: {
                    branches: [
                    {case:{$eq:["$time_of_day_morning","True"]}, then: "morning" }, 
                    {case:{$eq:["$time_of_day_afternoon","True"]}, then: "afternoon" },
                    {case:{$eq:["$time_of_day_evening","True"]}, then: "evening" },
                    ],
                    default: "none"
                }
            },
            sleep_impacted:1
        }
    },
    {
        $match:{}
    },
    {
        $group:{_id:"$time_of_day",impacted_rate:{$avg:{$toDouble:"$sleep_impacted"}},n: { $sum: 1 }}
    },
    {$sort:{impacted_rate:-1}}
]
    )
    
// 4)Collection considered: <caffeine_intake_tracker> 
// Bucket caffeine into Low/Med/High and compare average sleep quality
// Hint: $bucket, $addFields, $switch
db.caffeine_intake_tracker.find()
db.caffeine_intake_tracker.aggregate(
[
{
    $bucket: {
          groupBy: "$caffeine_mg",
          boundaries: [ 0, 0.25,0.5,1.01],
          default: "unknown",
          output: {
            "n": { $sum: 1 },
            "avg_sleep_quality" : { $avg: "$sleep_quality" },
            "avg_focus" : { $avg: "$focus_level" }
          }
        }
    
},
{
    $addFields: {
        caffeine_band:{
            $switch: {
              branches: [
                 { case:{$eq:["$_id",0]}, then: "Low" },
                 { case:{$eq:["$_id",0.25]}, then: "Med" },
                 { case:{$eq:["$_id",0.5]}, then: "High" }
              ],
              default: "unknown"
            }
        }
    }
},
    {$project:{_id:0}},
    {$sort:{caffeine_band:1}}
    
 ]
    )


// 5)Collection considered: <coffeesales> 
// What is the total revenue and order count?
// Hint: $addFields
db.coffeesales.find()
db.coffeesales.aggregate(
[{
    $addFields: {
        money_num:{$toDouble: "$money"}
    }
},
    {
        $group:{_id:null,order:{$sum:1},revenue:{$sum:"$money_num"}
    }
 },
 {$project:{_id:0}}
        ]
    )

// 6)Collection considered: <coffeesales>
// Which drink is most cash-heavy? (cash share by drink)

db.coffeesales.aggregate (
[{
    $addFields: {
        is_cash: {$eq: ["$cash_type","cash"]},money_num:{$toDouble: "$money"}
    }
},
    {$group: {
        _id: "$coffee_name",
        cash_orders:{$sum:{$cond:["$is_cash",1,0]}},
        total_orders:{$sum:1},
        cash_rev:{$sum:{$cond:["$is_cash","$money_num",0]}},
        total_rev:{$sum:"$money_num"}
    }},
    {$project:{
        coffee_name:"$_id",
        cash_order_share:{$cond:[{$gt: ["$total_orders",0]},{$divide: ["$cash_orders","$total_orders"]},null]},
        cash_revenue_share:{$cond:[{$gt: ["$total_rev",0]},{$divide: ["$cash_rev","$total_rev"]},null]},
        _id:0
    }},
    {$sort:{cash_revenue_share:-1}}
])
 