# Terrible Time Tracker

Command line tool for tracking time on projects.

Command line based. Works anywhere there is a command line and Python 3 or 2.

Tracks time in a Tab Seperated Value (TSV) file.

Only allows tracking the time of a single in-process task at a time (single user, so you can only work on one task at a time) BUT can track any number of projects/tasks.

Vaguely similar to:

  * https://github.com/PFython/time_is_money
  * https://github.com/FelixTheC/QT-TimeIsMoney

## Features

 * mostly works

## Anti-Features

I.e. TODO items.

  * no summation
  * no nice error messages
  * no zsh/fish autocomplete of project and task names

## Usage

    py -3 time_tracker.py my_project my_task  ## start working on my_task in the my_project
    py -3 time_tracker.py stop  # stop previously started project/task

    py -3 time_tracker.py my_project  # start working on an unamed task in my_project
    py -3 time_tracker.py stop  # stop previously started project/task

Logs to `time_tracker.tsv` in the current directory.

## Alternatives

  * https://github.com/TailorDev/Watson

