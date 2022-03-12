# Project_2 flights and delays

# %%
# internal packages
# from logging import PercentStyle
# from pandas.core import indexing
import urllib3
import  json

# libraries to load 
import pandas as pd
import altair as alt
import numpy as np
# from scipy import stats

# %%
# libraries for saving and markdown and altair charts
from vega_datasets import data
from altair_saver import save
# %%
# reading data
flights = pd.read_json("https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json")
# %%
# long way for future data
url_flights = 'https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json'
http = urllib3.PoolManager()
response = http.request('GET', url_flights)
flights_json = json.loads(response.data.decode('utf-8'))
flights = pd.json_normalize(flights_json)
# %%
flights.head()
# %%
# fixing data
# finding mean of data without the -999 in minutes late
# also replacing -999 with NaN
ndmeans = (flights.num_of_delays_late_aircraft
    .replace(-999, np.NaN).mean())

# %%
# datac is clean data with -999 values replaced with mean
datac = flights.assign(
    num_of_delays_late_aircraft 
    = lambda x: 
    x.num_of_delays_late_aircraft.replace(-999, np.NaN).fillna(ndmeans)
)
datac
# %%
# Grand Question 1, groupby airport code, agg total flights for 
# each airport, sum of num of delays total, percent, mean of minutes delayed
# .assign new columns for proportion and avg
df1 = datac.groupby('airport_code').agg({'num_of_flights_total': 
'sum', 'num_of_delays_total': 'sum', 'minutes_delayed_total': 'mean'}).assign(
    proportion_delayed_flights = lambda x: x.num_of_delays_total / x.num_of_flights_total *100,
    avg_hours_delayed_total = lambda x: x.minutes_delayed_total /60
    )

# should be newdf1 = flights.groupby('airport_code').agg(
# sum_of_flights = ('num_of_flights_total',sum),
# sum_of_delays = ('num_of_delays_total', sum'),
# sum_of_delay_min = ('minutes_delayed_total', sum)
# ).assign(percent_delays = lambda x: x.sum_of_delays/ x. sum_of_flights,
# avg_delay_hours = lambda x: x.sum_of_delay_min/ sum_of_delays/ 60)
  
# newdf1.drop ('minutes_delayed_total', axis = 1, inplace=True) 
# newdf1
# %%
df1.drop('minutes_delayed_total', axis=1, inplace=True)
df1
# %%
p2_g1_rank = df1.rank(0)
# %%
# table with num flights, num delays, proportion delayed and avg hrs
p2_g1_table = df1
# %%
# formats tables nicely for terminal, but not for markdown.
p2_g1_rank.style
p2_g1_table.style
# %%
print(p2_g1_table.to_markdown())
# %%
print(p2_g1_rank.to_markdown())
# %%
# Grand Question 2
# best month to fly to avoid any minutes delayed, remove months with na
df2 = datac.assign(
month = lambda x: x.month.replace('n/a', np.NaN))
# %%
df2_mo = df2.dropna(subset = ['month'])

# %%
# clean data frame without months with na, without -999
df3 = df2_mo.assign(
    proportion_delayed_flights = df2_mo.num_of_delays_total/df2_mo.num_of_flights_total,
)
# %%
df4 = df3.groupby('month').proportion_delayed_flights.mean().reset_index()
df5 = df4.replace('Febuary', 'February')

dictmonth = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# %%
bars = alt.Chart(df5, title = 'Proportion of Delayed Flights by Month', width = 400).mark_bar().encode(
    color = alt.Color('month',sort=dictmonth),
    x = alt.X('month',sort = dictmonth, title = 'Month'),
    y = alt.Y('proportion_delayed_flights', axis=alt.Axis(format='%'), title= "Proportion Delayed Flights",
    )   
)
# %%
p2_g2_bars = bars
p2_g2_bars
# %%
# line is at the mean of the proportioned delayed flights
g2_line = pd.DataFrame({'proportion_delayed_flights':[.20]})
g2_line = alt.Chart(g2_line).mark_rule(color = "black").encode(
   y = ('proportion_delayed_flights')
#    "mean(proportion_delayed_flights):Q"
  )
