from csv import reader
from munkres import Munkres, print_matrix
import argparse

# Cost pertaining to assignments can be modified in the dictionary below.
COSTS = {
    'Preferred': 1,
    'Available but not preferred': 5,
    'Conflict': 100
}

# The TAs below will each be assigned 2 slots/labs.
TAs_WITH_TWO_LABS = (
    #    'tarasov1@msu.edu',
    #    'castrog4@msu.edu',
)


def open_file(filename):
    """
    :param filename:
    :return file pointer:
    """
    try:
        fp = open(filename)
        return fp
    except IOError:
        print("File not found {}".format(filename))


def assistants_and_slots(fp):
    """
    :param fp:
    :return: timeslots, preference_dictionary
    """
    csvreader = reader(fp)
    headerline = next(csvreader, None)
    timeslots = list(headerline[2:])
    timeslots.extend(timeslots[-5:])  # Repeating the last 5 slots on Friday for Wilson

    preference_dictionary = {}

    for line in csvreader:
        assistant = line[1]

        for preferred in line[2:]:
            if assistant in preference_dictionary:
                preference_dictionary[assistant].append(COSTS[preferred])
            else:
                preference_dictionary[assistant] = [COSTS[preferred]]
        if assistant in TAs_WITH_TWO_LABS:
            preference_dictionary[assistant + "*"] = preference_dictionary[assistant]
        preference_dictionary[assistant].extend(preference_dictionary[assistant][-5:])
        # Repeating the last 5 slots on Friday for Wilson
    return timeslots, preference_dictionary


def build_cost_matrix(preference_dictionary):
    """
    :param preference_dictionary:
    :return cost_matrix:
    """
    cost_matrix = []
    for costs in preference_dictionary.values():
        cost_matrix.append(costs)
    return cost_matrix


def main():
    BANNER = '''
    ████████╗██╗  ██╗███████╗                                                  
    ╚══██╔══╝██║  ██║██╔════╝                                                  
       ██║   ███████║█████╗                                                    
       ██║   ██╔══██║██╔══╝                                                    
       ██║   ██║  ██║███████╗                                                  
       ╚═╝   ╚═╝  ╚═╝╚══════╝              -v1.0 by @amirootyet                                   
                                                                               
     █████╗ ██╗     ██╗      ██████╗  ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
    ██╔══██╗██║     ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    ███████║██║     ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝
    ██╔══██║██║     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
    ██║  ██║███████╗███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═                                            
    '''
    print(BANNER)
    ########################################
    # Arguments to the command-line utility
    parser = argparse.ArgumentParser(
        description='A utility to manage CSE 231 TA assignment with the Munkres algorithm.')
    parser.add_argument("-a", "--assign", help='Read the preferences CSV and create assignments.', action='store_true')
    parser.add_argument("-b", "--busybees", help="Find TAs that have a conflict for more than half"
                                                 "of the total work slots.", action='store_true')
    parser.add_argument("-f", "--filename", required=True, help="CSV file containing TA preferences.")
    parser.add_argument("-c", "--costmatrix", help="Build and display the TA cost matrix.", action='store_true')
    args = parser.parse_args()
    #########################################

    fp = open_file(args.filename)  # Attempt to open the CSV file with TA preferences.
    time_slots, preference_dictionary = assistants_and_slots(fp)  # Read time slots and preferences
    assistants = list(preference_dictionary.keys())  # Create a list of available TAs

    # Show the "busy bees"; these TAs make optimal assignment challenging.
    if args.busybees:
        busy_bees = []
        for assistant, costs in preference_dictionary.items():
            conflicts = costs.count(COSTS['Conflict'])  # Count the conflicts for each TA.
            if conflicts > (len(costs)) / 2:  # If the TA has more conflicts than half of the total slots.
                busy_bees.append((assistant, conflicts))
        print("-" * 40)
        print("{:<20} {} (/{})".format('Busy Bee', 'Conflicts', len(costs)))
        print("-" * 40)
        for busy_bee in busy_bees:
            print("{:<20} {}".format(busy_bee[0], busy_bee[1]))

    # Build and show the cost matrix.
    elif args.costmatrix:
        cost_matrix = build_cost_matrix(preference_dictionary)  # Build the cost matrix.
        print_matrix(cost_matrix)  # Display the cost matrix.

    # Assign TAs the time slots / labs.
    elif args.assign:
        cost_matrix = build_cost_matrix(preference_dictionary)
        munkres_obj = Munkres()
        total = 0
        indexes = munkres_obj.compute(cost_matrix)  # This is where the assignment magic happens.
        print('{:<17s} | {:<25s} -> {:<4s}'.format('TAs', 'Assignment', 'Cost'))
        print("-" * 55)
        for row, col in indexes:
            cost = cost_matrix[row][col]
            total += cost  # Calculate total cost of assignment.
            print('{:<17s} | {:<25s} -> {:<4d}'.format(assistants[row], time_slots[col],
                                                       cost))  # Display the assignment result.
        for k, v in COSTS.items():
            print(str(k) + " = " + str(v), sep="")

    fp.close()  # Close the CSV file before exit.


if __name__ == '__main__':
    main()
