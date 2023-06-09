#!/usr/bin/env python3
"""
# course: CMPS3500
# CLASS Project
# PYTHON IMPLEMENTATION: BASIC DATA ANALYSIS
# date: 3/30/23
# Student 1: Michael Kausch
# Student 2: David Mesa
# Student 3: Irvin Neri Zavala
# Student 4: Samantha Tellez
# Student 5: Raul Verduzco Guillen
# description: Implementation Basic Data Analysis Routines
"""

import pandas as pd
import time
import os
from datetime import datetime
import math
import re
import calendar

######################################################
##       Statistical / Mathematical Functions       ##       
######################################################

def counts(data):
    ''' takes in a list of data and returns the number of items
        note: i realize len() is much simpler but its not allowed here'''
    count = 0
    # loop through data add one per row in data
    for row in data:
        count += 1
    # print("Count: " ,  count)
    return count

def uniqueCounts(data):
    '''returns the number of unique items in a list'''
    # isDate = True
    unique_set = set()
    # loop through data and store if was not previously found
    for unique in data:
        if not pd.isna(unique):
            if isinstance(unique, str):
                
                try:
                    datetime.strptime(unique, '%m/%d/%Y %I:%M:%S %p')
                except ValueError:
                    pass
            if unique not in unique_set:
                unique_set.add(unique)
    return len(unique_set)

# mean varianca and Standard Deviation
'''calculates all 3''' 
def meanVarStdev(data):
    # variables
    
    stats = {'mean': 0, 'var': 0, 'st_dev': 0}
    stand_diff = set()
    sum_sq = 0

    # Step1: find the stats['mean']
    for index in data:
        stats['mean'] += index
    stats['mean'] = round(stats['mean'] / len(data))

    # Step 2: find each deviation of the stats['mean'] and square then add it to stand_diff list
    for index in data:
        stand_diff.add(math.pow((stats['mean'] - index), 2))

    for sum_index in stand_diff:
        sum_sq += sum_index

    stats['var'] = (round(sum_sq/ (len(data)-1),4))
    stats['st_dev'] = math.sqrt(stats['var'])

    return stats

def medianFunc2(data):
    '''Takes in a sorted list and returns middle value'''
    mid = int((len(data)/2))
    # print("mid is", mid)
    return data[mid]

def minFunc2(data):
    '''data: a list sorted in ascending order'''
    return data[0]

def maxFunc2(data):
    '''data: a list sorted in ascending order'''
    return data[-1]

def modeFunc2(sorted_list):
    '''takes in a sorted list of data in its correct format'''
    data = dict()
    for item in sorted_list:
        data[item] = data.get(item,0) + 1
        # print(item, ":", data[item])
    
    sorted_data = sorted([(v,k) for (k,v) in data.items()], reverse=True)
    # print("mode is:", sorted_data[0][1])
    return sorted_data[0][1]    
    

######################################################
##         Answers to Data Analysis Questions      ##       
######################################################

def totalUniqueCount(filename):
    now = datetime.now()
    #pandaBegin = time.time()
    # group data by year and count unique crimes
    count_by_year = filename.groupby('year')['DR_NO'].nunique()
    
    # sort the counts in descending order and return them
    sorted_counts = sorted(count_by_year.items(), key=lambda x: x[1], reverse=True)
    for year, count in sorted_counts:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"[{current_time}] ""{}: Total Unique Crimes {}".format(year, count))
    #pandaTimeEnd = time.time()
    #print("Time:", (pandaTimeEnd - pandaBegin),"sec.")


def countCrimesByArea(data):
    now =datetime.now()
    #begin = time.time()
    # group data by area name and count crimes
    counts_by_area = data.groupby('AREA NAME')['Crm Cd'].count()
    
    # sort the counts in descending order and return the top 5
    top_5_areas = counts_by_area.sort_values(ascending=False)[:5]
    
    # print the results
    
    for area, count in top_5_areas.items():
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"[{current_time}] {area}: {count} crimes")
       
    #end = time.time()
    #print("Time:", (end - begin,"sec."))

def MonthsUniqueCrimes(data):
    # copy data and add index locater
    data_copy = data.copy()
    data_copy = data.reindex(['DATE OCC', 'DR_NO'], axis = 1)
    data_copy.iloc[0,1]
    

    # Convert the date column to datetime format
    data['DATE OCC'] = pd.to_datetime(data['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Group the data by month and count unique crimes
    counts_by_month = data.groupby(data['DATE OCC'].dt.strftime('%B'))['DR_NO'].nunique()
    
    # Sort the counts in ascending order and return them
    now = datetime.now()
    sorted_counts = sorted(counts_by_month.items(), key=lambda x: x[1])
    for month, count in sorted_counts:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"[{current_time}] ""{}: Total Unique Crimes {}".format(month, count))

def Top10Streets(data):
    # Filter the data for the year 2019
    data2019 = data[data['year'] == 2019]

    # Count the occurrences of each street name
    street_counts = data2019['LOCATION'].value_counts()

    # Select the top 10 streets with the most crimes
    top_streets = street_counts.head(10)

    # Print the results
    now = datetime.now()
    # for i, (street, count) in enumerate(topStreets.iteritems()):
    for i, (street, count) in enumerate(top_streets.items()):
        current_time = now.strftime("%H:%M:%S.%f")
        easy_street = " ".join(street.split())
        print(f"[{current_time}] {i+1}. {easy_street}: {count} crimes")

def Top5HWood(data):
    now = datetime.now()
    
    # Filter the data to include only the specified area
    area_name = 'Hollywood'
    area_data = data[data['AREA NAME'] == area_name].copy() # make a copy of the slice
    area_data.loc[:, 'TIME OCC'] = pd.to_datetime(area_data['TIME OCC'].astype(str), format='%H%M', errors='coerce')
    
    # Count the number of crimes that occur in each hour of the day
    crime_counts = area_data.groupby(area_data['TIME OCC'].dt.hour).size().sort_values(ascending=False)
    
    # Select the top n hours with the most crimes
    top_hours = crime_counts.head(5)
    
    # Print the results
    
    # for i, (hour, count) in enumerate(topHours.iteritems()):
    for i, (hour, count) in enumerate(top_hours.items()):
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"[{current_time}] {i+1}: {int(hour):02d}:00 - {int(hour):02d}:59: {count} crimes")

