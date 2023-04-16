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

# TODO:
#   - Data Structure for holding whether column vals are strings or floats
#   - this should coincide with the excel spreadsheet as well?



import pandas as pd
import time
import os
import math

def counts(data):
    count = 0
    # loop through data add one per row in data
    for row in data:
        count += 1
    print("Count: " ,  count)

def uniqueCounts(data):

    unique_set = set()
    # loop through data and store if was not previously found
    for unique in data:
        if not pd.isna(unique) and unique not in unique_set:
            unique_set.add(unique)
    print("Unique: " , len(unique_set))

# 
# Standard Deviation and Variance 
def stanDev(data):
    # variables     
    stand_diff = set();
    mean = 0;
    sum_sq = 0;
    var = 0;
    st_dev = 0;

    # Step1: find the mean
    for index in data:
        mean += index
    mean = round(mean / len(data))

    # Step 2: find each deviation of the mean and square then add it to stand_diff list
    for index in data:
        stand_diff.add(math.pow((mean - index), 2))

    # Step3: sum of the stand_diff
    for sum_index in stand_diff:
        sum_sq += sum_index

    # Step 4: variance and sqrt to get stdev   
    var = (round(sum_sq/ (len(data)-1),4))
    st_dev = math.sqrt(var)

    # print statements
    print("Mean: ", mean)
    print("STDEV: ", round(st_dev, 4))
    print("Variance: ", var)
    # had two functions but you need to find the variance to find the stdev, so just merged the
    # two functions

