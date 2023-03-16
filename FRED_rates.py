# Author: 
# Date: 2/10/2023
# Class: CS 361 SE1
# Description: Gets latest mortgage rates from FRED economic data using the FRED API and adjusts it based on credit score.

import requests
from datetime import datetime, timedelta

def get_thursday():
    """ Gets previous thursdays date unless it's thursday then just gets todays date.
    
    Returns:
        thursday (string): The previous thursdays date in YYYY-MM-DD form.
    """
    date = datetime.today()
    week_day = datetime.weekday(date)
    
    difference = week_day - 3
    
    if difference > 0: date = date - timedelta(days=difference) 
    
    elif difference < 0:
        if difference == -1: date = date - timedelta(days=6)
        elif difference == -2: date = date - timedelta(days=5)
        elif difference == -3: date = date - timedelta(days=4)
    
    return date.strftime("%Y-%m-%d")

def get_rate():
    """ Gets rate from FRED economic data using the FRED API based on yesterdays date.

    Returns:
        rate (float): Mortgage rate returned by FRED API.
    """
    
    api_key = "4770e3754f3be27795d598f818719276"
    series_id = "MORTGAGE30US"
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&observation_start={get_thursday()}&file_type=json"
    response = requests.get(url)
    
    data = response.json()
    
    return float(data["observations"][0]["value"])

def adjust_rate(credit_score: int):
    """ Returns mortgage rate adjusted based on credit score.

    Args:
        credit_score (int): Credit score entered by the user.

    Returns:
        rate (float): Mortgage rate adjusted for credit score.
    """
    rate = get_rate()
    
    if 620 <= credit_score <= 639: return rate * 1.20
    elif 640 <= credit_score <= 659: return rate * 1.175
    elif 660 <= credit_score <= 679: return rate * 1.15
    elif 680 <= credit_score <= 699: return rate * 1.125
    elif 700 <= credit_score <= 759: return rate * 1.1
    elif 760 <= credit_score <= 850: return rate * 1.075
    
if __name__ == "__main__":
    print(adjust_rate(630))