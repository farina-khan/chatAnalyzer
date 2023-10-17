import re
import pandas as pd


def preprocess(data):
    pattern = '\\[\\d{1,2}/\\d{1,2}/\\d{2,4},\\s\\d{1,2}:\\d{1,2}:\\d{2,4}\\s[APM]{2}\\]\\s'

    messages = re.split(pattern, data)[1:]
    #  dates = re.findall(pattern, data)
    date = re.findall('\\d{1,2}/\\d{1,2}/\\d{2,4}', data)
    time = re.findall('\\d{1,2}:\\d{1,2}:\\d{2,4}\\s[APM]{2}', data)

    df = pd.DataFrame({'User_Messages': messages, 'Date': date, 'Time': time})

    # Convert the 'date' column to a datetime data type
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')

    # Format the 'date' column as 'YYYY-MM-DD' and assign it back to the DataFrame
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    df.rename(columns={'Message_Date': 'Date'}, inplace=True)


    # Combine date and time columns into a single datetime column
    df['Date_and_Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    df['Day'] = df['Date_and_Time'].dt.day_name()

    # Extract the month number
    df['Month_Number'] = df['Date_and_Time'].dt.month

    # Create a 'year' column
    df['Year'] = df['Date_and_Time'].dt.year

    # Create a 'month_name' column
    df['Month'] = df['Date_and_Time'].dt.strftime('%B')


    users = []

    msgs = []

    for message in df['User_Messages']:
        entry = re.split('^(.+?):\\s', message)
        if entry[1:]:  # username
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['User'] = users
    df['Message'] = msgs
    df.drop(columns=['User_Messages'], inplace=True)

    # Convert 'time' column to datetime with 12-hour format
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M:%S %p')

    # Format 'time' column in 24-hour format
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

    # Split the 'time' column into 'hour', 'minute', and 'second' columns
    df[['Hour', 'Minute', 'Second']] = df['Time'].str.split(':', expand=True)

    # Convert the columns to integers
    df['Hour'] = df['Hour'].astype(int)
    df['Minute'] = df['Minute'].astype(int)
    df['Second'] = df['Second'].astype(int)

    period = []

    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(hour) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period

    return df
