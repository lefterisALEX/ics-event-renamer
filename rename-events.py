import requests
from ics import Calendar, Event
import os

OUTPUT_ICS_FILE = "short_titles_calendar.ics"


def rename_title(original_title):
    if not original_title or not original_title.strip():
        return "Standby"
    first_word = original_title.split()[0]
    return f"{first_word} Standby"


def main():
    ORIGINAL_ICS_URL = os.environ.get("ICS_URL")
    if not ORIGINAL_ICS_URL:
        raise Exception("ICS_URL environment variable is not set!")
    print("Downloading original calendar...")
    response = requests.get(ORIGINAL_ICS_URL)
    response.raise_for_status()
    original_calendar = Calendar(response.text)

    new_calendar = Calendar()
    for event in original_calendar.events:
        new_event = Event()
        new_event.name = rename_title(event.name)
        new_event.begin = event.begin
        new_event.end = event.end
        new_event.description = event.description
        new_event.location = event.location
        new_event.url = event.url
        new_calendar.events.add(new_event)

    with open(OUTPUT_ICS_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_calendar.serialize_iter())

    print(f"New ICS file created: {OUTPUT_ICS_FILE}")


if __name__ == "__main__":
    main()