p2_g2_bar = p2_g2_bars + g2_line  
# %%
df5.proportion_delayed_flights.mean()

# save bar graph with mean line
p2_g2_bar.save("flights_g2_bars.svg")
# %%
# chart of months and 
df6 = df5.sort_values(by = ['proportion_delayed_flights'])

# %%
df7  = df6.assign(
    percent_mean_delayed = lambda x: x.proportion_delayed_flights * 100
)
# %%
df8 = df7.drop(columns = 'proportion_delayed_flights')
# %%
df8.rank()

print(df8.to_markdown())

# %%
# grand 3/4
# month, airport code, 
# number of delays aircraft, 30%
# nas 40 apr - aug, 65 
# weather 100 %
# severe = weather
weather = flights.assign(
    severe = lambda x: x.num_of_delays_weather,
    # dla_replace is assigned pd NAN, in place of -999 so can replace with mean
    dla_replace = lambda x: x.num_of_delays_late_aircraft.replace(-999, np.NaN),
    # replace NAN with mean
    mild_late = lambda x: x.dla_replace.fillna(x.dla_replace.mean()
    ),
    # NAS 40% & 60% accdg to month
    mild = lambda x: np.where(x.month.isin(['April', 'May', 'June', 'July', 'August']),
    x.num_of_delays_nas * 0.40,
    x.num_of_delays_nas * 0.65
    ),
    # add all the variables of weather
    weather = lambda x: x.severe + x.mild_late + x.mild,
    percent_weather = lambda x: round((x.weather / x.num_of_delays_total * 100),2) 
    ).filter(['airport_code', 'month', 'severe', 'mild', 'mild_late', 'weather', 'num_of_delays_total', 'percent_weather'])
weather['Percent_weather'] = weather.percent_weather.apply(lambda x: str(x) + '%')
# %%
# dropped "percent_weather" and kept reformatted "Percent_weather, captital P - dif. column."
weather_test = weather.drop("percent_weather",1)
# %%
weather.describe()
# %%
print(weather.head(6).to_markdown())

# %%
# Starting grand 4
weather1 = weather.assign(
month = lambda x: x.month.replace('n/a', np.NaN))
# %%
weather2 = weather1.dropna(subset = ['month'])
weather2 = weather2.replace('Febuary', 'February')
weather2
# %%
# to create sort column, could have used datetime and converted format to datetime and sorted on months.
dictmonth = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# chart representing airports and portion of late flights by month.
# %%
flights_g4 = alt.Chart(weather2, title = "Weather Delayed Flights", width = 300).mark_bar().encode(
    alt.Y("percent_weather", title = "Proportion Delayed Flights"), 
    alt.X('airport_code', title= 'Airport Code'),
    color = 'airport_code'
)
flights_g4
# %%
flights_g4.save("flights_g4.svg")
# %%
## Grand Question 5
# gathering information on the dataframe data type.
flights.year.value_counts()
# %%
flights
# %%
flights.info()
# %%
flights.year.isnull()

# %%
# simplest ways to replace the following values with official NaN
flights_clean1 = flights.replace(-999, np.nan, inplace = True)
flights.replace('1500+', 1750, inplace = True)
flights.replace('n/a', np.nan, inplace = True)
flights.replace(" ", np.nan, inplace = True)

# %%
# another way to clean the flights data
flights_clean = flights.replace(-999, np.nan).replace(" ", np.nan).replace('n/a', np.nan).replace('1500+', 1750)
# %%
flights_clean.to_json

# %%
# exporting the flights_clean to json file, printing one record including null.
json_data = flights_clean.to_json(orient = "records")
json_object = json.loads(json_data)
json_formatted_str = json.dumps(json_object, indent = 4)
print(json_formatted_str)

# %%
# 27 added to month, 40 to late_aircraft, 17 minutes delays nas.
flights_clean.isnull().sum()
# %%