def printCCFrauds(data):
    now = datetime.now()
    # Convert Date Rptd column to datetime format
    data["DATE OCC"] = pd.to_datetime(data["DATE OCC"], format="%m/%d/%Y %I:%M:%S %p")
    
    # Filter for major credit card frauds in 2019
    fraud_data = data.loc[(data["Crm Cd Desc"] == "CREDIT CARDS, FRAUD USE ($950 & UNDER") & (data["year"] == 2019), :]

    if len(fraud_data) == 0:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f'[{current_time}] No credit card frauds found in 2019')
        return

    # Extract month from DATE OCC column using .dt accessor
    fraud_data = fraud_data.assign(month=fraud_data["DATE OCC"].dt.month)

    # Count the number of frauds by month
    fraud_counts_by_month = fraud_data["month"].value_counts()

    # Find the month(s) with the most frauds
    max_fraud_count = fraud_counts_by_month.max()
    months_with_max_fraud = fraud_counts_by_month[fraud_counts_by_month == max_fraud_count].index
    month_names = [calendar.month_name[m] for m in months_with_max_fraud]

    # Print the result
    if len(month_names) == 1:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f'[{current_time}] The month with the most major credit card frauds in 2019 is {month_names[0]}, with {max_fraud_count} frauds.')
    else:
        month_str = " and ".join(month_names)
        current_time = now.strftime("%H:%M:%S.%f")
        print(f'[{current_time}] The months with the most major credit card frauds in 2019 are {month_str}, with {max_fraud_count} frauds each.')
    
    # Loop through all months and print out the fraud data for each month
    #For testing purposes
    # for month in range(1, 13):
    #     fraudDateForMonth = fraudData[fraudData["month"] == month]
    #     print(f"Month {month}: {len(fraudDateForMonth)} frauds")
    #     print(fraudDateForMonth.head())
       
def MostTime(data):
    now = datetime.now()
    data_copy = data.copy()
    data_copy.iloc[0,1]
  
    # Create a new column with the time difference between the report date and the date the crime occurred
    data_copy['DATE OCC'] = pd.to_datetime(data_copy['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p') - pd.to_datetime(data_copy['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Sort the DataFrame by the time difference column in descending order
    sorted_data = data_copy.sort_values(by='DATE OCC', ascending=False)
    
    # Get the details of the crime wit\nh the highest time difference
    max_reported_time = sorted_data.iloc[0]
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"[{current_time}] Time difference in hours: {max_reported_time['DATE OCC'].total_seconds() / 3600}")
    # Print the details of the crime
    for key, value in max_reported_time.to_dict().items():
        current_time = now.strftime("%H:%M:%S.%f")
        if (key == 'LOCATION'):
            easy_street = " ".join(value.split())
            print(f"[{current_time}] {key}: {easy_street}")
        else:
            print(f"[{current_time}] {key}: {value}")

def printMostCommonCrime(data):
    now = datetime.now()
     # Count the occurrences of each crime type
    crime_counts = data.groupby('Crm Cd Desc').size().sort_values(ascending=False)

    # Select the top 10 most frequent crime types
    top_crime_types = crime_counts.head(10)

    # Print the results
    # for i, (crimeType, count) in enumerate(topCrimeTypes.iteritems()):
    for i, (crimeType, count) in enumerate(top_crime_types.items()):
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"[{current_time}] {i+1}. {crimeType}: {count}")

def printLALunchTime(data):
    now = datetime.now()
    # Make a copy of the data so that the original data is not modified
    data_copy = data.copy()
    data_copy['DATE OCC'] = pd.to_datetime(data_copy['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p') - pd.to_datetime(data_copy['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p')
    # Convert the Date Occurred column to a datetime datatype
    data_copy['DATE OCC'] = pd.Timestamp('1900-01-01') + pd.to_timedelta(data_copy['DATE OCC'], unit='D')

    # Extract the victim sex and time of the crime
    data_copy['Vict Sex'] = data_copy['Vict Sex'].str.upper()

    # Convert 'TIME OCC' column to string and remove any non-numeric characters
    data_copy['TIME OCC'] = data_copy['TIME OCC'].astype(str).str.replace(r'\D', '', regex=True)

    # Convert 'TIME OCC' column to datetime object
    data_copy['TIME OCC'] = pd.to_datetime(data_copy['TIME OCC'], format='%H%M', errors='coerce')

    # Remove any rows with missing datetime values
    data_copy.dropna(subset=['TIME OCC'], inplace=True)

    # Extract hour component from datetime object
    data_copy['TIME OCC'] = data_copy['TIME OCC'].dt.hour

    # Filter the dataset to only include crimes between 11:00am and 1:00pm
    data_lunch_time = data_copy[(data_copy['TIME OCC'] >= 11) & (data_copy['TIME OCC'] <= 13)]

    # Calculate the number of crimes for each gender
    num_female_victims = len(data_lunch_time[data_lunch_time['Vict Sex'] == 'F'])
    num_male_victims = len(data_lunch_time[data_lunch_time['Vict Sex'] == 'M'])

    # Print the results
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] Evidence:")
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] Number of female victims between 11:00am and 1:00pm: {num_female_victims}")
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"[{current_time}] Number of male victims between 11:00am and 1:00pm: {num_male_victims}")

    print(f"\n[{current_time}] Answer:")
    if num_female_victims > num_male_victims:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"\n[{current_time}] Women are more likely to be the victim of a crime during lunchtime.")
    elif num_female_victims < num_male_victims:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"\n[{current_time}] Men are more likely to be the victim of a crime during lunchtime.")
    else:
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"\n[{current_time}] There is an equal likelihood of men and women being the victim of a crime during lunchtime.")


