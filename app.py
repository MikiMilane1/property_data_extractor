import datetime

from plotter import plotter
import pandas as pd


def app():
    try:
        df = pd.read_csv('scraped_data.csv')
        df = df.dropna()
    except FileNotFoundError:
        print('The csv file is missing. Please run the scraper first.')
        return None

    # GET THE LIST OF DISTRICTS
    districts_list = df['district'].unique().tolist()

    district_pick = input(f'Please type in a district from the following list and press ENTER {districts_list}\n')
    choice_1 = input(f'To plot the average price for the entire district of {district_pick} type "district" and press ENTER. For a specific location type in "list" and press ENTER.\n')
    if choice_1 == "district":
        location_type = 'district'
        location_name = district_pick
    elif choice_1 == 'list':
        viable_locations = df.loc[(df['district'] == district_pick)]['location'].unique().tolist()
        location_type = 'location'
        print(f'The following is the list of locations for the district of {district_pick}')
        for loc in viable_locations:
            print(loc)
        location_name = input("Please type in a location from the list and press ENTER.\n")
    else:
        print('Invalid input.')
        app()

    lookback_period = int(input('Enter the lookback period in years and press ENTER./n'))
    input_parameters = {'location_type': location_type,
                        'location_name': location_name,
                        'lookback_period': lookback_period
                        }
    # FORMAT DATA
    lookback_date = datetime.datetime.now() - datetime.timedelta(days=lookback_period * 365)

    if input_parameters['location_type'] == 'district':
        df = df.loc[(df['district'] == input_parameters["location_name"])]
        df = df.dropna()
        df = df[['date', 'price']]
        df = df.groupby('date').mean()
        df = df.reset_index(drop=False)
    else:
        df = df.loc[(df['location'] == input_parameters['location_name'])]
        df.dropna()
        df = df[['date', 'price']]
        df = df.reset_index(drop=False)
        df = df.sort_values('date', ascending=True)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.loc[(df['date'] > lookback_date)]

    # RUN PLOTTER
    if location_type == 'district':
        location_name_for_plot = f'{location_name} district'
    else:
        location_name_for_plot = f'{location_name}, district {district_pick}'
    plotter(df=df, location=location_name_for_plot, lookback_period=input_parameters["lookback_period"])


app()
