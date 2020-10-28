"""
This script cleans the open address data that's already been collected.
The comparisons are ultimately done based on street number and street name,
so we drop all entries where those, or the city field, are empty.
This script then does basic cleaning using the recordlinkage package,
including the removal of excess whitespace and removal of special characters.
It calls on special functions from the Address_Format_Funcs program that
standardise street names and directions to improve matching.

Joseph Kuchar
23-10-2020
"""
import pandas as pd
from recordlinkage.preprocessing import clean
from Address_Format_Funcs import AddressClean_en, AddressClean_fr

# Specify the Input CSV file location
INPUT_CSV_FILE = "NB_OA.csv"

# Specify the Output Directory location
OUTPUT_DIR = "Output_OA_STD_Files\\"

# Specify the City Name Column
CITY_COL = "CITY"

# Specify the Street Name Column
STREET_COL = "STREET"

# Specify the Street Number Column
NUMBER_COL = "NUMBER"

# Specify the Postal Code Column
POSTAL_CODE_COL = "POSTCODE"

# Specify the Latitude Column
LAT_COL = "LAT"

# Specify the Longitude Column
LONG_COL = "LON"

# Specify province (the OA data has already been collected into provincial level files)
PR = 'NB'
pr = PR.lower()

ADD = pd.read_csv(INPUT_CSV_FILE, low_memory=False)

# drop entries with null values
ADD = ADD.dropna(subset=[NUMBER_COL, STREET_COL, CITY_COL])

ADD[NUMBER_COL] = ADD[NUMBER_COL].astype(str)
ADD = ADD.reset_index()
ADD = ADD.fillna('')

# remove line breaking characters, if they exist
ADD[STREET_COL] = ADD[STREET_COL].str.replace('\n', '')

# perform basic cleaning
ADD[STREET_COL] = clean(ADD[STREET_COL])
ADD[CITY_COL] = clean(ADD[CITY_COL])
ADD[NUMBER_COL] = ADD[NUMBER_COL].str.replace('\n', '')

# abbreviate street types and directions
print('abbreviating types...')
if PR == 'QC':
    ADD = AddressClean_fr(ADD, STREET_COL, STREET_COL)
else:
    ADD = AddressClean_en(ADD, STREET_COL, STREET_COL)

# Drop all but the specified columns in the data frame
ADD = ADD[[LAT_COL, LONG_COL, NUMBER_COL, STREET_COL, CITY_COL, POSTAL_CODE_COL]]

N1 = len(ADD)
ADD['Duplicated'] = ADD.duplicated(subset=[NUMBER_COL, STREET_COL, CITY_COL], keep=False)
ADD.to_csv(OUTPUT_DIR+"Duplicates_"+PR+'_OA_STD.csv', index=False)
ADD = ADD.drop_duplicates(subset=[NUMBER_COL, STREET_COL, CITY_COL], keep='first')
N2 = len(ADD)

# Calculate how many duplicate rows existed in the data frame
print('dropped {} duplicates'.format(N1-N2))
ADD.to_csv(r''+OUTPUT_DIR+PR+'_OA_STD.csv', index=False)
