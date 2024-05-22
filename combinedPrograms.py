import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


#This first function is for calculating the number of players that login in per day and calculating the changes 
#between days. It requires the data from a json file as a parameter. 
def calculatePlayerCounts(data):

    startDate = datetime(2024, 3, 11).date()
    endDate = datetime(2024, 3, 24).date()

    # Dictionary to store date keys and count values
    playerCountsByDay = {}


    for userId, userData in data['__collections__']['users'].items():
        
        # Set to store unique dates upon which logins occur
        loginDates = set()

        for logEventData in userData['__collections__']['Logins'].values():
            timestamp = int(logEventData['Timestamp']['value']['_seconds'])
            loginDates.add(datetime.utcfromtimestamp(timestamp).date())

        # Updates player counts by day. Goes through the loginDates set, checks it's within range, if it's not an existing key playerCountsByDay it
        # initialises itself to zero. Regardless, then increments by 1
        for loginDate in loginDates:
            if startDate <= loginDate <= endDate:
                if loginDate not in playerCountsByDay:
                    playerCountsByDay[loginDate] = 0
                playerCountsByDay[loginDate] += 1

    dates = list(playerCountsByDay.keys())
    playerCounts = list(playerCountsByDay.values())

    # Sorts the dates and player counts in ascending order of dates
    dates, playerCounts = zip(*sorted(zip(dates, playerCounts)))

    return dates, playerCounts

def calculateAveragePickups(data):
    numberOfUsers = len(data['__collections__']['users'])

    # Dictionary to store date keys and pickup values
    pickupsByDay = {}

    for userId, userData in data['__collections__']['users'].items():
        for pickupId, pickupData in userData['__collections__']['Pickups'].items():
            timestampSeconds = pickupData['2. Timestamp']['value']['_seconds']
            pickupDate = datetime.utcfromtimestamp(timestampSeconds).date()

            if pickupDate not in pickupsByDay:
                pickupsByDay[pickupDate] = 0
            pickupsByDay[pickupDate] += 1

    averagePickupsByDay = {}

    # Works out the date range
    minDate = min(pickupsByDay.keys())
    maxDate = max(pickupsByDay.keys())
    allDates = [minDate + timedelta(days=x) for x in range((maxDate - minDate).days + 1)]

    # Works out average pickups for the day
    for date in allDates:
        if date in pickupsByDay:
            averagePickupsByDay[date] = pickupsByDay[date] / numberOfUsers
        else:
            averagePickupsByDay[date] = 0  # Where no pickups are found

    
    datesAvg = sorted(averagePickupsByDay.keys())
    averagePickups = [averagePickupsByDay[date] for date in datesAvg]

    return datesAvg, averagePickups

def plotCombined(data):
    dates, playerCounts = calculatePlayerCounts(data)
    datesAvg, averagePickups = calculateAveragePickups(data)

    # Works out the change rates
    changeRates = [0]
    for i in range(1, len(playerCounts)):
        changeRate = playerCounts[i] - playerCounts[i - 1]
        changeRates.append(changeRate)

    plt.figure(figsize=(12, 6))

    plt.plot(datesAvg, averagePickups, marker='o', linestyle='-', color='blue', label='Average Pickups per Day')
    plt.xlabel('Date')
    plt.ylabel('Average Number of Pickups')
    plt.title('Average Pickups per Day and Player Counts with Change Rates')

    plt.plot(dates, playerCounts, marker='o', linestyle='-', color='red', label='Player Counts')
    plt.ylabel('Player Count')

    for i in range(len(dates) - 1):
        plt.annotate(f"{changeRates[i+1]}", (dates[i+1], playerCounts[i+1]),
                     textcoords="offset points", xytext=(-10, 10), ha='center')

    plt.xticks(dates, rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(0, max(max(averagePickups), max(playerCounts)) + 1)
    plt.show()

#Load the json file and run
with open('dummyTestData.json', 'r') as f:
    data = json.load(f)
plotCombined(data)
