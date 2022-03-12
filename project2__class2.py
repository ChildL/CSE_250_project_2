# %%
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats


# %%
flights = pd.read_json("https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json")
# %%
flights.head()
# %%
flights.describe()
# %%
flights.value_counts()
# %%
flights.shape
# %%
# this is where the code needs to be copied above
flights.num_of_delays_late_aircraft.describe()


# %%
# fixing data
# finding mean of data without the -999 in minutes late
# also replacing -999 with NaN
ndmeans = (flights.num_of_delays_late_aircraft
    .replace(-999, np.NaN).mean())

ndmeans   
# %%
flights.head() 
# %%
# taking the mean value found and replacing the -999 value with
# NaN and then filling in the mean and storing it in new data datac
# clean data
datac = flights.assign(
    num_of_dalays_late_aircraft = lambda x:x.
    num_of_delays_late_aircraft.replace(-999, np.NaN).fillna(ndmeans))  

datac
# %%
# grand 1, groupby airport code, agg total flights for 
# each airport, sum of num of delays total, percent
# .assign 

