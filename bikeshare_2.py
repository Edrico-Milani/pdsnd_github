import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #This displays a welcome message and introduces the available Bikeshare city data to the users.
    print('\nHello, and welcome! Let\'s explore some US bikeshare data! \n')
    print('''You can access the Bikeshare data for any of the following US city using its name:
    Chicago\n    New York City\n    Washington''')
    # This section gets user input for city (chicago, new york city, washington). It also uses a while loop and the .lower() method to handle invalid inputs
    while True:
        cities = ['Chicago', 'New York City', 'Washington']
        city = str(input('Please enter a city name (e.g. Chicago) to continue: \n')).lower()
        cities_lower = [item.lower() for item in cities]
        if city.lower() in cities_lower:
            break
        else:
            print('Please enter a valid city from the list provided')
    # This section gets user input for month (January, February, ... , June, all). It also uses a while loop to handle invalid inputs
    print('Bikeshare data is currently available for the following months only:\nJanuary, February, March, April, May, and June \n')
    while True:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'all']
        months_lower = [item.lower() for item in months]
        month = str(input('Please enter a month name to filter by it, or enter "all" for all months: \n'))
        if month.lower() in months_lower:
            break
        else:
            print('Please enter valid month name or enter "all" to see all months')
    # This section gets user input for day of the week (Monday, Tuesday, ... Sunday, all). It also uses a while loop to handle invalid inputs
    print('Bikeshare data is available for all days of the week i.e Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday \n')
    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all']
        days_lower = [item.lower() for item in days]
        day = str(input('Please enter a day to filter by specific day, or enter "all" to show data for all days of the week: \n'))
        if day.lower() in days_lower:
            break
        else:
            print('Please enter a valid day or enter "all" to see data for all days')

    print('-' * 40)
    return(city, month, day)

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
    df = pd.read_csv(CITY_DATA[city])                        # This reads the city column index of the csv files from the dictionary created above
    df['Start Time'] = pd.to_datetime(df['Start Time'])      # This converts the 'Start Time' column index to_datetime, and allow extracting its data
    df['month'] = df['Start Time'].dt.month_name()           # Creates a df['month'] column index with extracted month_name() from df['Start Time'] column
    df['day_of_week'] = df['Start Time'].dt.day_name()       # Creates a df['day_of_week'] column index with extracted day_name() from df['Start Time'] column

    if month.lower() != 'all':
        df = df[df['month'] == month.title()]

    if day.lower() != 'all':                                 # This searches the text content in a case-insensitive way and then implements the if command
        df = df[df['day_of_week'] == day.title()]            # The command to execute if user enters a day instead of text variable content
    return df                                                # Returns the function df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculations on The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # This displays the most popular month users engage in bike trips
    if month.lower() == 'all':
        popular_month = df['month'].mode()[0]
        print('The most frequent travel month is: ',popular_month)
    # This displays the most popular day of week users take trips
    if day.lower() == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('The most frequent travel day of the week is: ', popular_day)
    # This displays the most popular start hour for users trips
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    print('The most frequent travel start time is {}:00 hrs '.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculations on The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # This displays the most popularly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most frequently used start station is: ',popular_start_station)
    # This displays the most popularly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most frequently used end station is: ',popular_end_station)
    # This displays the most popular combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' ' + 'to' + ' ' + df['End Station']
    popular_combination = df['combination'].mode()[0]
    print('The most frequent trip with the same combination of start station and end station is: {}'.format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculations on Trip Duration...\n')
    start_time = time.time()
    # This displays the total travel time in hours, minutes and seconds
    total_travel_time = df['Trip Duration'].sum()
    minute,second = divmod(total_travel_time, 60)
    hour,minute = divmod(minute, 60)
    print('The total time traveled is: {} hour(s) {} minute(s) {} second(s): '.format(hour, minute, second))

    # This displays the average (mean) travel time
    average_travel_time = round(df['Trip Duration'].mean())
    min,sec = divmod(average_travel_time, 60)
    if min > 60:
        hr, min = divmod(min, 60)
        print('The average or mean travel time is: {} hour(s) {} minute(s) {} second(s)'.format(hr, min, sec))
    else:
        print('The average or mean travel time is: {} minute(s) {} second(s)'.format(min, sec))

    # This displays the maximum trip duration
    max_travel_time = round(df['Trip Duration'].max())
    minute,second = divmod(max_travel_time, 60)
    hour,minute = divmod(minute, 60)
    print('The maximum trip duration is: {} hour(s) {} minute(s) {} second(s): '.format(hour, minute, second))

    # This displays the minimum trip duration
    min_travel_time = round(df['Trip Duration'].min())
    minute, second = divmod(min_travel_time, 60)
    hour, minute = divmod(minute, 60)
    print('The minimum trip duration is: {} hour(s) {} minute(s) {} second(s): '.format(hour, minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculations on User Stats...\n')
    start_time = time.time()

    # This displays the counts of user types based on each category
    user_type_count = df['User Type'].value_counts()
    print('The total number of users by categories are: \n',user_type_count)

    # This displays the counts of gender (i.e male count and female count)
    while True:
        if city == 'washington'.lower():
            break
        else:
            gender_count = df['Gender'].value_counts()
            print('The total number of users by gender are: \n',gender_count)
            print('\n')
            break

    # This displays the earliest (oldest) birth year, most recent (newest) birth year, and the most common (popular) year of birth.
    while True:
        if city == 'washington'.lower():
            break
        else:
            earliest_birth_yr = int(df['Birth Year'].min())
            print('The earliest or oldest birth year is: ', earliest_birth_yr)
            newest_birth_yr = int(df['Birth Year'].max())
            print('The most recent or newest birth year is: ', newest_birth_yr)
            frequent_birth_yr = int(df['Birth Year'].mode()[0])
            print('The most frequent birth year is: ', frequent_birth_yr)
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_stats(df):
    """ Asks user to specify whether or not they would like to view trip data 5-entries per time, view more data or not """

    while True:
        possible_responses =['yes', 'no']
        user_response = input('Would you like to view 5 entries of trip raw data per time? Please enter "yes" or "no":\n').lower()
        if user_response in possible_responses:
            if user_response == 'yes':
                start = 0
                stop = 5
                trip_data = df.iloc[start:stop, :9]
                print(trip_data)
            break
        else:
            print('Please enter a valid response')
    if user_response == 'yes':
        while True:
            user_response_2 = input('Would you like to view more entries of the trip raw data? Please enter "yes" or "no":\n').lower()
            if user_response_2 in possible_responses:
                if user_response_2 == 'yes':
                    start += 5
                    stop += 5
                    trip_data = df.iloc[start:stop, :9]
                    print(trip_data)
                else:
                    break
            else:
                print('Please enter a valid response')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
#Link to Project Bikeshare Github repository
print('For more information, please visit: https://github.com/Edrico-Milani/psdnd_github')

if __name__ == "__main__":
	main()