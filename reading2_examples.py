# libraries
# %%
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats
# %%
base_url = "https://github.com/byuidatascience/data4python4ds/raw/master/data-raw/"
table1 = pd.read_csv("{}table1/table1.csv".format(base_url))

# %%
# Compute rate per 10,000
table1.assign(
    rate = lambda x: x.cases / x.population * 1000
)
# Compute cases per year
#>        country  year   cases  population      rate
#> 0  Afghanistan  1999     745    19987071  0.037274
#> 1  Afghanistan  2000    2666    20595360  0.129447
#> 2       Brazil  1999   37737   172006362  0.219393
#> 3       Brazil  2000   80488   174504898  0.461236
#> 4        China  1999  212258  1272915272  0.166750
#> 5        China  2000  213766  1280428583  0.166949
(table1.
  groupby('year').
  agg(n = ('cases', 'sum')).
  reset_index())

# Visualise changes over time
# import altair as alt
#>    year       n
#> 0  1999  250740
#> 1  2000  296920
base_chart = (alt.Chart(table1).
  encode(alt.X('year'), alt.Y('cases'), detail = 'country'))

chart = base_chart.mark_line() + base_chart.encode(color = 'country').mark_circle()
chart
# %%
flights2_url = "https://github.com/byuidatascience/data4python4ds/raw/master/data-raw/flights/flights.csv"

flights2 = pd.read_csv(flights2_url)
flights2['time_hour'] = pd.to_datetime(flights2.time_hour, format = "%Y-%m-%d %H:%M:%S")
# %%
flights2.dtypes
# %%

flights2_sml = (flights2
    .filter(regex = "^year$|^month$|^day$|delay$|^distance$|^air_time$"))

(flights2_sml
  .assign(
    gain = lambda x: x.dep_delay - x.arr_delay,
    speed = lambda x: x.distance / x.air_time * 60
    )
  .head())
#>    year  month  day  dep_delay  arr_delay  air_time  distance  gain       speed
#> 0  2013      1    1        2.0       11.0     227.0      1400  -9.0  370.044053
#> 1  2013      1    1        4.0       20.0     227.0      1416 -16.0  374.273128
#> 2  2013      1    1        2.0       33.0     160.0      1089 -31.0  408.375000
#> 3  2013      1    1       -1.0      -18.0     183.0      1576  17.0  516.721311
#> 4  2013      1    1       -6.0      -25.0     116.0       762  19.0  394.137931
# %%
(flights2_sml
  .assign(
    gain = lambda x: x.dep_delay - x.arr_delay,
    hours = lambda x: x.air_time / 60,
    gain_per_hour = lambda x: x.gain / x.hours
    )
  .head())
#>    year  month  day  dep_delay  ...  distance  gain     hours  gain_per_hour
#> 0  2013      1    1        2.0  ...      1400  -9.0  3.783333      -2.378855
#> 1  2013      1    1        4.0  ...      1416 -16.0  3.783333      -4.229075
#> 2  2013      1    1        2.0  ...      1089 -31.0  2.666667     -11.625000
#> 3  2013      1    1       -1.0  ...      1576  17.0  3.050000       5.573770
#> 4  2013      1    1       -6.0  ...       762  19.0  1.933333       9.827586
#> 
#> [5 rows x 10 columns]

# %%
by_dest = flights2.groupby('dest')

delay = by_dest.agg(
    count = ('distance', 'size'),
    dist = ('distance', np.mean),
    delay = ('arr_delay', np.mean)
    )

delay_filter = delay.query('count > 20 & dest != "HNL"')

# It looks like delays increase with distance up to ~750 miles
# and then decrease. Maybe as flights get longer there's more
# ability to make up delays in the air?
chart_base = (alt.Chart(delay_filter)
  .encode(
    x = 'dist',
    y = 'delay'
    ))
  
chart = chart_base.mark_point() + chart_base.transform_loess('dist', 'delay').mark_line()  
# chart.save("screenshots/transform_1.png")
# %%
chart
# %%
