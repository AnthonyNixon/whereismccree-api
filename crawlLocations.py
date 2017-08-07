import re

#UTC: Tues 3:17 am

with open('times') as data_file:
    data = data_file.readlines()
data_file.close()

print len(data)

timezoneLookup = {}

for line in data:
    line = line.strip('\n')
    m = re.search(r'(.+?)\t(.+?) (\d{1,}):(\d{2}) ([ap]m)', line)
    (city, day, hour, minute, ampm) = m.groups()
    hour = int(hour)
    minute = int(minute)
    if "tue" in day.lower():
        # It's tuesday
        if "pm" in ampm.lower():
            # It's tuesday afternoon. It's ahead of UTC.
            # Just subtract the time after adding 12 to the hour
            if hour < 12:
                hourDiff = int(hour) + 9
            else:
                hourDiff = int(hour) - 3

        else:
            #It's tuesday morning. It's near UTC time.
            if hour == 12:
                hour = 0
            hourDiff = int(hour) - 3
            # print line
            # print hourDiff
            # print "------"

    else:
        # It's monday
        if "am" in ampm.lower():
            # It's monday morning. This shouldn't be possible.
            print line
        else:
            hourDiff = int(hour) - 15


    minuteDiff = int(minute) - 17
    if minuteDiff < 0:
        hourDiff -= 1
        minuteDiff += 60

    print line
    lookupKey = "UTC"
    if hourDiff >= 0:
        lookupKey = lookupKey + "+"

    lookupKey = lookupKey + str(hourDiff)
    lookupKey = lookupKey + "_"

    if minuteDiff == 0:
        minuteDiff = "00"

    lookupKey = lookupKey + str(minuteDiff)

    if lookupKey not in timezoneLookup:
        timezoneLookup[lookupKey] = []

    timezoneLookup[lookupKey].append(city)

    print timezoneLookup

count = 0
for key in timezoneLookup:
    print key
    count += 1
    with open('output/' + key + '.txt', 'w+') as output_file:
        for location in timezoneLookup[key]:
            output_file.write(location + '\n')
    output_file.close()
    # print
    # print timezoneLookup[key]
    # print "------------------------"

print count



# >>> import re
# >>> m = re.search('(?<=abc)def', 'abcdef')
# >>> m.group(0)
# 'def'
