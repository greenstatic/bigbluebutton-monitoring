import logging
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlparse

import xmltodict

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
        if type(data['response']['meetings']['meeting']) == list:
            meetings = data['response']['meetings']['meeting']
        else:
            meetings.append(data['response']['meetings']['meeting'])
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

        origin_server = None
        try:
            origin_server = meeting['metadata']['bbb-origin-server-name']
        except KeyError:
            logging.debug("BBB origin server name does not exist for meeting")
            logging.debug("Setting BBB origin as the server itself")
            origin_server = urlparse(settings.API_BASE_URL).netloc

        m = {
            "name": meeting['meetingName'],
            "id": meeting['meetingID'],
            "creation": meeting['createDate'],
            "noUsers": meeting['participantCount'],
            "moderators": moderators,
            "metadata": {
                "origin-server": origin_server,
            }
        }

        # bbb-context is optional in bbb response
        try:
            m['metadata']['origin-context'] = _bbb_context_convert_moodle(meeting['metadata']['bbb-context'])
        except KeyError:
            pass

        response.append(m)

    return response


def _bbb_context_convert_moodle(context_html):
    """
        Returns the first inner node string from the context html string (useful for the context string returned
        by the BigBlueButton Moodle plugin.
    """

    context_html = "<root>{}</root>".format(context_html)  # removes the bug where there is no root node in context_html
    return_str = ""

    try:
        root = xmltodict.parse(context_html)

        if type(root['root']) == str:
            # No XML contents, just plain old string
            return root['root']

        for element in root['root']:
            el = root['root'][element]
            if type(el) == list and len(el) > 0:
                return_str = el[0]['#text']
                break
    except Exception as e:
        logging.error("Failed to parse BBB context string from Moodle, error: " + str(e))

    return return_str


def get_server():
    url_parsed = urlparse(settings.API_BASE_URL)

    return {
        "service": "bigbluebutton-monitoring",
        "server": url_parsed.netloc,
        "api": settings.API_BASE_URL,
        "version": settings.VERSION,
        "datetime": datetime.now().isoformat(),
        "source": "https://github.com/greenstatic/bigbluebutton-monitoring"}
