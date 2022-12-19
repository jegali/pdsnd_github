import time
import pandas as pd
import numpy as np

# Sources for looking up some functions
# https://de.acervolima.com/wie-kann-der-haufigste-wert-in-einer-pandas-serie-angezeigt-werden/
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.idxmax.html
# https://note.nkmk.me/en/python-pandas-len-shape-size/

# Just a comment for the github project
# for the second commit

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# I created these lists for convenient
# input check and data extraction / conversion
DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

# if the users chooses a single month, we do not need the most common month in evaluation
ALLMONTHS = False

# if the users chooses a single day, we do not need the most common day in evaluation
ALLDAYS = False

def get_filters():
    global ALLMONTHS
    global ALLDAYS

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print()
    print("Starting up bikeshare terminal...")
    print('Hello! Let\'s explore some US bikeshare data!')    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print()
    while True:
        city = input("Please enter one of the following city names or 'X' to exit:\n1) Chicago\n2) New York City\n3) Washington\n[bikeshare]:~$ ")
        city = city.lower()
        if city in CITY_DATA:
            break
        elif city == "x":
            print("Farewell!")
            print()
            exit()
        else:
            print("You entered an invalid city. Please try again.")

    # get user input for month (all, january, february, ... , june)
    print()
    while True:
        month = input("Please enter the month you want to explore the data, 'ALL' for all months or 'X' to exit:\n1) January\n2) February\n3) March\n4) April\n5) May\n6) June\n7) ALL\n[bikeshare]:~$ ")
        month = month.lower()
        if month in MONTHS or month == "all":
            if month == "all":
                ALLMONTHS = True
            break
        elif month == "x":
            print("Farewell!")
            print()
            exit()
        else:
            print("You did a wrong selection. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print()
    while True:
        day = input("Please enter the day you want to explore, 'ALL' for all days or 'X' to exit:\n1) Monday\n2) Tuesday\n3) Wednesday\n4) Thursday\n5) Friday\n6) Saturday\n7) Sunday\n8) ALL\n[bikeshare]:~$ ")
        day = day.lower()
        if day in DAYS or day == "all":
            if day == "all":
                ALLDAYS = True
            break
        elif day == "x":
            print("Farewell!")
            print()
            exit()
        else:
            print("You did a wrong selection. Please try again.")

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # let's read the csv file for the entered city
    df = pd.read_csv(CITY_DATA[city])

    # Values from the CSV file may be wrong datatype,
    # so convert the "Start Time" column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # now get the month, day and hour from the currently created
    # datetime and create new columns in the dataframe
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Washington is missing gender and birth info
    # I decided to add a new column to the data frame containing the city name
    # (a global variable would have worked too...)
    df['city'] = city

    # Now that we've added these columns, 
    # we can filter the data using them
    # filter by month, if applicable
    if month != 'all':
        month_num = MONTHS.index(month) + 1
        df = df[df['month'] == month_num] 

    # filter by day_of_week, if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    # If the user entered "all" as value for month, 
    # we can get the most common month
    # else we only have one month which is the most common automatically
    if ALLMONTHS:
        print("The most common month is " + MONTHS[most_common_month - 1].title())
    else:
        print("We cannot display the most common month since your input was a single month, namely " + MONTHS[most_common_month - 1].title())
    

    # display the most common day of week
    most_common_day = df['day_of_week'].value_counts().idxmax()
    # If the user entered "all" as value for day, 
    # we can get the most common day
    # else we only have one day which is the most common automatically
    if ALLDAYS:
        print("The most common day is " + most_common_day)
    else:
        print("We cannot display the most common day since your input was a single day, namely " +  most_common_day)

    # display the most common start hour
    most_common_starthour = df['hour'].value_counts().idxmax()
    # make the hour format more readable
    print("The most common start hour is " + str(most_common_starthour).zfill(2) + ":00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_startstation = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is " + most_common_startstation)

    # display most commonly used end station
    most_common_endstation = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is " + most_common_endstation)  

    # display most frequent combination of start station and end station trip
    most_common_startendstation = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end stations are {} and {}"\
            .format(most_common_startendstation[0], most_common_startendstation[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration_total = df['Trip Duration'].sum()
    print("Total travel time : ", trip_duration_total)

    # display mean travel time
    trip_duration_mean = df['Trip Duration'].mean()
    print("Mean travel time : ", trip_duration_mean)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here is a list and count of user types:\n")
    user_types = df['User Type'].value_counts()
    
    # iteratively print out the total numbers of user types 
    for index, user_type in enumerate(user_types):
        print("  - {}: {}".format(user_types.index[index], user_type))
    print()

    # We have a little problem with Washington data
    # since it does not contain any gender and birth info,
    # we'll have to skip these if city is washington

    if df['city'].iat[0] == "washington":
        print ("Sorry, we have to skip gender and birth statistics, as these value are not included in the data set")
    else:
        # Display counts of gender
        print("Here is a list and count of gender:\n")
        gender_types = df['Gender'].value_counts()
        
        # iteratively print out the total numbers of genders 
        # basically same as above
        for index,gender_type in enumerate(gender_types):
            print("  - {}: {}".format(gender_types.index[index], gender_type))
        print()

        # Display earliest, most recent, and most common year of birth
        # the most earliest birth year
        print("Now to some statistics on birth date:\n")
        birth_year = df['Birth Year']
        
        earliest_year = birth_year.min()
        print("  - earliest birth year:", earliest_year)
        
        #the most common birth year
        most_common_year = birth_year.value_counts().idxmax()
        print("  - most common birth year:", most_common_year)
        
        # the most recent birth year
        most_recent = birth_year.max()
        print("  - most recent birth year:", most_recent)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_data(df):
    """
    Displays five rows of data from the csv file chosen by the user.
    
    Args:
        df - the data frame to work with
    Returns:
        Nothing
    """
    VALIDINPUT = ['yes,', 'no']
    last_input = ""
    current_page = 0
    page_length = 5   # for faster debugging

    print()
    print("Welcome to the bikeshare raw data browser. Do you want to view the raw data?")

    while last_input not in VALIDINPUT:
        last_input = input("Please enter 'Yes' or 'No':\n[bikeshare]:~$ ")
        last_input = last_input.lower()
        if last_input == "yes":
            # print five lines of raw data
            print(df[current_page:current_page+page_length])
            current_page += page_length
            break
        elif last_input not in VALIDINPUT:
            print("Your input was not recognized. Please try again")

    while last_input == "yes" and current_page < len(df):
        print("Do you wish to see more raw data? ")
        last_input = input("Please enter 'Yes' or 'No':\n[bikeshare]:~$ ")
        last_input = last_input.lower()
        if last_input == "yes":
            # print five lines of raw data
            print(df[current_page:current_page+page_length])
            current_page += page_length
        elif last_input == "no":
            print("Exiting browser...")
            break
        else:
            print("Your input was not recognized. Please try again")
    
    if current_page >= len(df):
        print("End of data file reached. Exiting browser...")
        print()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # this function is used to satisfy the 5 line Raw Data display
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
