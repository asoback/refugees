import pandas as pd
import numpy as np

#This is the file I downloaded for the complete data
#downloaded from http://popstats.unhcr.org/en/time_series
#selected all years data, all countries to all countries, only refugees
#export "current view, as .csv file"
#Had to manually open in excel, and remove the header and top rows
pop_file = "pop_stats_full.csv"

#create pandas data frame from file
full_data_frame = pd.read_csv(pop_file)

#remove country of residence, and situation type (they are all refugees, left out asylum seekers, internally displaced people, etc.)
#value means population size
short_data_frame = full_data_frame[['Year', 'Origin', 'Value']]

#values marked with a '*' mean population size of 1-4
#For now I think we can drop these values, later we might want to use them
short_data_frame = short_data_frame[short_data_frame['Value'] != '*']

#Because the col previously had '*' in it, it is a string col, and needs to become an int col
short_data_frame['Value'] = pd.to_numeric(short_data_frame['Value'])

#There are a lot of duplicates, this is because we dropped the new country of residence
#I dont know why it converts from dataframe to series here, but I use to_frame to keep it as a datframe (more than 1 col)
fixed_data_frame = short_data_frame.groupby(['Year', 'Origin'])['Value'].sum().to_frame()

#It gives some stuff like 7 refugees from Canada, and I don't know how to interpret that, 
#so I think it is reasonable to pick a cut off. For now I chose 100
#maybe it would be better to use 500, or 1000, or even higher, once we see the rest of our data
final_data_frame = fixed_data_frame[fixed_data_frame.Value >= 1000]

#Still need to adjust some values in order to work with google sheets. values that are off: 
	#Tibetan: ?, Various/Unknown: ?, #Stateless : ?
d = {r"Dem. People's Rep. of Korea": "North Korea", 
	r"Syrian Arab Rep." : 'Syria', 
	r'Bolivia (Plurinational State of)': 'Bolivia', 
	r'Iran (Islamic Rep. of)': 'Iran',
	r'Serbia and Kosovo (S/RES/1244 (1999))': 'Serbia and Kosovo',
	r'Venezuela (Bolivarian Republic of)': 'Venezuela'}
final_data_frame = final_data_frame.rename(d)

#Here I am going to make a new table with index being each country, and columns being year, and fill in the pops for each cell
df = final_data_frame.unstack(level='Year')

df.fillna(0, inplace=True)

#return this to csv file, which can be opened by google sheets
df.to_csv('refugee_origin_pops_by_year.csv')
