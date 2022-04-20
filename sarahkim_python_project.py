import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#define acceptable input lists
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

#project checks:
#prompt the user if they want to see 5 lines of raw data
#display that data if the answer is 'yes'
#continue iterating these prompts/displaying next 5 lines of raw data at each iteration
#stop the program when the user says 'no' or there is no more raw data to display
#hint: use while loop to handle invalid inputs
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello!\nLet\'s explore some US bike-share data!\n')
# TO DO: get user input for CITY (chicago, new york city, washington).
    while True:
        try:
            city = str(input('Please choose a city: Chicago, New York City, or Washington.\n')).lower()
            break
        except ValueError:
            print('Invalid input provided. Please try again using an option from the city list.')
        except KeyboardInterrupt:
            print('No input was received. Please try again.')
            break
        finally:
            print('\nAttempted input: {}'.format(city))
            
    """prevent recursive code """
    while city not in CITY_DATA:
        city = str(input('Invalid city. Please enter your city of choice again.\n'))

# TO DO: get user input for MONTH (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Please choose a month between January and June.\n')).lower()
            break
        except ValueError:
            print('Invalid input provided. Please try again.')
        except KeyboardInterrupt:
            print('No input was received. Please try again.')
            break
        finally:
            print('\nAttempted input: {}'.format(month))
    
    #repeatedly ask user for valid input
    """prevent recursive code """
    while month not in months:
        month = str(input('\nPlease check your input. The month entered is either outside the expected range of input or is misspelled.\n'))

# TO DO: get user input for DAY of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Please enter one day of the week to analyze. Please enter "all" to apply no filter.\n')).lower()
            break
        except ValueError:
            print('Invalid input provided. Please try again.')
        except KeyboardInterrupt:
            print('No input was received. Please try again.')
            break
        finally:
            print('\nAttempted input: {}'.format(day))
            
    """prevent recursive code """
    
    while day not in days:
        day = str(input('\nPlease check your input. The day entered is either outside the expected range of input or is mispelled.\n'))


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1

        #filtered month for new data frame
        df = df[df['month'] == month]

    if day != 'all':
        #filtered day for new data frame
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #use mode to generate most often listed month in the data
    most_common_month = df['month'].mode()[0]
    print('Most common month bikes were rented in the dataset:{}'.format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day bikes were rented in the dataset:{}'.format(most_common_day))

    # TO DO: display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common hour bike rentals started in the dataset:{}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    #filter to new data frame and re-define with relevant stat name
    common_start_stn = df['Start Station'].mode()[0]
    print('Most people rented their bikes starting at station:{}'.format(common_start_stn))

    # TO DO: display most commonly used end station
    common_end_stn = df['End Station'].mode()[0]
    print('Most people ended their bike rental at station:{}'.format(common_end_stn))

    # TO DO: display most frequent combination of start station and end station trip
    #most frequent aka max of the value count for the stations
    start_end_comb = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print('The most frequent combination of start and end stations is:{}'.format(start_end_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time was {} seconds'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time was {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of each user type:\n{}'.format(user_types))

    # TO DO: Display counts of gender
    #exclude Washington since gender is not provided in that dataset
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print('Number of users by gender: \n{}'.format(gender))

    # TO DO: Display earliest, most recent, and most common year of birth
    #exclude Washington since birth year is not provided in that dataset
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year among users: {}'.format(int(earliest_birth_year)))

        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year among users: {}'.format(int(most_recent_birth_year)))

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year among users: {}'.format(int(most_common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_by_request(df):
    """
    Prompt user if they want to see 5 lines of raw data, display that data if the answer
    is 'yes'. Continue iterating prompts and displaying the next 5 lines of raw data at
    each iteration. Stop the program when the user says 'no' or there is no more raw
    data to display. Implements while loop to track progress through iterations.
    """
    i = 0
    raw = input("Would you like to view individual trip data? Please type 'yes' or 'no'.\n").lower()
    pd.set_option('display.max_columns',200)

    while True:
        #run checks on input and increment accordingly
        if raw == 'no':
            break
        elif raw == 'yes':
            #subset/slice dataframe to display next five rows
            print(df.iloc[0+i:i+5])
            raw = input("Would you like to view more individual trip data? Please type 'yes' or 'no'.\n").lower()
            i += 5
        else:
            #catch unexpected input
            raw = input("\nPlease check your input. Only 'yes' or 'no' are accepted values.\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        raw_data_by_request(df)

        restart = input('\nWould you like to restart the interactive program? Enter YES to restart or NO to end.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
