# internal packages
# %%
import urllib3
import  json

# %%
# external packages
import pandas as pd
import numpy as np
import altair as alt


# %%
url_cars = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.json"
cars = pd.read_json(url_cars)
# %%
cars.head()
# %%
cars.car.value_counts().sum()
cars.cyl.value_counts()
# %%
cly_4 = cars.query("cyl >= 4").value_counts()
cly_4
# %%
cars.sort_values(by = ['mpg'], ascending = False)
cars1 = cars.query('wt >= 3')
cars1
# %%
cyl_6 = cars.query('cyl == 6').sort_values(by='mpg', ascending=False)

# %%
cars4 = cars.groupby(['car', 'cyl', 'gear'])
cars4.agg(
    disp_mean = ('disp', np.mean)
).reset_index() # reset the index for grouping car, cyl, gear
# %%

car = cars[cars['car'].str.contains('Hornet')].sort_values(['wt'])
#%%
cars.groupby('cyl').agg(['min','max','mean'])
# %%
cars.agg({'vs': np.mean})  

# %%

cars.value_counts('cyl')
pd.crosstab(cars.cyl, cars.carb)
# %%
cars.filter(['car', 'cyl', 'qsec']).assign(
    cyl_x_qsec = lambda x: x.cyl*x.qsec
)

# %%
pd.crosstab(cars.mpg,cars.cyl)
# %%
url = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.json"

# %%
http = urllib3.PoolManager()
response = http.request('GET', url)
cars_json = json.loads(response.data.decode('utf-8'))

cars_json
# %%

pd.DataFrame.from_dict(cars_json)
# %%

cars_json = json.loads(response.data.decode('utf-8'))
# %%
pd.json_normalize(cars_json)
# %%
data = [{'id': 1,
         'name': "Cole Volk",
         'fitness': {'height': 130, 'weight': 60}},
        {'name': "Mose Reg",
         'fitness': {'height': 130, 'weight': 60}},
        {'id': 2, 'name': 'Faye Raker',
         'fitness': {'height': 130, 'weight': 60}}]
pd.json_normalize(data, max_level=0)
# %%
pd.json_normalize(data, max_level=0)
# %%
pd.json_normalize(data, max_level=2)


# %%
pd.json_normalize(data, max_level=1)
# %%
# handling mising

df = (pd.DataFrame(
    np.random.randn(5, 3), 
    index=['a', 'c', 'e', 'f', 'h'],
    columns=['one', 'two', 'three'])
  .assign(
    four = 'bar', 
    five = lambda x: x.one > 0,
    six = [np.nan, np.nan, 2, 2, 1],
    seven = [4, 5, 5, np.nan, np.nan])
  )
df
# %%
# removing na from column six
df.six.fillna(0) + df.seven.fillna(0)
# %%
# ignores na when summing column
df.six.sum()
# %%
## starting day 2, project 2
df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman', np.nan],
                   "toy": [np.nan, 'Batmobile', 'Bullwhip',np.nan],
                   "born": [pd.NaT, pd.Timestamp("1940-04-25"),
                            pd.NaT, pd.NaT],
                    "power": [np.nan, np.nan, np.nan, np.nan]})
# %%
df
# %%
# drops the row of na's
df.dropna(how="all")

# %%
df.dropna(how="all", axis =1)
# %%
df.dropna(how="all", axis =1).dropna(how= "all")
# %%
df.dropna(subset = ['born'])
# %%
df.dropna(subset = ['toy'])
# %%
df

# %%
flights = pd.read_json("https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json")
# %%
# long way to load flights to understand json file
url_flights = 'https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json'
http = urllib3.PoolManager()
response = http.request('GET', url_flights)
flights_json = json.loads(response.data.decode('utf-8'))
flights = pd.json_normalize(flights_json)
flights.head()
# %%
flights.describe()
# %%
flights.value_counts()
# %%
flights.shape
# %%
# doesn't work!!!!
flights.dropna(subset = ['month'])
# %%
#  google pandas replace serioes
# didn't replace month n/a

flights = flights.month.replace('n/a' , np.NaN)
flights.month.describe()
# %%
flights
# %%
fli_mnth = flights.assign(
month = lambda x: x.month.replace('n/a', np.NaN)
)
# %%
fli_mnth
# %%
flights.columns

# %%
# airport code works with no nan
flights.airport_code.value_counts()
# %%
# data missing some airport names. Counts not same as airport code
flights.airport_name.value_counts()
# %%
flights.month.value_counts()
# %%
# missing some months in years
pd.crosstab(flights.month, flights.year)
# %%
# missing some months in airport codes
pd.crosstab(flights.month, flights.airport_code)
# %%
flights.year.describe()

# %%
flights.year.isna().sum()
# %%
flights.year.value_counts()
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
# taking the mean value found and replacing the -999 value with
# NaN and then filling in the mean and storing it in new data datac
datac = flights.assign(
    num_of_delays_late_aircraft 
    = lambda x: 
    x.num_of_delays_late_aircraft.replace(-999, np.NaN).fillna(ndmeans)
)
datac
# %%
flights.info()
# %%


