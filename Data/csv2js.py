""" This file converts the csv data to a js array and saves it in a js file.
Before running this, make sure you follow these directions:
If you have run dataclean.py, and have a fresh refugee_origin....csv file, manually delete the top row that just says value,
and the random row below the year, and put Origin above afghanistan
also manual delete 1951 through '59, there is no data for those anyways

Before running the website, check that this object is correct
it should look like
const refugeeData = [[['country', number], ['country', number]], [... and so on"""

import pandas as pd
import numpy as np

pop_file = 'refugee_origin_pops_by_year.csv'
f = open("pop_data.js", "w")

df = pd.read_csv(pop_file)

countries = list(df['Origin'])
#print(countries)
country_count = len(countries)

f.write("const refugeeData = [")
for column in df.columns[1:]:
	f.write("[['Country', 'Fleeing Population'],")
	for i in range(country_count):
		f.write('["' + countries[i] + '",' + str(df[column][i]) + "],")
	f.write('],')
f.write(']')