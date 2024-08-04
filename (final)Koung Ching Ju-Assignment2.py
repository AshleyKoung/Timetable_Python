#
# File: (final)Koung Ching Ju-Assignment2
# Author: Koung Ching Ju
# Student ID: 110394176
# Email ID: Koucy013
# This is my own work as defined by
#  the University's Academic Misconduct Policy.
#


def timetable_header():
    print("Weekly Personal timetable")
    print("Author: Koung Ching Ju")
    print("UniSA Email: koucy013@mymail.unisa.edu.au")


def menu():
    print("Menu:")
    print("+"+"-"*35+"+")
    print("1. Create a scheduled event")
    print("2. Update a scheduled event")
    print("3. Delete a scheduled event")
    print("4. Print the whole week's timetable")
    print("5. Print events on a specific day")
    print("6. Print events as keyword")
    print("7. Save timetable to a file")
    print("8. Load timetable from a file")
    print("9. Quit")
    print("+"+"-"*35+"+")

#Define time format
standard_input_day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
standard_time = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
events = {}  #Create event dictionary


def is_overlapping(events, day, start, end):
    """Check if the given time range overlaps with any existing events on the day."""
    # Convert to 24-hour format for easy comparison
    def to_24_hour(time):
        if 'am' in time:
            return int(time[:-2]) if time[:-2] != "12" else 0
        else:
            return int(time[:-2]) + 12 if time[:-2] != "12" else 12

    start = to_24_hour(start)
    end = to_24_hour(end)

    if day in events:
        for event in events[day]:
            existing_start, existing_end = event['time'].split('-')

            # Convert to 24-hour format for easy comparison
            existing_start = to_24_hour(existing_start)
            existing_end = to_24_hour(existing_end)

            if (existing_start < end and existing_end > start):
                print("Time slot is already taken. Please choose another time.")
                return True
    return False


def create_event():
    print("Let's create a new event:")
    input_title = input("Enter the title of the event: ")
    input_day = input("Event day (e.g., Mon): ").capitalize()

    if input_day not in standard_input_day:
        print("Invalid input_day format. Event creation failed.")
        return
    
    input_time = input("Enter the time interval for the event (e.g., 9am-10am): ")

    if not "-" in input_time:
        print("Invalid time interval format. Please enter the time interval as 'start-end' (e.g., 9am-10am). Event creation failed.")
        return
    
    start, end = input_time.split("-")
    
    if start not in standard_time or end not in standard_time:
        print("Out of time range. The time only can between 9am and 5pm (e.g., 9am-10am).")
        return
    
    # Check for time overlap
    if is_overlapping(events, input_day, start, end):
        """Use the overlapping function to check whether it is repeated with events in the dictionary"""
        return
   
    input_where = input("Enter the location: ")

    # Check if the event already exists.
    if input_day in events:
        for event in events[input_day]:
            if event['time'] == input_time:
                print("Event already exists.")
                return
              
    event_details={
        'title': input_title,
        'day': input_day,
        'time': input_time,
        'location': input_where
    }
    if input_day not in events:
        events[input_day] = []

    """Add the events in the events dictionary to the title name set in the event_details dictionary"""
    events[input_day].append(event_details)
    print(f"Title: {input_title}\nDay: {input_day}\nTime: {input_time}\nLocation: {input_where}\n{'Event created successfully!'}")


