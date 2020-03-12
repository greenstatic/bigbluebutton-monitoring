import logging
from collections import OrderedDict
from urllib.parse import urlparse

import api_lib
import settings


def get_meetings():
    data = api_lib.getMeetings(settings.API_CLIENT)

    if data is None:
        return []

    if data['response']['meetings'] is None:
        return []

    meetings = []
    try:
        meetings = data['response']['meetings']['meeting']
    except KeyError:
        logging.warning("Failed to parse meetings")
    except TypeError:
        return []

    response = []

    for meeting in meetings:
        if type(meeting) != OrderedDict:
            continue

        moderators = []

        if type(meeting['attendees']) == OrderedDict:
            if type(meeting['attendees']['attendee']) == list:
                for attendee in meeting['attendees']['attendee']:
                    if attendee['role'].lower() == "moderator":
                        moderators.append(attendee['fullName'])

            else:
                attendee = meeting['attendees']['attendee']
                if attendee['role'].lower() == 'moderator':
                    moderators.append(attendee['fullName'])

        response.append({
            "name": meeting['meetingName'],
            "id": meeting['meetingID'],
            "creation": meeting['createDate'],
            "recording": meeting['recording'],
            "noUsers": meeting['listenerCount'],
            "moderators": moderators
        })

    return response


def get_server():
    url_parsed = urlparse(settings.API_BASE_URL)

    return {"server": url_parsed.netloc, "api": settings.API_BASE_URL}
