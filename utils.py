import json
import objc

from datetime import datetime, timedelta
from dateutil import tz

from CalendarStore import CalCalendarStore, CalEvent, CalTask
from Cocoa import NSDate


CALENDARS = ['NU']


def fetch_events(days):
    store = CalCalendarStore.defaultCalendarStore()
    cals = []
    for cal in store.calendars():
        if cal.title() in CALENDARS:
            cals.append(cal)

    cst = tz.gettz('America/Chicago')
    today = datetime.now().date()
    end_dt = datetime(today.year, today.month, today.day, tzinfo=cst)
    start_dt = end_dt - timedelta(days)

    start_int = int(start_dt.strftime("%s"))
    end_int = int(end_dt.strftime("%s"))
    start = NSDate.dateWithTimeIntervalSince1970_(start_int)
    end = NSDate.dateWithTimeIntervalSince1970_(end_int)

    formatted_results = {}

    for cal in cals:
        events = []
        pred = CalCalendarStore.eventPredicateWithStartDate_endDate_calendars_(start, end, [cal])
        for event in store.eventsWithPredicate_(pred):
            s = event._.startDate.timeIntervalSince1970()
            e = event._.endDate.timeIntervalSince1970()
            events.append({'name': event._.title, 'start': s, 'end': e})
        formatted_results[cal.title()] = events

    return formatted_results
