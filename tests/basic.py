#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # Use local
from anglerfish import *


print("Running anglerfish.make_logger()")
make_logger("test")

print("Running anglerfish.get_config_folder()")
print(get_config_folder("test"))

print("Running anglerfish.set_cli_title()")
set_terminal_title("test")
set_terminal_title("")

print("Running anglerfish.set_single_instance()")
lock = set_single_instance("test")

print("Running anglerfish.set_process_name_and_cpu_priority()")
set_process_name("test")

print("Running anglerfish.make_root_check_and_encoding_debug()")
check_encoding()

print("Running anglerfish.check_working_folder()")
check_folder()

print("Running anglerfish.get_or_set_temp_folder()")
get_temp_folder("test")

print("Running anglerfish.get_clipboard()")
clipboard_copy, clipboard_paste = get_clipboard()  # FIXME
clipboard_copy("42")
print(clipboard_paste())

print("Running anglerfish.beep()")
beep()

print("Running anglerfish.make_config()")
make_config("test")

print("Running anglerfish.backup_config()")
backup_config("test")

print("Running anglerfish.log_exception()")
try:
    0 / 0
except Exception:
    log_exception()


print("Running anglerfish.bytes2human()")
print(bytes2human(3284902384, "g"))
print(bytes2human(0, "m"))
print(bytes2human(6666, "k"))
print(bytes2human(-6666, "k"))
print(bytes2human(1024, "k"))

print("Running anglerfish.get_sanitized_string()")
print(get_sanitized_string("\m/_(>_<)_\m/", "."))
print(get_sanitized_string("╭∩╮_(҂≖̀‿≖́)_╭∩╮"))
print(get_sanitized_string("abcd1234"))
print(get_sanitized_string(""))

print("Running anglerfish.json_pretty()")
print(json_pretty({"foo": True, "bar": 42, "baz": []}))
print(json_pretty({}))

print("Running anglerfish.multiprocessed()")
import time
def process_job(job):  # a simple function for testing only
    time.sleep(1)
    count = 100
    while count > 0:
        count -= 1
    return job
jobs = [str(i) for i in range(30)]  # a simple list
# print(multiprocessed(process_job, jobs, cpu_num=1, thread_num=1))  # SLOW
# print(multiprocessed(process_job, jobs, cpu_num=2, thread_num=2))  # SLOW
print(multiprocessed(process_job, jobs, cpu_num=1, thread_num=4))
print(multiprocessed(process_job, jobs, cpu_num=4, thread_num=1))
print(multiprocessed(process_job, jobs, cpu_num=4, thread_num=6))

print("Running anglerfish.@threads")
@threads(4)
def process_job():  # a simple function for testing only
    return time.sleep(1)
process_job()

#print("Running anglerfish.@retry")
#@retry(4)
#def retry_job():  # a simple function for testing only
#    return open("").read()  # Will Fail as expected
#retry_job()

print("Running anglerfish.walkdir2filelist")
print(walk2list(".", ".py", ".pyc"))


print("Running anglerfish.seconds2human()")
print(seconds2human(0))
print(seconds2human(42))
print(seconds2human(-666))
print(seconds2human(83490890))

print("Running anglerfish.walk2dict()")
print(walk2dict(".", jsony=True))

print("Running anglerfish.@typecheck")
@typecheck
def test_typecheck(foo: int, bar: str) -> float:
    return float(foo)
test_typecheck(42, "test")

print("Running anglerfish.make_post_execution_message()")
make_post_exec_msg(None, "foo")

print("Running anglerfish.TemplatePython()")
demo = """<html><body>
     {%
     def say_hello(arg):
         {{"<tr> hello ", arg, " </tr>"}}
     %}
     <table>
         {% [say_hello(i) for i in range(9) if i % 2] %}
     </table>
     {% {{ testo }} {{ __doc__.title() }} %}
     {% # this is a python comment %}  </body></html>"""
templar_template = TemplatePython(demo)
print(templar_template(testo=9, mini=True))


print("Printing globals() keys...")
print(tuple(sorted(globals().keys())))
