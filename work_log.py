import csv
import datetime
import re
import os


def main_menu():
    """Initial menu that the rest of the program runs off of"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
            "Main Menu \n"
            "========= \n"
            "1) Add Entry \n"
            "2) Search Log \n"
            "0) Quit \n"
        )
        # get input from user, and then use it to navigate menu
        select = input('> ')
        # ends program
        if select == '0':
            break
        # adds a new entry
        elif select == '1':
            add_entry()
        # searches through log.csv, leads to search menu
        elif select == '2':
            search_menu()

def add_entry():
    """Adds entry to log.csv, by calling various other functions"""
    # entry to write into log.csv
    entry = []
    os.system('cls' if os.name == 'nt' else 'clear')
    entry.append(add_date())
    entry.append(add_task())
    entry.append(add_time_spent())
    entry.append(add_note())
    # open log.csv, and write the entry to it
    with open('log.csv', 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(entry)
    input('press any key to continue')
    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

def add_date():
    """checks for valid date, and if valid, adds to the entry,
    otherwise asks for date again, until satisfied"""
    while True:
        date = input('Date completed (MM/DD/YY): ')
        # check for valid date, and return date if valid
        try:
            datetime.datetime.strptime(date, '%m/%d/%y')
            return date
        except ValueError as err:
            print(err)

def add_time_spent():
    """checks for valid time, and if valid, adds to the entry,
    otherwise asks for time again, until satisfied"""
    while True:
        time = input('Time spent on task (in rounded minutes): ')
        # check for valid time, and return time if valid
        try:
            re.match(r'[\d]*', time)
            return time
        except ValueError:
            print('please input a valid integer number of minutes')

def add_task():
    """adds task to entry"""
    task = input('Input task name: ')
    return task

def add_note():
    """adds an optional note to the entry"""
    note = input('Input note if desired (optional): ')
    if note == '':
        # adds in the string 'none' so that regex can search csv
        note = 'none'
    return note

def search_menu():
    """menu called from main menu, to choose search option"""
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        # search menu to print
        print(
            "Search Menu \n"
            "========= \n"
            "1) Date Search \n"
            "2) Task Search \n"
            "3) Duration Search \n"
            "4) RegEx Search \n"
            "0) To Main \n"
        )
        # get user input, use to navigate menu
        select = input('> ')
        # returns to main menu
        if select == '0':
            break
        # leads to search by date input
        elif select == '1':
            search_date()
        # leads to search by task name
        elif select == '2':
            search_task()
        # leads to search by time spent
        elif select == '3':
            search_time()
        # leads to search by regular expression
        elif select == '4':
            search_regex()

def search_date():
    """requests search date, and then searches through log.csv for date"""
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        date = input(
            'Date of task \n'
            '(0 to return) \n'
            'input date in format MM/DD/YY: '
        )
        os.system('cls' if os.name == 'nt' else 'clear')
        # returns to search menu
        if date == '0':
            return
        # try date, and if valid, search through log.csv for date
        try:
            datetime.datetime.strptime(date, '%m/%d/%y')
            break
        except ValueError as err:
            print(err)
    # open file and search through it, returning results
    with open('log.csv', encoding = 'utf-8') as open_log:
        log = open_log.read()
        pat = re.compile(r'''
                        (?P<date>{}),
                        (?P<name>[\w'@#+=_?<>!& ]*),
                        (?P<time>[\w ]*),
                        (?P<note>[\w'@#+=_?<>!& ]*)
                        '''.format(date), re.X
                        )
        # if there are no results print message
        if not pat.search(log):
            input('Sorry, no results for that search. Any key to continue')
        # iterate through search results
        for line in pat.finditer(log):
            print(
                "\n\nTask Name: {}\n"
                "Date: {}\n"
                "Time Spent: {} minutes\n"
                "Notes: {}\n"
                .format(line['name'],line['date'],line['time'],line['note'])
            )
            input('press any key for next entry \n')
            os.system('cls' if os.name == 'nt' else 'clear')

def search_time():
    """requests time length to search for, and then searches through 
    log.csv for that time"""
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        time = input(
            'Time spent on task \n'
            '(0 to return) \n'
            'input time in rounded minutes:'
        )
        os.system('cls' if os.name == 'nt' else 'clear')
        # back to search menu
        if time == '0':
            return
        # check for valid time, and if valid, move forward
        try:
            re.match(r'[\d]*', time)
            break
        except ValueError:
            print('please input a valid integer number of minutes')
    # open log.csv and search through it for time checked above
    with open('log.csv', encoding = 'utf-8') as open_log:
        log = open_log.read()
        pat = re.compile(r'''
                        (?P<date>[\d/]*),
                        (?P<name>[\w'@#+=_?<>!& ]*),
                        (?P<time>{}),
                        (?P<note>[\w'@#+=_?<>!& ]*)
                        '''.format(time), re.X
                        )
        # if no search results, print message
        if not pat.search(log):
            input('Sorry, no results for that search. Any key to continue')
        # iterate through results, printing out
        for line in pat.finditer(log):
            print(
                "\n\nTask Name: {}\n"
                "Date: {}\n"
                "Time Spent: {} minutes\n"
                "Notes: {}\n"
                .format(line['name'],line['date'],line['time'],line['note'])
            )
            input('press any key for next entry \n')
            os.system('cls' if os.name == 'nt' else 'clear')

def search_task():
    """asks for task to search through log.csv for, and searches"""
    os.system('cls' if os.name == 'nt' else 'clear')
    # get user input
    name = input(
        'Name of task \n'
        '(0 to return)\n'
        'input Name of Task: '
    )
    os.system('cls' if os.name == 'nt' else 'clear')
    # return to search menu
    if name == '0':
        return
    # open file and search through it
    with open('log.csv', encoding = 'utf-8') as open_log:
        log = open_log.read()
        pat = re.compile(r'''
                        (?P<date>[\d/]*),
                        (?P<name>{}),
                        (?P<time>[\w ]*),
                        (?P<note>[\w'@#+=_?<>!& ]*)
                        '''.format(name), re.X
                        )
        # if not results, print message
        if not pat.search(log):
            input('Sorry, no results for that search. Any key to continue')
        # iterate through results, printing them out
        for line in pat.finditer(log):
            print(
                "\n\nTask Name: {}\n"
                "Date: {}\n"
                "Time Spent: {} minutes\n"
                "Notes: {}\n"
                .format(line['name'],line['date'],line['time'],line['note'])
            )
            input('press any key for next entry \n')
            os.system('cls' if os.name == 'nt' else 'clear')

def search_regex():
    """requests regex from user, and search through log.csv"""
    os.system('cls' if os.name == 'nt' else 'clear')
    # get users regex
    reg = input(
        'Regular Expression \n'
        '(0 to return)\n' 
        'input RegEx to search: '
    )
    os.system('cls' if os.name == 'nt' else 'clear')
    # return to search menu
    if reg == '0':
        return
    # users regex to search with
    pat = re.compile(r'{}'.format(reg))
    # regex used to fill out search display
    pat2 = re.compile(r'''
                    (?P<date>[\d/]*),
                    (?P<name>[\w'@#+=_?<>!& ]*),
                    (?P<time>[\w ]*),
                    (?P<note>[\w'@#+=_?<>!& ]*)
                    ''', re.X)
    # open file and search with users regex
    open_log = open('log.csv', encoding = 'utf-8')
    for line in open_log:
        if pat.search(line):
            ret = pat2.search(line)
            print(
            "\n\nTask Name: {}\n"
            "Date: {}\n"
            "Time Spent: {} minutes\n"
            "Notes: {}\n"
            .format(ret['name'],ret['date'],ret['time'],ret['note'])
            )
            input('press any key for next entry \n')
            os.system('cls' if os.name == 'nt' else 'clear')
    # close file
    open_log.close()

# run program if called
if __name__ == "__main__":
    main_menu()