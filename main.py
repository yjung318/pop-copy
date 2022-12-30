#Python library for data manipulation and analysis
import pandas as pd 

#Python library for supporting large multidimensional arrays.
import numpy as np 

#Python library for machine learning
#Linear regression uses the relationship between the data-points to draw a straight line through all them.
#This line can be used to predict future values.
from sklearn.linear_model import LinearRegression 

#Imports regular expressions, which are special text strings used for searching for a pattern.
import re

#JSON is a standardized format commonly used to transfer data as text that can be sent over a network.
import json

#Ignores warnings
import warnings
warnings.filterwarnings("ignore")

from fastapi import FastAPI
# from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pop")
async def pop(country: str, year: int):
    return api_function(country, year)

def api_function(country, year):
    #Using pandas, read the csv file and set it equal to df.
    df = pd.read_csv('population.csv')
    
    #Renames the Country Name column to country_name.
    df.rename(columns={'Country Name':'country_name'},inplace=True)
    
    #Changes the country names to lowercase.
    df['country_name'] = df['country_name'].apply(lambda row: row.lower())
    
    #All unique country names are stored into this list.
    lists = df['country_name'].unique().tolist()
    
    #Convert the lists into a new json file.
    with open('country_list.json','w', encoding='utf-8') as f:
        json.dump(lists, f, ensure_ascii=False, indent=4)
    
    result = -1
    actual = -1
    
    if country in lists:
        df = df.loc[df['country_name']==country]
        df.drop(['country_name','Country Code','Indicator Name','Indicator Code'],axis=1,inplace=True)
        df = df.T
        df.dropna(inplace=True)
        df.columns = ['population']
        df=df.reset_index().rename(columns={'index':'year'})

        x = df.iloc[:, 0].values.reshape(-1,1)
        y = df.iloc[:, 1].values.reshape(-1,1)
        model = LinearRegression().fit(x,y)

        result = int(model.coef_[0][0] * year + model.intercept_[0])
        
        for i in range(len(df)):
            if df.loc[i, 'year']==str(year):
                actual=int(df.loc[i, 'population']) 
        print(f"\nThis model predicts that {country.capitalize()}\'s population in {year} is/will be {result:,d} people!")
        print(f"According to \"worldbank.org\" {country.capitalize()}\'s population in {year} was actually {actual:,d} people!")
    x = {
        "predicted": result,
        "actual": actual}
    y = json.dumps(x)
    return(y)
def main():
    country = "japan"
    year = 2003
    json_result = api_function(country, year)
    print(json_result)

if __name__ == "__main__":
    main()