def OlderManTop5(data):
    now = datetime.now()
    # Convert DATE OCC column to datetime format
    data["DATE OCC"] = pd.to_datetime(data["DATE OCC"], format="%m/%d/%Y %I:%M:%S %p")

    # Filter for crimes that occurred in December 2018 and involved a victim age 65 or older and male gender
    filtered_data = data.loc[(data["DATE OCC"].dt.year == 2018) & (data["DATE OCC"].dt.month == 12) & (data["Vict Age"] >= 65) & (data["Vict Sex"] == "M"), :]

    # Count the number of crimes in each area and sort in descending order
    crime_count_by_area = filtered_data["AREA NAME"].value_counts().sort_values(ascending=False)
    
    # Print the top 5 dangerous areas
    for i,(area, count) in enumerate(crime_count_by_area.head(5).items(), 1):
        current_time = now.strftime("%H:%M:%S.%f")
        print(f"[{current_time}] {i}. {area}: {count}")



######################################################
##        File I/O / System Functions               ##
######################################################

# clears screen - designed to work on multiple os's
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
'''Gets a list of csv files in the current working directory'''
def getCsvFileList():
    os.chdir(os.getcwd())   # change directory to current working directory
    files = []  # make an empty list
    for file in os.listdir():   #iterate through all filenames in ls
        # previous method:
        # file_lower = file.lower()
        # print(file_lower)
        # dot_pos = file.find('.')    # find where the . is for the file extension
        # ext = file[dot_pos+1:]  # get a string of what's leftover from the . onward
        # if (ext.lower() == "csv"):
        #     files.append(file)  # append if it's a csv file
        # easier and simpler
        
        # if ".csv" in file.lower():
        #     files.append(file)
        
        # third method: safest in case of poor file naming by professor
        ext = os.path.splitext(file)
        if (ext[1].lower() == ".csv"):
            files.append(file)    
        
    # print(files) # debug
    return files
        
#Time to read and store data in an array
def readFile(file_name="Crime_Data_from_2017_to_2019.csv"):
    '''Pass in name of data file, will call the main file we were given by default
        Returns: pandas dataframe containing all of the data less the 5 dropped columns'''
    csv_arr = pd.read_csv(file_name, quotechar='"', delimiter=',', skipinitialspace=True, dtype = {"Date Rptd":"string", "year": "int32"} )
    
    drop_columns2 = ['Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street']

    try:
        csv_arr.drop('Unnamed: 0',  axis= 1, inplace = True)
        csv_arr.drop(drop_columns2, axis= 1, inplace = True)
    except:
        pass
    
    headers = list(csv_arr.columns)

    return(csv_arr)

        
def writeDataset(data_frame, num_rows):
    '''takes in a dataframe and writes num_rows number of rows out to a file
    with the date appended to the filename'''
    
    pd.set_option('display.max_columns', None)
    print(data_frame.iloc[:num_rows])
    
    date_time = datetime.now()
    dts = date_time.strftime("%y%m%d%H%M%S_data_print.csv")
    try:
        data_frame.iloc[:num_rows].to_csv(dts)
        print("Data was written to ((", dts, ")) successfully")
    except:
        print("Data was not written successfully")
    pd.reset_option("max_columns")
    
def writeSort(dlist):
    '''takes in a list of items from sort function and writes 
    the data out to a csv file with the date appended to the filename'''
    
    date_time = datetime.now()
    dts = date_time.strftime("%y%m%d%H%M%S_sorted_data.txt")
    print("Sorted data is being written to ((", dts, "))")
    f = open(dts, 'w')
    for item in dlist:
        f.write(str(item) + '\n')
    f.close()
    print(f"file {dts} written successfully")
    