def update_event():
    standard_input_day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    standard_time = ['9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm']  

    search_option = input("Would you like to search by day and start time or by keyword? (Enter 'time' or 'keyword'): ")

    if search_option not in ['time', 'keyword']:
        print("Invalid option. Update failed.")
        return

    found_events = []

    if search_option == 'time':
        input_day = input("Please enter the day of the week (Mon-Sun) to update an event: ").capitalize()
        input_start_time = input("Please enter the original start time of the event (e.g., 9am): ")

        if input_day not in standard_input_day or input_start_time not in standard_time:
            print("Invalid format. Update failed.")
            return

        if input_day in events:
            for event in events[input_day]:
                start, _ = event['time'].split("-")
                if start == input_start_time:
                    found_events.append((input_day, event))

    else:
        keyword = input("Please enter a keyword (event title) to search for the event: ")

        for day, day_events in events.items():
            for event in day_events:
                if keyword.lower() in event['title'].lower():
                    found_events.append((day, event))

    if not found_events:
        print("Event not found.")
        return

    if len(found_events) == 1:
        day_to_update, event_to_update = found_events[0]

    else:
        print("Multiple events found. Please select the event to update:")
        for i, (day, event) in enumerate(found_events, 1):
            print(f"{i}. Day: {day}, Title: {event['title']}, Time: {event['time']}, Location: {event['location']}")

        choice = int(input("Enter the number of the event you want to update: "))

        if choice > 0 and choice <= len(found_events):
            day_to_update, event_to_update = found_events[choice - 1]
        else:
            print("Invalid choice. Update canceled.")
            return

    print(f"Event found. Details:")
    print(f"Title: {event_to_update['title']}")
    print(f"Day: {event_to_update['day']}")
    print(f"Time: {event_to_update['time']}")
    print(f"Location: {event_to_update['location']}")

    update_choice = input("Do you want to update this event? (y/n): ").lower()

    if update_choice == 'y':
        new_title = input(f"Enter the updated event title (press Enter to keep '{event_to_update['title']}'): ")
        new_day = input(f"Enter the updated event day (press Enter to keep '{day_to_update}'): ")
        new_time = input(f"Enter the updated event time (press Enter to keep '{event_to_update['time']}'): ")
        new_location = input(f"Enter the updated event location (press Enter to keep '{event_to_update['location']}'): ")

        # Check for time overlap
        new_day_to_check = new_day if new_day else day_to_update
        new_start, new_end = new_time.split("-") if new_time else event_to_update['time'].split("-")
        if is_overlapping(events, new_day_to_check, new_start, new_end):
            print("Update failed due to time overlap.")
            return

        # Remove the event from its original day.
        events[day_to_update].remove(event_to_update)

        # Update the event details.
        event_to_update['title'] = new_title if new_title else event_to_update['title']
        event_to_update['day'] = new_day if new_day else day_to_update
        event_to_update['time'] = new_time if new_time else event_to_update['time']
        event_to_update['location'] = new_location if new_location else event_to_update['location']

        # Add the event to the new day.
        if new_day and new_day not in events:
            events[new_day] = []

        events[new_day if new_day else day_to_update].append(event_to_update)

        print("Event updated successfully.")
    else:
        print("Event not updated.")



def delete_event():
    search_option = input("Would you like to search by start time or keyword? (Enter 'time' or 'keyword'): ").lower()
    
    if search_option not in ['time', 'keyword']:
        print("Invalid option. Deletion failed.")
        return
    
    found_events = []

    if search_option == 'time':
        input_day = input("Please enter the day of the week (Mon-Sun) to delete an event: ").capitalize()

        if input_day not in standard_input_day:
            print("Invalid day format. Deletion failed.")
            return

        input_start_time = input("Please enter the original start time of the event to delete (e.g., 9am): ")

        if input_start_time not in standard_time:
            print("Invalid start time format. Deletion failed.")
            return

        if input_day in events:
            for event in events[input_day]:
                start, _ = event['time'].split("-")
                if start == input_start_time:
                    found_events.append((input_day, event))

    else:  # keyword search
        keyword = input("Please enter a keyword (event title) to search for the event to delete: ")
        
        for day, day_events in events.items():
            for event in day_events:
                if keyword.lower() in event['title'].lower():
                    found_events.append((day, event))

    if found_events:
        print("Events found:")
        for i, (day, event) in enumerate(found_events, 1):
            print(f"{i}. Day: {day}, Title: {event['title']}, Time: {event['time']}, Location: {event['location']}")
        
        choice = int(input("Enter the number of the event you want to delete: "))
        
        if choice > 0 and choice <= len(found_events):
            day_to_delete, event_to_delete = found_events[choice - 1]
            events[day_to_delete].remove(event_to_delete)
            print("Event deleted successfully.")
        else:
            print("Invalid choice. Event not deleted.")
    else:
        print("Event not found.")


#Search the schedule using keyword
def search_events():
    keyword = input("Enter a keyword to search for events: ").lower()
    matching_events = []

    # Define a mapping of days to their numerical values
    day_to_number = {
        'Mon': 1,
        'Tue': 2,
        'Wed': 3,
        'Thu': 4,
        'Fri': 5,
        'Sat': 6,
        'Sun': 7
    }

    for day, events_list in events.items():
        for event in events_list:
            if keyword in event['title'].lower() or keyword in event['location'].lower():
                event_with_day = event.copy()
                event_with_day['day'] = day
                matching_events.append(event_with_day)

    if matching_events:
        # Sort matching_events by 'day' using the custom key
        matching_events.sort(key=lambda x: (day_to_number[x['day']]))
        print("Matching Events:")
        print("+------------------+------------------+--------------------------------+----------------------+")
        print("|      Day         |      Time        |             Title              |      Location        |")
        print("+------------------+------------------+--------------------------------+----------------------+")
        for event in matching_events:
            print(f"| {event['day'].ljust(16)} | {event['time'].ljust(16)} | {event['title'].ljust(30)} | {event['location'].ljust(20)} |")
            print("+------------------+------------------+--------------------------------+----------------------+")
    else:
        print("No matching events found.")




