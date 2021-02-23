import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['jan', 'feb', 'march', 'april', 'may', 'june','aug','nov','oct','dec']
days = ['mon', 'tu', 'wed', 'th', 'fri', 'sat','sun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    flg = True
    while(flg):
        try:
            # get user input for city (chicago, new york city, washington).
            city = input("Enter the name of the city you are intersted in 'Chicago,New York City,Washington':\n").lower()
            city = CITY_DATA[city]
            # get user input for month (all, january, february, ... , june)
            month = input("Enter the name of the month you want to filter {} or all:\n".format(months)).lower()
            if month != 'all':
                month = months.index(month)
            # get user input for day of week (all, monday, tuesday, ... sunday) 
            day = input("Enter the name of the day you want to filter {} or all:\n".format(days)).lower()
            if day != 'all':
                day = days.index(day)
            flg = False
        except:
            print("Invalid input please input name form the list provided!!!")        

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
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x:x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x:x.dayofweek)
    # extract hour from the Start Time column to create an hour column
    df['hour'] =df['Start Time'].apply(lambda x:x.hour)

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month']==month]#+1]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]
    
    #check that there are records for that filters
    if(len(df)):
        return df
    else:
        print("There are no Records for this spcifications.")
        main()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    popular_Mon = df['month'].mode()[0]
    print('Most Frequent Start Month:', months[popular_Mon])

    # display the most common day of week
    popular_Day = df['day_of_week'].mode()[0]
    print('Most Frequent Start Day:', days[popular_Day])

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_st_station = df['Start Station'].mode()[0]
    print('Most Frequent Start station:', popular_st_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df["Start - End"] = df["Start Station"] + " - " +df["End Station"]
    popular_st_en_station = df["Start - End"].mode()[0]
    print('Most Frequent combination of start and end station:', popular_st_en_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travil time is:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The Avrage travil time is:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # print value counts for each user type
    user_types = df["User Type"].value_counts()
    print("We have\n{} Subscriber\t{} Customer".format(user_types[0],user_types[1]))
    fig = go.Figure(data=[go.Bar(y=df["User Type"].value_counts(),x=['Subscriber','Customer'])],
                        layout_title_text="A Figure of Males vs Females number")
    fig.show()
    try: #As Washington has no gender or birth day data
        # Display counts of gender
        # print value counts for each user type
        user_gender = df["Gender"].value_counts()
        print("We have\n{} Male\t{} Female".format(user_gender[0],user_gender[1]))
        fig2 = go.Figure(data=[go.Bar(y=df["Gender"].value_counts(),x=['M','F'])],
                        layout_title_text="A Figure of Males vs Females number")
        fig2.show()
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df["Birth Year"].min())
        recent_birth_year = int(df["Birth Year"].max())
        common_birth_year = int(df["Birth Year"].mode()[0])
        print('''The oldest traviler born on {}\nThe youngest traviler born on {}\nThe most of Travilers born on {}'''.format(earliest_birth_year,recent_birth_year,common_birth_year))
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    ''' Displays for the user the records 5 by 5 until he stop it '''
    
    print('\nDisplaying the filtered Records...\n')
    start_time = time.time()

    # ask the user if he want to see the records 
    view_data = input('\nWould you like to see 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == "yes" or view_data == "y"):
        # Visulizting the important data in the records for the user into table
        try: # As Washington has no gender or birth day data
            fig = go.Figure(data=[go.Table(
                        header=dict(values=['Start Time','End Time','Trip Duration','Start - End','User Type', 'Gender', 'Birth Year'],
                        fill_color='paleturquoise'),
                        cells=dict(values=[df['Start Time'][start_loc:start_loc+5],df['End Time'][start_loc:start_loc+5],df['Trip Duration'][start_loc:start_loc+5],df['Start - End'][start_loc:start_loc+5],df['User Type'][start_loc:start_loc+5], df['Gender'][start_loc:start_loc+5], df['Birth Year'][start_loc:start_loc+5]],
                        fill_color='lavender'))
                        ])
        except:
            fig = go.Figure(data=[go.Table(
                        header=dict(values=['Start Time','End Time','Trip Duration','Start - End','User Type'],
                        fill_color='paleturquoise'),
                        cells=dict(values=[df['Start Time'][start_loc:start_loc+5],df['End Time'][start_loc:start_loc+5],df['Trip Duration'][start_loc:start_loc+5],df['Start - End'][start_loc:start_loc+5],df['User Type'][start_loc:start_loc+5]],
                        fill_color='lavender'))
                        ])
        fig.show()
        # print the row data for the user 
        print(df.head(start_loc+5))
        start_loc += 5
        #update the value by asking the user if he want to show more 5 records
        view_data = input("Do you wish to continue? yes or no\n").lower()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
