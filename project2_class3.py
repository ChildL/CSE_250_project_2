# %%
# internal packages
from logging import PercentStyle
from os import replace
from pandas.core import indexing
import urllib3
import  json

# libraries to load 
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats
# %%
# reading data
flights = pd.read_json("https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json")
# %%
### Day 3

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'] * 4
days.sort()

df=pd.DataFrame({
    'hour': ["9am", "10am", "11am", "12pm"] * 5,
    'dayofweek': days,
    'cnt': [5, 18, 2, 3, 19, 1, 9, 0, 7, 10,
        12, 3, 1, 17, 6, 7, 10, 11, 3, 4]}) 

chartex = alt.Chart(df, height=210).mark_rect().encode(
    alt.Y(
        "hour",
        sort = ["9am", "10am", "11am", "12pm"],
        title="Hour"), 
    alt.X(
        "dayofweek",
        sort=["Mon", "Tue", "Wed", "Thu", "Fri"],
        title="Day of Week"),
        color=alt.Color(
            "cnt", 
            scale=alt.Scale(
                range=['lightyellow','red']), 
        legend=alt.Legend(title='Count')
    ),
    tooltip=[
        alt.Tooltip("cnt", title="Count")
    ]
).properties(width=250)

# %%
chartex
# %%
# grand 3/4
# month, airport code, 
# number of delays aircraft, 30%
# nas 40 apr - aug, 65 
# weather 100 %
# severe = weather
weather = flights.assign(
    severe = lambda x: x.num_of_delays_weather,
    # nodla_nona assigns pd NAN, so can replace with mean
    nodla_nona = lambda x: x.num_of_delays_late_aircraft.replace(-999, np.NaN),
    # replace NAN with mean
    mild_late = lambda x: x.nodla_nona.fillna(x.nodla_nona.mean()
    ),
    # NAS 40% & 60% accdg to month
    mild = lambda x: np.where(x.month.isin(['April', 'May', 'June', 'July', 'August']),
    x.num_of_delays_nas * 0.40,
    x.num_of_delays_nas * 0.65
    ),
    # add all the variables of weather
    weather = lambda x: x.severe + x.mild_late +x.mild,
    percent_weather = lambda x: x.weather / x.num_of_delays_total
    ).filter(['airport_code', 'month', 'severe', 'mild', 'mild_late', 'weather', 'num_of_delays_total', 'percent_weather'])
    
# %%  
weather
# %%
# using cars data

url_cars = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.json"
cars = pd.read_json(url_cars)
# %%
cars.head()
# %%
cars.cyl.value_counts()
# %%
bob = cars.groupby('cyl').agg(avg_hp = ('hp', np.mean)).reset_index()
bob
# %%
alt.Chart(bob).mark_line().encode(
    x = 'cyl', 
    y = alt.Y ('avg_hp', axis = alt.Axis(format = '%')))

# %%
cars.describe()

# %%
cars.isnull().sum()
# %%
cars.head()
# %%
# trying another way to take 999 out and replace with mean
cars3 = cars.assign(
    gear_r = lambda x: x.
    gear.replace(999, np.NaN)),

gear_m = lambda x: x.gear_r.fillna(x.gear_r.mean()
)
cars3.head()
# %%
mean_of_gear = cars.gear.replace(999, np.nan).mean()
# %%
cars2 = cars.copy()

# %%
cars2.gear = cars2.gear.replace(999, mean_of_gear)
cars2

# %%
answer = cars2.assign(
    part1 = cars2.cyl,
    part2 = .60 * cars2.gear,
    part3 = np.where(cars.disp < 200, cars2.carb, 2 * cars2.carb), 
    bob = lambda x: x.part1 + x.part2 + x.part3
)
answer.head()
# %%
print(answer.head().filter(["car", "cyl", "disp", "carb", "part1", "bob"]).to_markdown())
# %%
cars.isnull().sum()
# %%
cars_clean = cars.replace(999, np.nan).replace("", np.nan)
# %%
cars_clean.isnull().sum()
# %%
cars_clean.to_json("my_cars_data.json")
# %%
json_data = cars.to_json(orient="records")
json_object = json.loads(json_data)
json_formatted_str = json.dumps(json_object, indent = 4)
print(json_formatted_str)
# %%
