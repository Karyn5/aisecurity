
"""

"log.py"

MySQL logging handling.

"""

import time
import warnings

import mysql.connector

from extras.paths import Paths

# SETUP
THRESHOLDS = {
  "num_recognized": 3,
  "num_unrecognized": 25,
  "percent_diff": 0.2,
  "cooldown": 10,
  "time_since_previous": 3
}

num_recognized = 0
num_unrecognized = 0
current_log = {}
unrec_last_logged = time.time()
rec_last_logged = time.time()

try:
  database = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="Blast314" if "ryan" in Paths.HOME else "KittyCat123",
      database="LOG"
      )
  cursor = database.cursor()
except mysql.connector.errors.DatabaseError:
  warnings.warn("Database credentials missing or incorrect")

# LOGGING INIT AND HELPERS
def init(flush=False):
  cursor.execute("USE LOG;")
  database.commit()

  if flush:
    instructions = open(Paths.HOME + "/logs/drop.sql", "r")
    for cmd in instructions:
      if not cmd.startswith(" ") and not cmd.startswith("*/") and not cmd.startswith("/*"): # allows for docstrings
        cursor.execute(cmd)
        database.commit()

def get_now(seconds):
  date_and_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))
  return date_and_time.split(" ")

def get_id(name):
  # will be filled in later
  return "00000"

def get_percent_diff(best_match):
  return 1.0 - (len(current_log[best_match]) / len([item for sublist in current_log.values() for item in sublist]))

def update_current_logs(is_recognized, best_match, now):
  if is_recognized:
    global current_log, num_recognized, num_unrecognized

    if best_match not in current_log:
      current_log[best_match] = [now]
    else:
      current_log[best_match].append(now)

    if len(current_log[best_match]) == 1 or get_percent_diff(best_match) <= THRESHOLDS["percent_diff"]:
      num_recognized += 1
      num_unrecognized = 0
    else:
      num_unrecognized += 1
      num_recognized = 0

# LOGGING FUNCTIONS
def log_person(student_name, times):
  add = "INSERT INTO Transactions (student_id, student_name, date, time) VALUES ({}, '{}', '{}', '{}');".format(
    get_id(student_name), student_name, *get_now(sum(times) / len(times)))
  cursor.execute(add)
  database.commit()

  flush_current()

def log_suspicious(path_to_img):
  add = "INSERT INTO Suspicious (path_to_img, date, time) VALUES ('{}', '{}', '{}');".format(
    path_to_img, *get_now(time.time()))
  cursor.execute(add)
  database.commit()

  flush_current(is_recognized=False)

def flush_current(is_recognized=True):
  if is_recognized:
    global current_log, num_recognized, rec_last_logged
    current_log = {}
    num_recognized = 0
    rec_last_logged = time.time()
  else:
    global num_unrecognized, unrec_last_logged
    num_unrecognized = 0
    unrec_last_logged = time.time()
