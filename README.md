# OA_Linking

The scripts in this repository are meant to do a limited type of geocoding for data that can not be sent to an internet-based geocoder by matching it against a local download of open address data. It assumes the existence of a download of the data from OpenAddresses, aggregated at the provincial level (data available internally). 

The main scripts are OpenAddress_Standardise, which performs some address standardizations on the OpenAddresses data for easier matching, and recordlinkage_OA, which uses the recordlinkage package to match the addresses in the input file against those from OpenAddresses. The output is a csv with string comparison metrics for possible matches which can be manually verified to see if they are legitimate matches. 

The recordlinkage package allows for "blocking" when comparing two datasets, which means it considers only pairs of entries where both values are the same. In this case the blocking is done on the street number column, but if CSDUID were available then that could also be used to make sure that addresses are only compared in the same CSD.