def maxFunc(data):
    #initialize max for string and int/float, plus dict.
    max_num = None
    max_string = None
    string_dict = {}

    for temp in data:
        #made a bool to determine if int/float being used
        int_float = True
        for char in str(temp):
            if char not in ['-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                int_float = False
                break
        #ints/floats are dealt here
        if int_float:
            if max_num is None or temp > max_num:
                max_num = temp
        #strings are dealt here
        #finding max # of instances
        elif not int_float:
            if temp in string_dict:
                string_dict[temp] += 1
            else:
                string_dict[temp] = 1

    #set count to 0
    max_count = 0
    for string, str_count in string_dict.items():
        if str_count > max_count:
            max_count = str_count
            max_string = string

    if max_num is not None:
            print("Maximum: ", max_num)
    else:
            print("Maximum: ", max_string)

def minFunc(data):
    #initialize max for string and int/float, plus dict.
    min_num = None
    minstring = None
    string_dict = {}

    for temp in data:
        #made a bool to determine if int/float being used
        int_float = True
        for char in str(temp):
            if char not in ['-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                int_float = False
                break
        #ints/floats are dealt here
        if int_float:
            if min_num is None or temp < min_num:
                min_num = temp
        #strings are dealt here
        #finding max # of instances
        elif not int_float:
            if temp in string_dict:
                string_dict[temp] += 1
            else:
                string_dict[temp] = 1

    #this count needs to be a big #
    min_count = 1000000000
    for string, str_count in string_dict.items():
        if str_count < min_count:
            min_count = str_count
            min_string = string

    if min_num is not None:
        print("Minimum: ", min_num)
    else:
        print("Minimum: ", min_string)

def totalUniqueCount(data):
    # create an empty dictionary to store unique crime counts per year
    count_by_year = {}

    # loop through each crime data
    for index, row in data.iterrows():
        # saves the year and crime into variables
        year = int(row.year)
        crime_code = row['Crm Cd']
        
        # if the year and crime code combination is already in the dictionary, increment the count
        if (year, crime_code) in count_by_year:
            count_by_year[(year, crime_code)] += 1
        # if the year and crime code combination is not in the dictionary, add it with a count of 1
        else:
            count_by_year[(year, crime_code)] = 1

    # create a new dictionary to store unique crime counts per year, without considering the crime code
    unique_counts_by_year = {}

    # loop through each year and crime code combination in the dictionary
    for (year, crime_code), count in count_by_year.items():
        # if the year is already in the new dictionary, increment the count
        if year in unique_counts_by_year:
            unique_counts_by_year[year] += 1
        # if the year is not in the new dictionary, add it with a count of 1
        else:
            unique_counts_by_year[year] = 1

    # sort the dictionary by value in descending order and return it 0 for year 1 for count
    sorted_counts = sorted(unique_counts_by_year.items(), key=lambda x: x[0], reverse=True)
    for year, count in sorted_counts:
        print(f"{year}: {count} unique crimes")


def countCrimesByArea(data):
    # create an empty dictionary to store crime counts per area
    count_by_area = {}

    # loop through each crime data
    for index, row in data.iterrows():
        # saves the area name and year into variables
        area_name = row['AREA NAME']
        year = int(row.year)
        
        # if the area is already in the dictionary, increment the count
        if area_name in count_by_area:
            # if the year is already in the area dictionary, increment the count
            if year in count_by_area[area_name]:
                count_by_area[area_name][year] += 1
            # if the year is not in the area dictionary, add it with a count of 1
            else:
                count_by_area[area_name][year] = 1
        # if the area is not in the dictionary, add it with a count of 1 for the current year
        else:
            count_by_area[area_name] = {year: 1}

    # create a new dictionary to store the total crime counts by area, without considering the year
    total_counts_by_area = {}

    # loop through each area and year in the dictionary
    for area_name, year_counts in count_by_area.items():
        # compute the total number of crimes for the area
        total_count = sum(year_counts.values())
        
        # add the total count to the new dictionary
        total_counts_by_area[area_name] = total_count

    # sort the dictionary by year and value in descending order and return it
    sorted_counts = sorted(total_counts_by_area.items(), key=lambda x: (x[1], x[0]), reverse=True)
    for area_name, count in sorted_counts[:5]:
        print(f"{area_name}: {count} crimes")


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def getPrintColumns(dframe):
    headers = list(dframe.columns)
    print(headers)

#Time to read and store data in an array

def readFile(file_name="Crime_Data_from_2017_to_2019.csv"):
    # s_time = time.time()
    csv_arr = pd.read_csv(file_name, quotechar='"', delimiter=',', skipinitialspace=True)    
    # e_time = time.time()
    """
    If you want to access elements of csv_array or want to see the whole array use the following:

    Prints the whole csv with the header at the top and row nums on the left side:
    print(csv_arr)

    Prints csv as an array without the header and row nums:
    print(csv_arr.values)

    Prints specific elements in array:
    print(csv_arr.values[1,16])

    Prints elements all elements on column 1 uptil row 4
    print(csv_arr.values[:4,1])

    Note: all null data points are set to NaN by default
    """
    # print("Read time: ", (e_time-s_time), "\n")
    # print(csv_arr)

    return(csv_arr)


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


def sortData(dframe, column_name):
    ''' method for sorting data frame data by passed in column_name'''
    pass

def describeColumn(data_list, col_number):
    # TODO
    counts(data_list)
    uniqueCounts(data_list)
    maxFunc(data_list)
    minFunc(data_list)

    # only call STDEV and Variance when needed
    if (col_number  == 4 or col_number==12 or 27 <= col_number <= 29  ):
        stanDev(data_list);
        # variance(data_list);
    else:
        print ("Standard Deviation: N/A")
        print ("Variance: N/A")


    print(data_list)
    
    pass


def getResponse(foo, min_val, max_val, **kwargs):
    '''Takes in a print function (foo) and tests against minumum
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
            str_response = input("Enter your choice: ")
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
    print("25. Add Back a Dropped Column:")
    print("26. Back to the Main Menu")
        

def printDropHeaders(excl_header_list):
    printHeaders(excl_header_list)
    print("Enter a column number to drop")
    print("Enter -1 to finish entering columns")
    
def printInclHeaders(incl_header_list):
    printHeaders(incl_header_list)
    print("Enter a column number to add")
    print("Enter -1 to finish entering columns")    
   
def printHeaders(header_list):
    for i in range(len(header_list)):
        print(f"[{i}] {header_list[i]}")
    
def printDescribeColMenu(incl_header_list):
    print("Describe Columns:")
    print("*****************")
    print("*****************")
    printHeaders(incl_header_list)
    print("Enter the column number to desribe")
    print("Enter -1 to finish entering columns")    
    
def printSearchMenu(header_list):
    print("Search Element in Column:")
    print("**************************")
    for i in range(len(header_list)):
        print(f"[{i}] {header_list[i]}")   
    print("Select the column number to perform a search")
    print("Enter -1 to finish entering columns")

def printDataAnalysis(df):
    print("Data Analysis:")
    print("***************")
    print("Show the total unique count of crimes per year sorted in descending order:")
    totalUniqueCount(df)
    print(f"\nShow the top 5 areas with the most crime events in all years:")
    countCrimesByArea(df)
    print("\nShow all months and the unique total count of crimes sorted in increasing order.")
    # printMonthsUniqueCrimes(df) # TODO
    print("\nShow the top 10 streets with the most crimes in LA in 2019. Also display the total amount of crimes in each street.")
    # printTop10Streets(df) # TODO
    print("\nShow the top 5 most dangerous times (in hours) to be in Hollywood. Also display the total amount of crimes in each hour.")
    # printTop5HWood(df) # TODO
    print("\nPrint the details of the crime that that took the most time (in hours) to be reported.")
    # printMostTime(df) # TODO
    print("\nShow the 10 top most common crime types (Crm Cd Desc) overall across all years.")
    # printMostCommonCrime(df) # TODO
    print("\nAre woman or men more likely to be the victim of a crime in LA between lunch time (11:00am and 1:00pm)?. Support of your answer.")
    # printLALunchTime(df) # TODO
    print("\nWhat is the month the has the most major credit card frauds (Crm Cd Desc = 'CREDIT CARDS, FRAUD USE ($950 & UNDER')) in LA in 2019.")
    # printCCFrauds(df) # TODO
    print("\nList the top 5 more dangerous areas for older man (age from 65 and more) in december of 2018 in West LA.")
    # printOlderManTop5(df) # TODO
    print(df)

def printMenu():
    print("  Print Menu  :")
    print("***************")
    print(f"\t[0] = first 100 lines")
    print(f"\t[1] = first 1000 lines")
    print(f"\t[2] = first 5000 lines\n")
    print(f"Select how many rows to print")
    print("Enter -1 to go back")


'''Main Logic // Menu loop'''
def main():
    
    menu_option = None
    data_frame = pd.DataFrame()
    error_msg = ""
    included_headers = []
    excluded_headers = []
    all_headers = []
    
    data_bools = [dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #0
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #1
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #2
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #3
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #4
                    
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #5
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #6
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #7
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #8
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #9
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #10
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #11
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #12
                    
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=False, max=False), #13
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=False, max=False), #14
                    
                    dict(count=True, unique_count=True, mean=False, median=True, mode=True, stdev=False, var=False, min=True, max=True), #15
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #16
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #17
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #18
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #19
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #20
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #21
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #22
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #23
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #24
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #25
                    dict(count=True, unique_count=True, mean=False, median=False, mode=True, stdev=False, var=False, min=False, max=False), #26
                    
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #27
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True), #28
                    dict(count=True, unique_count=True, mean=True, median=True, mode=True, stdev=True, var=True, min=True, max=True)] #29
    
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
                data_frame
                e_time = time.time()
                print("[start time]", s_time)
                print("[end time]", e_time)
                print("Time to load:", (e_time-s_time),"sec.")
                included_headers = list(data_frame.columns)
                all_headers = included_headers.copy() # save backup of all column names
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
                    print("*****************")
                    print("Included Columns:")
                    print("*****************")
                    if (len(included_headers) > 0):
                        printHeaders(included_headers)
                    else:
                        print("No columns are currently included")
                    print("*****************")
                    print("*****************")
                    print("Excluded Columns:")
                    print("*****************")
                    if (len(excluded_headers) > 0):
                        printHeaders(excluded_headers)
                    else:
                        print("No columns are currently excluded")
                    print("*****************")
                    print("*****************")
                    input(f"\npress enter to continue...")
                    continue
                    
                elif (sub_menu_option == 22):
                    # Drop Columns
                    #clear()
                    while (col_number != -1):
                        clear()
                        printDropHeaders(included_headers)
                        col_number = getResponse(printDropHeaders, -1, len(included_headers)-1, arg_list=included_headers)
                        # print("col_number now",col_number)
                        
                        if (col_number != -1):
                            excluded_headers.append(included_headers[col_number])
                            # print(f"excluded headers last: {excluded_headers[-1]}")
                            included_headers.remove(included_headers[col_number])
                            print(f"\nColumn {col_number}:\n")
                            print(excluded_headers[-1])
                            input(f"\nwas successfully dropped. Press any key...")
                            
                            # print("included_headers now***")
                            # print(included_headers)
                        
                        
                          
                    print("Finished removing columns")
                    print(f"There are currently {len(excluded_headers)} items being excluded.")
                    input("press any key to continue...")
                    col_number = 0
                    
                elif (sub_menu_option == 23):
                    # Desribe Columns
                    # input("describing the columns..")
                    clear()
                    
                    printDescribeColMenu(included_headers)
                    col_number = getResponse(printDescribeColMenu, -1, len(included_headers)-1, arg_list=included_headers)
                    if (col_number == -1):
                        col_number = 0
                        continue
                    
                    # TODO: function to retrieve all of the stats: describeColumn
                    #  - return dictionary of count, unique, mean, median, mode, stdev, variance, minimum, maximum

                    datalst = data_frame[included_headers[col_number]].to_list()
                    describeColumn(datalst, col_number)
                    
                    print(f"{included_headers[col_number]} stats:")
                    print("============================")

                    try:
                        s_time = time.time()
                        #stats = describeColumn(data_frame, included_headers[col_number]) # TODO
                        e_time = time.time()
                        # printStats(stats) # TODO
                        
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
                    if (col_number == -1):
                        col_number = 0
                        continue
                    
                    search_ele = input("Enter the search value: ")
                    
                    # TODO: Need to make 1:1 list of variable type so that I can 
                    #       check and see if the correct element was input

                    is_found = False
                    s_time = time.time()
                    # should return a bool
                    # is_found = search(data_frame, col_number, search_ele) # TODO: search function
                    e_time = time.time()
                    
                    
                    if (is_found):
                        print("stats printed successfully!")
                        print("Time to process is", (e_time-s_time),"sec.")
                    else:
                        print(f"could not locate (({search_ele})) in the data")
                        print("Total search time was", (e_time-s_time),"sec.")
                    
                    input("Press any key to continue")
                    continue
                    
                elif (sub_menu_option == 25):
                    # add back a dropped column
                    # input("adding back a dropped column...")
                    # Drop Columns
                    clear()
                     
                    if (len(excluded_headers) == 0):
                        print_msg = "There are currently 0 excluded columns so there's none to add back!"
                        continue
                     
                    while (col_number != -1):
                        printInclHeaders(excluded_headers)
                        col_number = getResponse(printInclHeaders, -1, len(excluded_headers)-1, arg_list=excluded_headers)
                        # print("col_number now",col_number)
                        
                        if (col_number != -1):
                            
                            included_headers.append(excluded_headers[col_number])
                            # print(f"included headers last: {included_headers[-1]}")
                            excluded_headers.remove(excluded_headers[col_number])
                            # print("excluded_headers now***")
                            # print(excluded_headers)
                            
                    print("Finished adding back columns")
                    print(f"There are currently {len(excluded_headers)} items still being excluded.")
                    col_number = 0
                    input("press any key to continue...")
                    
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
            
            printDataAnalysis(data_frame)
            
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
            sub_menu_option = getResponse(printMenu, -1, 3)
            
            print(f"printing {num_rows[sub_menu_option]} number of rows...\n")
            # printDataset(data_frame, num_rows) # TODO
            print("done printing")
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
