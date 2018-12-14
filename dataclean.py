import pandas as pd
import numpy as np

#This is the file I downloaded for 2017 data
#downloaded from http://popstats.unhcr.org/en/time_series
#selected 2017 data, all countries to all countries, only refugees
#export "current view, as .csv file"
#Had to manually open in excel, and remove the header and top rows
pop_file = "pop_stats_2017.csv"

#create pandas data frame from file
full_data_frame = pd.read_csv(pop_file)

#remove country of residence, and situation type (they are all refugees, left out asylum seekers, internally displaced people, etc.)
#value means population size
short_data_frame = full_data_frame[['Origin', 'Value']]

#values marked with a '*' mean population size of 1-4
#For now I think we can drop these values, later we might want to use them
short_data_frame = short_data_frame[short_data_frame['Value'] != '*']

#Because the col previously had '*' in it, it is a string col, and needs to become an int col
short_data_frame['Value'] = pd.to_numeric(short_data_frame['Value'])

#There are a lot of duplicates, this is because we dropped the new country of residence
#I dont know why it converts from dataframe to series here, but I use to_frame to keep it as a datframe (more than 1 col)
fixed_data_frame = short_data_frame.groupby('Origin')['Value'].sum().to_frame()

#It gives some stuff like 7 refugees from Canada, and I don't know how to interpret that, 
#so I think it is reasonable to pick a cut off. For now I chose 100
#maybe it would be better to use 500, or 1000, or even higher, once we see the rest of our data
final_data_frame = fixed_data_frame[fixed_data_frame.Value >= 1000]

#uncomment to see info about this dataframe (size, shape, etc)
#print(final_data_frame.info())

#uncomment to see what the first 10 values now look like
#print(final_data_frame.head(10))

#return this to csv file, which can be opened by google sheets
final_data_frame.to_csv('cleaned_data_2017.csv')