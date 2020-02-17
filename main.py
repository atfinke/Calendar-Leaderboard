import utils
import pprint

people = {}
max_name_length = 0

events = utils.fetch_events(days=30)
for calendar in events.keys():
    calendar_events = events[calendar]
    filtered = filter(lambda x: x['name'].startswith('1:1'), calendar_events)
    for event in filtered:
        name = event['name'].replace('1:1 ', '').split(' / ')[0]
        max_name_length = max(max_name_length, len(name))

        duration = (event['end'] - event['start']) / 60 / 60
        people[name] = people.get(name, 0) + duration


result = sorted((value, key) for (key, value) in people.items())
result.reverse()
for index, item in enumerate(result):
    rank = str(index + 1)
    name = item[1]
    print('{}: {} ({} hours)'.format(rank.rjust(2), name.ljust(max_name_length), round(item[0], 1)))
