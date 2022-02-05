# %%
import pandas as pd
import altair as alt
import numpy as np

import urllib3
import  json
# %%
url_flights = 'https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json'
http = urllib3.PoolManager()
response = http.request('GET', url_flights)
flights_json = json.loads(response.data.decode('utf-8'))
flights = pd.json_normalize(flights_json)
# %%
flights.info()
# %%
flights.year.isnull()

# %%
clean = flights.assign(
    month = flights.month.replace('n/a', np.NaN), num_delays_late_aircraft = flights.num_delays_late_aircraft.replace('-999', np.Nan),
    num_of_delays_carrier = flights.num_of_delays_carrier.replace("1500+", "1758").astype("float64")

)

# %%

# %%

flights_example = alt.Chart(weather, height=210).mark_rect().encode(
    alt.Y(
        "airport_code",
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