# preprocessor.py

import re
import pandas as pd

def preprocess(data):
    # Improved regex pattern to match different date formats (with/without seconds, AM/PM)
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?\]'
    
    # Replace non-breaking spaces with regular spaces
    data = data.replace('\u202f', ' ')  
    
    # Split data into messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Raise an error if there is a mismatch between the number of messages and dates extracted
    if len(messages) != len(dates):
        raise ValueError(f"Mismatch between the number of messages ({len(messages)}) and dates ({len(dates)}). Please check the data format.")

    # Create a DataFrame to store messages and corresponding dates
    df = pd.DataFrame({'user_msg': messages, 'msg_date': dates})

    # Normalize the date format by removing the brackets
    df['msg_date'] = df['msg_date'].str.strip('[]')

    # List of possible date formats
    date_formats = [
        '%d/%m/%y, %I:%M:%S %p', '%m/%d/%y, %I:%M:%S %p',
        '%d/%m/%Y, %I:%M:%S %p', '%m/%d/%Y, %I:%M:%S %p',
        '%d/%m/%y, %I:%M %p', '%m/%d/%y, %I:%M %p',
        '%d/%m/%Y, %I:%M %p', '%m/%d/%Y, %I:%M %p',
        '%d/%m/%y, %H:%M', '%m/%d/%y, %H:%M',
        '%d/%m/%Y, %H:%M', '%m/%d/%Y, %H:%M'
    ]

    # Attempt to parse the dates into a standard datetime format
    parsed_dates = pd.to_datetime(df['msg_date'], format=date_formats[0], errors='coerce')
    for fmt in date_formats[1:]:
        parsed_dates = parsed_dates.combine_first(pd.to_datetime(df['msg_date'], format=fmt, errors='coerce'))

    # Assign parsed dates back to the DataFrame
    df['date'] = parsed_dates

    # Check if all dates are NaN, and raise an error if so
    if df['date'].isna().all():
        raise ValueError("No valid dates found in the provided data. Please check the date format.")

    # Initialize lists to hold users and messages separately
    users = []
    messages = []
    for message in df['user_msg']:
        # Split each message into user and message content
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # Assign the extracted users and messages back to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Clean and format the data for analysis
    df.drop(columns=['user_msg', 'msg_date'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.strftime('%B')
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['period'] = df['hour'].apply(lambda x: f'{x:02d}:00-{x+1:02d}:00')
    
    return df