def writeSearch(data_frame, row_match):
    ''' takes in a pandas dataframe and a list of rows from the search fucntion
    that are matches from the search and write the matches out to a file with 
    the date appended to the file name'''
    
    if (len(row_match) > 0):
        pd.set_option('display.max_columns', None)
        # print(data_frame.loc[row_match])
        date_time = datetime.now()
        dts = date_time.strftime("%y%m%d%H%M%S_search.csv")
        print("Search Results are writing to ((", dts, "))")
        data_frame.iloc[row_match].to_csv(dts)
        pd.reset_option("max_columns")
        print(f"file {dts} written successfully")
    else:
        print(f"No search results, not writing to a file.")


######################################################
##                 Sorting / Searching              ##
######################################################

# searches a specified data_frame column for a user inputed string/integer
def search(data_frame, col_num, search_string):
    row_match = []
    found = False
    col_name = data_frame.columns[col_num]
    
    print("Searching...")
    s_time = time.time()
    for index, row in data_frame.iterrows():
        if(re.search(search_string, str(row[col_name]), re.IGNORECASE)):
            row_match.append(index)
    e_time = time.time()
        
    if (len(row_match) != 0):
        print(len(row_match), "Items found!")
        print(data_frame.loc[row_match])
        print("Time to process is", (e_time-s_time),"sec.")
    else:
        print(f"could not locate (({search_string})) in the data")
        print("Total search time was", (e_time-s_time),"sec.")
        print("Either the data wasn't in the table or you should")
        print("check that you entered the information correctly")
    
    writeSearch(data_frame, row_match)
    
    input("Press any key to continue")

def sortData(lst, format):
    ''' method for sorting data frame data by passed in column_name
        lst             Data list to sort
        format = 1      Ascending
        format = 2      Descending'''
    s_time = time.time()
    if (format == 1):
        heapSort2(lst, len(lst))
        # heapSort1(lst)
    elif (format == 2):
        minHeapSort(lst, len(lst))
    else:
        print("bad arg", format, "passed to sortData")
    e_time = time.time()
    print("Time to sort is", (e_time-s_time),"sec.")
    return lst
    


def minHeapify(lst, n, i):
    ''' creates a minheap from a list of items'''
    smallest = i    #initialize smallest as root
    l = 2 * i + 1 # left child
    r = 2 * i + 2 # right child

    #check left child is smaller
    if l < n and lst[l] < lst[smallest]:
        smallest = l
    
    # check if right child is smaller
    if r < n and lst[r] < lst[smallest]:
        smallest = r
    
    # swap if smallest is not root
    if smallest != i:
        (lst[i], lst[smallest]) = (lst[smallest], lst[i])
        # recursively minheapify the subtree
        minHeapify(lst, n, smallest)

# faster heapify that follows minheap which was faster
def heapify2(lst, n, i):
    ''' creates a maxheap from a list of items'''
    biggest = i    #initialize biggest as root
    l = 2 * i + 1 # left child
    r = 2 * i + 2 # right child

    #check left child is smaller
    if l < n and lst[l] > lst[biggest]:
        biggest = l
    
    # check if right child is smaller
    if r < n and lst[r] > lst[biggest]:
        biggest = r
    
    # swap if biggest is not root
    if biggest != i:
        (lst[i], lst[biggest]) = (lst[biggest], lst[i])
        # recursively minheapify the subtree
        heapify2(lst, n, biggest)

# previous implementation, leaving for historical purposes until we know that everything works fully
def heapify(lst, i, upper):
    ''' creats a maxheap from a list of items'''
    while (True):
        l, r = i*2+1, i*2+2

        # 2 children
        if (max(l,r) < upper):
            if (lst[i] >= max(lst[l], lst[r])):
                break
            elif (lst[l] > lst[r]):
                lst[l], lst[i] = lst[i], lst[l]
                i = l
            else:
                lst[r], lst[i] = lst[i], lst[r]
                i = r
                
        # 1 child
        elif (l < upper):
            if lst[l] > lst[i]:
                lst[l], lst[i] = lst[i], lst[l]
                i = l
            else:
                break
        elif (r < upper):
            if lst[r] > lst[i]:
                lst[r], lst[i] = lst[i], lst[r]
                i = r
            else:
                break
        # no children
        else:
            break
  
# The main function to sort an array of given size
  