#Print the whole week schedule like a calendar
def print_timetable():
    print(f"{'': <8}", end='')  # Leave space for white space in the upper left corner
    for day in standard_input_day:
        print(f"{day: <25}", end='')  #Print the name of each week
    print()

    for time in standard_time:
        print(f"{time: <8}", end='')  # Print Time
        for day in standard_input_day:
            event_str = ''
            if day in events:
                for event in events[day]:
                    start_time, _ = event['time'].split('-')
                    if start_time == time:
                        short_title = event['title'][:3]  # Get first 3 characters of the title
                        short_location = event['location'][:3]  # Get first 3 characters of the location
                        event_str = f"{short_title}/{short_location}/{event['time']}"
            print(f"{event_str: <25}", end='')  
        print()



#Print events at a specific time
def print_special_day():
    input_day = input("Enter the day of the week (Mon-Sun) to print events for: ").capitalize()

    if input_day not in standard_input_day:
        print("Invalid day format. Printing failed.")
        return

    if input_day in events:
        day_events = events[input_day]
        if day_events:
            print(f"Events for {input_day}:")
            print("+------------------+--------------------------------+----------------------+")
            print("|      Time        |             Title              |      Location        |")
            print("+------------------+--------------------------------+----------------------+")
            for event in day_events:
                print(f"| {event['time'].ljust(16)} | {event['title'].ljust(30)} | {event['location'].ljust(20)} |")
                print("+------------------+--------------------------------+----------------------+")
        else:
            print(f"No events found for {input_day}.")
    else:
        print(f"No events found for {input_day}.")



#Save the schedule to the specified file
def save_file():
    filename = input("Enter the filename to save the timetable: ")
    try:
        file = open(filename, 'w')
        for day, events_list in events.items():
            for event in events_list:
                file.write(f"{event['day']},{event['time']},{event['title']},{event['location']}\n")
        file.close()
        print(f"Timetable saved to {filename} successfully.")
    except IOError:
        print("Error: Unable to save the timetable.")



#Load the specified file to this schedule
def load_file():
    filename = input("Enter the filename to load the timetable from: ")
    new_events = {}  # Used to store new events loaded from fileˇ

    try:
        file = open(filename, 'r')
        for line in file:
            day, time, title, location = line.strip().split(",")
            if day not in new_events:
                new_events[day] = []

            new_events[day].append({
                'day': day,
                'time': time,
                'title': title,
                'location': location
            })

        # Add new events to the existing schedule that do not overlap with the existing schedule
        overlapping_events = []  # Used to store overlapping events
        for day, day_events in new_events.items():
            if day not in events:
                events[day] = []
            for event in day_events:
                start_time, end_time = event['time'].split('-')
                if not is_overlapping(events, day, start_time, end_time):
                    events[day].append(event)
                else:
                    overlapping_events.append(f"Day: {day}\nTime: {event['time']}\nTitle: {event['title']}\nLocation: {event['location']}")

        print("+" + "-" * 55 + "+")
        print(f"Timetable loaded from {filename} successfully.")

        # When the loaded event overlaps with an event in the existing schedule, print out the overlapping event details
        if overlapping_events:
            print("However, the following events overlap with the existing schedule and will not be added to the schedule:")
            print("+" + "-" * 105 + "+")
            for event in overlapping_events:
                print(event)
                print("+" + "-" * 105 + "+")

        file.close() 
    except IOError:
        print(f"Error: Unable to load timetable from {filename}.")




def main():
    """Main function to run at start."""
    timetable_header() 

    command = ''
    while command != '9':
        menu() 
        command = input("Enter your option (1-9): ")

        if command == '1':
            create_event()
        elif command == '2':
            update_event()
        elif command == '3':
            delete_event()
        elif command == '4':
            print_timetable()
        elif command == '5':
            print_special_day()
        elif command == '6':
            search_events()            
        elif command == '7':
            save_file()
        elif command == '8':
            load_file() 
        else:
             print("Not among the provided options, try again!")
    print("Good bye!")

main()