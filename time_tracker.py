#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Time tracking to a TSV file.

Only one activity can be active at anyone time.
This is a single user tool, you can not run two activities at the same time.
Currently missing time calcs and cleanly formatted timestamps (millisecs accuracy really not needed)
"""

import datetime
import os
import sys


# TODO pick up from calender builtin?
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

def find_first_day_of_week(the_date, which_day=MONDAY):
    """Given the_date which is the first `which_day` of that week?
    NOTE weeks start on SUNDAY
    """
    # where the_date is datetime/date
    offset = which_day - the_date.weekday()
    if offset < 0:
        offset += 7  # SUNDAY + 1
    return the_date + datetime.timedelta(offset)

OUTPUT_FILE = "time_tracker.tsv"
HEADERS = '\t'.join(["TASK", "SUB-TASK", "START-TIME", "END-TIME", "HOURS"]) + '\n'
UNNAMED_SUB_TASK = 'unnamed'  # TODO consider upper case?

now = datetime.datetime.now()
first_day_of_week = find_first_day_of_week(now, which_day=MONDAY)  # assume work week starts on monday

def create_tsv_if_needed(output_file=OUTPUT_FILE):
    if not os.path.exists(output_file):
        with open(output_file, "w") as file:
            file.write(HEADERS)


# TODO consider using csv module
def read_file(input_file=OUTPUT_FILE):
    with open(input_file, "r") as file:
        lines = file.readlines()  # NOTE includes trailing newline
    return lines

# TODO append_file()
def write_file(lines, output_file=OUTPUT_FILE):
    # NOTE lines need to include newline
    with open(output_file, "w") as file:
        #file.write(HEADERS) Assumes header in lines
        for line in lines:
            file.write(line)


def doit(argv):
    task_filename = OUTPUT_FILE

    create_tsv_if_needed()  # FIXME filename param
    lines = read_file()  # FIXME filename param
    first_line = lines[0]
    last_line = lines[-1]
    print(first_line)
    print(last_line)
    if first_line != HEADERS:
        raise NotImplementedError('first line does not have expected header, %r have %r' % (HEADERS, first_line))

    # TODO handle argv processing
    # TODO argv report totals
    # TODO argv force hour (re-)calc?

    """
    if first_line == last_line:
        raise NotImplementedError('no content in file')
    """

    first_argument = argv[1]  # TODO handle missing

    if first_argument.upper() == 'STOP':
        # sanity check there is already a started task, can ONLY have one started task at a time
        if first_line == last_line:
            raise NotImplementedError('no content in file')
        print('Got: %r' % last_line)
        task_entry = last_line.replace('\n', '').split('\t')
        if len(task_entry) != 3:
            raise NotImplementedError('Possible user error, no start time or there is already a stop time')
        task, sub_task, start_time = task_entry
        stop_time = now
        # TODO hours calc
        task_entry = [task, sub_task, start_time, str(stop_time)]  # FIXME now/stop_time to string...
        last_line = '\t'.join(task_entry) + '\n'
        lines[-1] = last_line
        write_file(lines)  # FIXME filename param
        #raise NotImplementedError('')
    else:
        # Assume want to START a (new) activity/task
        task = first_argument
        try:
            sub_task = argv[2]
        except IndexError:
            sub_task = UNNAMED_SUB_TASK
        # check there is NOT an already active task/activity 
        if first_line == last_line == HEADERS:
            # handle empty file (bar header)
            # can start new task
            with open(task_filename, "a") as file:
                file.write('\t'.join([task, sub_task, str(now)]) + '\n')  # FIXME now to string...
        else:
            # non-empty
            # ensure there isn't an already started entry
            task_entry = last_line.split('\t')  # FIXME refactor - code duplication with STOP
            if len(task_entry) == 3:
                raise NotImplementedError('Probable user error, already have an in progress task')
            # TODO code duplicaton for file IO
            with open(task_filename, "a") as file:
                file.write('\t'.join([task, sub_task, str(now)]) + '\n')  # FIXME now to string...

def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version.replace('\n', ' '), sys.platform.replace('\n', ' ')))

    doit(argv)

    return 0


if __name__ == "__main__":
    sys.exit(main())