def heapSort(lst):
    '''sorts by heapsort using maxheap
        this results in a sorted list in ascending order'''
    for itm in range(len(lst)-2//2, -1, -1):
        heapify(lst, itm, len(lst))
    
    for end in range(len(lst)-1, 0, -1):
        lst[0], lst[end] = lst[end], lst[0]
        heapify(lst, 0, end)
        
def heapSort2(lst, n):
    '''sorts by heapsort using minheap
        this results in a sorted list in descending order'''
    for i in range(int(n/2) -1, -1, -1):
        heapify2(lst, n, i)
        
    for i in range(n-1, -1, -1):
        lst[0], lst[i] = lst[i], lst[0]
        heapify2(lst, i, 0)

def minHeapSort(lst, n):
    '''sorts by heapsort using minheap
        this results in a sorted list in descending order'''
    for i in range(int(n/2) -1, -1, -1):
        minHeapify(lst, n, i)
        
    for i in range(n-1, -1, -1):
        lst[0], lst[i] = lst[i], lst[0]
        minHeapify(lst, i, 0)


######################################################
##          User Input /  Printing Functions        ##
######################################################


def describeColumn2(clean_sorted_lst, col_number, data_bools, **kwargs):
    '''Helper function that calls math functions and prints results'''
       
    total = counts(clean_sorted_lst)
    unique = uniqueCounts(clean_sorted_lst)
    # print("col_number", col_number)
    # print("len(data_bools):", len(data_bools))
    if (data_bools[col_number]["mean"] == True):
        # print("getting standev")
        mvs = meanVarStdev(clean_sorted_lst)
    else:
        mvs = None
    if (data_bools[col_number]["median"] == True):
        # print("getting median")
        med = medianFunc2(clean_sorted_lst)
    else:
        med = None
    if (data_bools[col_number]["mode"] == True):
        # print("getting mode")
        mode = modeFunc2(clean_sorted_lst)
    else:
        mode = None
    if (data_bools[col_number]["min"] == True):
        # print("getting min")
        min = minFunc2(clean_sorted_lst)
    else:
        min = None
    if (data_bools[col_number]["max"] == True):
        # print("getting max")
        max = maxFunc2(clean_sorted_lst)
    else:
        max = None
        
   
    print("Count:", total)
    print("Unique:", unique)
    
    
    
    if 'dtype' in kwargs:
        # print("date passed in")
        
        
        d = pd.to_datetime("2010-01-01") + pd.DateOffset(days=mvs['mean'])
        print("Mean:", d.strftime("%m/%d/%Y"))
        
        d = pd.to_datetime("2010-01-01") + pd.DateOffset(days=med)
        print("Median:", d.strftime("%m/%d/%Y"))
        
        d = pd.to_datetime("2010-01-01") + pd.DateOffset(days=mode)
        print("Mode", d.strftime("%m/%d/%Y"))
        
        d = pd.to_datetime("2010-01-01") + pd.DateOffset(days=min)
        print("Minimum:", d.strftime("%m/%d/%Y"))
        
        d = pd.to_datetime("2010-01-01") + pd.DateOffset(days=max)
        print("Maximum:", d.strftime("%m/%d/%Y"))
        
        print("STDEV: ", mvs['st_dev'], "days")
        print("Variance: ", mvs['var'], "days squared")

    else:
        if (mvs is not None):
            print("Mean:", mvs['mean'])
        else:
            print("Mean: N/A")
        if (med is not None):
            print("Median:", med)
        else:
            print("Median: N/A")
        if (mode is not None):
            print("Mode", mode)
        else:
            print("Mode: N/A")
        if (min is not None):
            print("Minimum:", min)
        else:
            print("Minimum: N/A")
        if (max is not None):
            print("Maximum:", max)
        else:
            print("Maximum: N/A")
        if (mvs is not None):
            print("STDEV: ", mvs['st_dev'])
            print("Variance: ", mvs['var'])
        else:
            print ("STDEV: N/A")
            print ("Variance: N/A")



def getPrintColumns(dframe):
    ''' prints headers of a dataframe'''
    headers = list(dframe.columns)
    print(headers)


def getResponse(foo, min_val, max_val, **kwargs):
    '''Takes in a print function (foo) and tests against minimum
        and maximum menu options.
        Function returns an integer value that met the response criteria
        if function foo takes parameters (like a list), they are included as a key word
        argument arg_list'''
    response = -2
    
    if 'arg_list' not in kwargs:
        pass
    
    # if 'arg_list' in kwargs:
    #     print(f"you passed in an arg_list:")
    #     print(f"{kwargs.get('arg_list')}")
    
    while ((response < min_val) or (response > max_val)):
        # foo()
        
        try:
            str_response = input("Enter your response: ")
            response = int(str_response)
            
            if ((response < min_val) or (response > max_val)):
                #os.system('clear')
                clear()
                if 'arg_list' in kwargs:
                    foo(kwargs.get('arg_list'))
                else:
                    foo()
                print(response, "is not in the range of acceptable values.")
                print("Enter a value between", min_val, "and", max_val)
        except:
            #os.system('clear')
            clear()
            
            if 'arg_list' in kwargs:
                foo(kwargs.get('arg_list'))
            else:
                # print('arg list not found so calling reg foo()')
                # input()
                foo()
                
            print(str_response, "is not a valid response. Please enter an integer.")
            response = -2
        
    return response

      
def printBaseMenu():
    print("Main Menu:")
    print("**********")
    print("1. Load Data")
    print("2. Explore Data")
    print("3. Data Analysis")
    print("4. Print Data Set")
    print("5. Quit")

def printDataSelectMenu(menu_list=None):
    """prints data select menu

    Args:
        menu_list (list of menu items, optional): Defaults to None.
    """
    # print("menu_list passed in:")
    # print(menu_list)
    # if (menu_list == None):
    #     menu_list = files.getCsvFileList()
    print("Load data set:")
    print("***************")
    
    print(f"Please select from the following available files:")
    for i in range(len(menu_list)):
        print(f"\t[{i+1}]: {menu_list[i]}")
        
        
def printDataExpMenu():
    print("Exploring Data:")
    print("**********")
    print("21. List all Columns:")
    print("22. Drop Columns:")
    print("23. Describe Columns:")
    print("24. Search Element in Column:")
    print("25. Sort by Column:")
    print("26. Back to the Main Menu")
        

def printDropHeaders(header_list):
    printHeaders(header_list)
    print("Enter a column number to drop")
    print("Enter -1 to finish entering columns")
    

def printDayPrompt():
    print("What day do you want to search? (DD)")

def printMonthPrompt():
    print("What month do you want to search? (MM)")
    
def printYearPrompt():
    print("What year do you want to search? (YYYY)")
    
# def printInclHeaders(incl_header_list):
#     printHeaders(incl_header_list)
#     print("Enter a column number to add")
#     print("Enter -1 to finish entering columns")    
   
def printHeaders(header_list):
    for i in range(len(header_list)):
        print(f"[{i}] {header_list[i]}")
    
def printDescribeColMenu(incl_header_list):
    print("Describe Columns:")
    print("*****************")
    print("*****************")
    printHeaders(incl_header_list)
    print("Enter the column number to desribe")
    # print("Enter -1 to finish entering columns")    
    
def printSearchMenu(header_list):
    print("Search Element in Column:")
    print("**************************")
    for i in range(len(header_list)):
        print(f"[{i}] {header_list[i]}")   
    print("Select the column number to perform a search")
    print("Enter -1 to finish entering columns")
    
def printSortMenu(header_list):
    print("Sort Data Column:")
    print("**************************")
    for i in range(len(header_list)):
        print(f"[{i}] {header_list[i]}")   
    print("Select the column number to sort")
    print("Enter -1 to return to the previous menu")
    
def printAscDescMenu():
    print("Select Ascending or Descending")
    print("[1] Ascending")
    print("[2] Descending")
    
def printDataAnalysis(df):
    now = datetime.now()
    data_copy = df.copy()
    
    print("Data Analysis:")
    print("***************")
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"[{current_time}] 1. Show the total unique count of crimes per year sorted in descending order:")
    totalUniqueCount(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 2. Show the top 5 areas with the most crime events in all years:")
    countCrimesByArea(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 3. Show all months and the unique total count of crimes sorted in increasing order.")
    MonthsUniqueCrimes(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 4. Show the top 10 streets with the most crimes in LA in 2019. Also display the total amount of crimes in each street.")
    Top10Streets(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 5. Show the top 5 most dangerous times (in hours) to be in Hollywood. Also display the total amount of crimes in each hour.")
    Top5HWood(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 6. Print the details of the crime that that took the most time (in hours) to be reported.")
    MostTime(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 7. Show the 10 top most common crime types (Crm Cd Desc) overall across all years.")
    printMostCommonCrime(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 8. Are woman or men more likely to be the victim of a crime in LA between lunch time (11:00am and 1:00pm)?. Support of your answer.")
    printLALunchTime(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 9. What is the month the has the most major credit card frauds (Crm Cd Desc = 'CREDIT CARDS, FRAUD USE ($950 & UNDER')) in LA in 2019.")
    printCCFrauds(data_copy)
    
    current_time = now.strftime("%H:%M:%S.%f")
    print(f"\n[{current_time}] 10. List the top 5 more dangerous areas for older man (age from 65 and more) in december of 2018.")
    OlderManTop5(data_copy)
   
 
def printMenu():
    print("  Print Menu  :")
    print("***************")
    print(f"\t[0] = first 100 lines")
    print(f"\t[1] = first 1000 lines")
    print(f"\t[2] = first 5000 lines\n")
    print(f"Select how many rows to print")
    print("Enter -1 to go back")



######################################################
##       Data Input / Prompt Printing Functions     ##
######################################################


'''Main Logic // Menu loop'''
def main():
    
    menu_option = None
    data_frame = pd.DataFrame()
    error_msg = ""
    # included_headers = []
    # excluded_headers = []
    all_headers = []
    data_frame_bak = None
    
    data_bools_unmod = [
                    # dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #0
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #1 DR_NO (INT)
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #2 DATE rptd
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #3 DATE occ
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #4 TIME occ (INT)
                    
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #5 area
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #6 area name
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #7 rpt dist no
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #8 part 1-2
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #9 crm cd
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #10 crm cd desc
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #11 mocodes *added mean/std/var
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #12 Age
                    
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #13 Sex * added min/max
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #14 Descent * added min/max
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #15 Premesis Code * added mean/std/var
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #16 Premesis Description * added min/max/med
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #17 Weapon Used Cd * added mean/std/var/min/max
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #18 Weapon Desc * added min/max/med
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #19 Status
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #20 Status Desc
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #21 Crm Cd 1 * added m/s/v/min/max
                    # dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #22
                    # dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #23
                    # dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #24
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #25 Location
                    # dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #26
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #27 LAT
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #28 LON
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True)] #29 YEAR
    data_bools = data_bools_unmod.copy()
    
    
    while (menu_option != 5):
        #os.system("clear")
        clear()
        if (error_msg != ""):
            print(error_msg)
            error_msg = ""
        
        printBaseMenu()
        menu_option = getResponse(printBaseMenu, 1, 5)
        # print("you selected option", menu_option)   #debug
        
        
        if (menu_option== 1):
            #os.system("clear")
            clear()
            menu_list = getCsvFileList()
            printDataSelectMenu(menu_list)
            sub_menu_option = getResponse(printDataSelectMenu, 1, len(menu_list), arg_list=menu_list)
            # print("calling readFile on",menu_list[sub_menu_option-1])
            print("")
            
            try:
                s_time = time.time()
                data_frame = readFile(menu_list[sub_menu_option-1])
                e_time = time.time()
                print("[start time]", s_time)
                print("[end time]", e_time)
                print("Time to load:", (e_time-s_time),"sec.")
                all_headers = list(data_frame.columns)
                data_frame_bak = data_frame.copy()
                data_bools = data_bools_unmod.copy()
                # included_headers = all_headers.copy() # save backup of all column names
                # print("included headers:")
                # print(included_headers)
                print(f"\nTotal Columns Read: {len(all_headers)}")
                print(f"Total Rows Read: {len(data_frame.index)}")
                # print(f"\nTotal Elements (Not null) in each category:\n\n{data_frame.notna().sum()}")
                
            except:
                error_msg = f"could not load data file {menu_list[sub_menu_option-1]}"

            input("press enter to continue...")
            continue
            
        elif (menu_option == 2):
            # Explore Data
            #os.system("clear")
            clear()
            if (data_frame.empty):
                error_msg = """You haven't loaded any data yet!
                Select option 1 from the main menu"""
                continue
            
            # print("Data Exploration Section")
            sub_menu_option = 0
            print_msg = ""
            while (sub_menu_option != 26):
                # get user input until correct
                #os.system("clear")
                clear()
                if (print_msg != "" ):
                    print(print_msg)
                    print_msg = ""
                printDataExpMenu()
                sub_menu_option = getResponse(printDataExpMenu, 21, 26)
                col_number = 0

                if (sub_menu_option == 21):
                    # list all columns
                    clear()
                    print("*****************")
                    print(f"Data Columns:\n")
                    print("*****************")
                    printHeaders(all_headers)
                    print("*****************")
                    print("*****************")
                    input(f"\npress enter to continue...")
                    continue
                    
                elif (sub_menu_option == 22):
                    # Drop Columns
                    #clear()
                    while (col_number != -1):
                        clear()
                        
                        
                        printDropHeaders(all_headers)
                        col_number = getResponse(printDropHeaders, -1, len(all_headers)-1, arg_list=all_headers)
                        # print("col_number now",col_number)
                        
                        if (col_number != -1):
                            # excluded_headers.append(included_headers[col_number])
                            # print(f"excluded headers last: {excluded_headers[-1]}")
                            # included_headers.remove(included_headers[col_number])
                            data_frame.drop(columns = [all_headers[col_number]], inplace=True)
                            print(f"\nColumn {all_headers[col_number]}\n")
                            all_headers = list(data_frame.columns)
                            data_bools.pop(col_number)
                            input(f"\nwas successfully dropped. Press any key...")
                            
                            # print("included_headers now***")
                            # print(all_headers)
                               
                    print("Finished removing columns")
                    print(f"There are currently {len(all_headers)} columns of data included.")
                    input("press any key to continue...")
                    col_number = 0
                    
                elif (sub_menu_option == 23):
                    # Desribe Columns
                    # input("describing the columns..")
                    clear()
                    
                    printDescribeColMenu(all_headers)
                    col_number = getResponse(printDescribeColMenu, -1, len(all_headers)-1, arg_list=all_headers)
                    if (col_number == -1):
                        col_number = 0
                        continue
                    
                    print("cleaning data...")
                    clean_df = data_frame.dropna(axis = 'index', subset = [all_headers[col_number]])
                    
                    
                    # Clean specific columns in the data frame
                    
                    # clean out 0.0's from lat and long columns
                    if (all_headers[col_number] == 'LAT' or all_headers[col_number] == 'LON'):
                        clean_df = clean_df[clean_df[all_headers[col_number]] != 0]
                        
                    elif (all_headers[col_number] == 'Vict Age'):
                        clean_df = clean_df[clean_df[all_headers[col_number]] > 0]
                        clean_df = clean_df[clean_df[all_headers[col_number]] != 118]
                        # print("should have cleaned neg values from vic age")
                    
                    elif (all_headers[col_number] == 'Vict Sex'):
                        clean_df = clean_df[clean_df[all_headers[col_number]] != 'X']
                        clean_df = clean_df[clean_df[all_headers[col_number]] != 'N']
                        
                    elif (all_headers[col_number] == 'Vict Descent'):
                        clean_df = clean_df[clean_df[all_headers[col_number]] != '-']
                         
                    elif (all_headers[col_number] == 'Date Rptd' or all_headers[col_number] == 'DATE OCC'):
                        # clean_df = pd.to_datetime(clean_df[all_headers[col_number]], format='%m/%d/%Y %I:%M:%S %p')
                        clean_df[all_headers[col_number]] = pd.to_datetime(clean_df[all_headers[col_number]], format="%m/%d/%Y %I:%M:%S %p")
                        # print("made the clean df yo")
                        clean_df[all_headers[col_number]] = pd.to_datetime(clean_df[all_headers[col_number]]).sub(pd.Timestamp('2010-01-01')).dt.days
                    
                    
                    # if mocodes, split mocodes on space and join as one number
                     
                    if (all_headers[col_number] == 'Mocodes'):
                            # split the Mocodes
                        clean_lst = clean_df[all_headers[col_number]].to_list()
                        new_lst = list()
                        for codes in clean_lst:
                            try:
                                new_lst.append(int("".join(codes.split())))
                            except:
                                continue
                        # print(new_lst)                            
                        clean_lst = new_lst
                    else:
                        clean_lst = clean_df[all_headers[col_number]].to_list()
                    
                    # send in a sorted list
                        
                    # clean_sorted_lst = sorted(clean_lst)
                    # just in case we need to use our own sort
                    clean_sorted_lst = sortData(clean_lst, 1)

                    
                    print("done cleaning data...")
                    
                    print(f"{all_headers[col_number]} stats:")
                    print("============================")
                    

                    try:
                        s_time = time.time()
                        
                        if (all_headers[col_number] == 'Date Rptd' or all_headers[col_number] == 'DATE OCC'):
                            describeColumn2(clean_sorted_lst, col_number, data_bools, dtype='date')
                        else:
                            describeColumn2(clean_sorted_lst, col_number, data_bools)
                            
                        e_time = time.time()
                        
                        print("stats printed successfully!")
                        print("Time to process is", (e_time-s_time),"sec.")
                    except:
                        print("stats did not process successfully")
                            
                        print("====== End Print ======")
                        
                        
                        
                        
                    input("Press any key to continue...")
                        
                    continue
                    
                elif (sub_menu_option == 24):
                    # Search Element in Column
                    # input("searching the columns..")
                    clear()
                    printSearchMenu(all_headers)
                    col_number = getResponse(printSearchMenu, -1, len(all_headers)-1, arg_list=all_headers)
                    month = 0
                    day = 0
                    year = 0
                    # year_list = data_frame_bak['year'].to_list()
                    # min_year = int(minFunc(year_list))
                    # max_year = int(maxFunc(year_list))
                    # max_day = None
                    search_ele = None
                    # print("min_year:", min_year, "max_year:", max_year)
                    # input("enter anything")
                    
                    
                    if (col_number == -1):
                        col_number = 0
                        continue
                    
                    if (all_headers[col_number] == 'Date Rptd' or all_headers[col_number] == 'DATE OCC'):
                        # print ("we're looking at a date here mike")
                        printYearPrompt()
                        year = getResponse(printYearPrompt, 1900, 2023)
                        printMonthPrompt()
                        month = getResponse(printMonthPrompt, 1, 12)
                        printDayPrompt()
                        day = getResponse(printDayPrompt, 1, 31)
                        
                        m_str = str(month).rjust(2, '0')
                        d_str = str(day).rjust(2, '0')
                        # print("searching the following string...")
                        # print(m_str + '/' + d_str + '/' + str(year))
                        search_ele = str(m_str + '/' + d_str + '/' + str(year))
                        # print(search_ele)
                    else:
                        search_ele = input("Enter the search value: ")
                    
                    search(data_frame, col_number, search_ele)
                    
                    continue
                
                elif (sub_menu_option == 25):
                    clear()
                    printSortMenu(all_headers)
                    col_number = getResponse(printSortMenu, -1, len(all_headers)-1, arg_list=all_headers)
                    if (col_number == -1):
                        continue
                    printAscDescMenu()
                    sort_type = getResponse(printAscDescMenu, 1, 2)
                    
                    clean_df = data_frame.dropna(axis = 'index', subset = [all_headers[col_number]])
                    
                    if (all_headers[col_number] == 'DATE OCC' or all_headers[col_number] == 'Date Rptd'):
                        try:
                            clean_df[all_headers[col_number]] = pd.to_datetime(clean_df[all_headers[col_number]], format="%m/%d/%Y %I:%M:%S %p")
                        except:
                            print("couldn't format",all_headers[col_number],"as a date")
                            print("attempting to sort without converting...")
                    
                        # split the Mocodes
                    
                    clean_lst = clean_df[all_headers[col_number]].to_list()
                    
                    if (all_headers[col_number] == 'Mocodes'):
                        new_lst = list()
                        for codes in clean_lst:
                            try:
                                new_lst.append(int("".join(codes.split())))
                            except:
                                continue
                        # print(new_lst)                            
                        clean_lst = new_lst
                    
                    sortData(clean_lst, sort_type)
                    writeSort(clean_lst)
                    input("Press any key to continue")
                    continue
                    
                elif (sub_menu_option == 26):
                    # back to the main menu
                    input("Back to the main menu...")
                    
            error_msg = "Data Exploration Section"
            continue
            
        elif (menu_option == 3):
            # Data Analysis
            if (data_frame.empty):
                error_msg = """You haven't loaded any data yet! 
                Select option 1 from the main menu"""
                continue
            
            printDataAnalysis(data_frame_bak)
            
            input("Press any key to continue...")
            continue
        elif (menu_option == 4):
            # Print Data Set
            if (data_frame.empty):
                error_msg = """You haven't loaded any data yet! 
                Select option 1 from the main menu"""
                continue
            clear()
            num_rows = [100, 1000, 5000]
            printMenu()
            sub_menu_option = getResponse(printMenu, -1, 2)
            
            if sub_menu_option != -1:
                print(f"printing {num_rows[sub_menu_option]} number of rows...\n")
                writeDataset(data_frame, num_rows[sub_menu_option]) # TODO
            # print("done printing")
            # print("data also appended to dataout.txt")
            input("Press any key to continue...")
            
            # error_msg = "Print Data Section"
            continue
        
            # Prints specific rows in array:
            # print(data_frame[0:9])
            # print(data_frame.loc[0:9,"DR_NO"])
            # data_frame.to_csv('output.csv',)
            
        
if __name__ == '__main__':
    #os.system('clear')
    clear()
    main()
