from pathlib import Path
import re
from collections import defaultdict
import logging 
from logging import basicConfig as basic_config
import sys
import traceback
import json

basic_config(
	level=logging.DEBUG,
	format="%(asctime)s - %(levelname)s - %(message)s - [file: %(filename)s]",
	datefmt='%Y:%m:%d %T',
	style="%",
	encoding='utf-8',
	filename='error.log',
	filemode='a'
)

class Log:
	@staticmethod
	def get_error_details():
		error_type, error_message, error_traceback = sys.exc_info()
		error_name = error_type.__name__
		frames = traceback.extract_tb(error_traceback)
		line_no = next((frame.lineno for frame in reversed(frames) if frame.filename == __file__), frames[-1].lineno)
		return error_name, error_message, line_no
		
	@staticmethod
	def error():
		error_name, error_message, line_no = Log.get_error_details()
		logging.error('%s - %s - [line %s]', error_name, error_message, line_no)

	@staticmethod
	def info(message):
		logging.info('%s', message)
	
	@staticmethod
	def debug(message):
		logging.debug('%s', message)

def get_episode_no(file):
	match = pattern.search(file.stem)
	if match:
		return int(match.group(1))
	return None

def save_trace(file):
	for key in trace:
		trace[key] = list(trace[key])
	with file.open('w', encoding='utf-8') as f:
		json.dump(trace, f, ensure_ascii=False, indent=4)

def rename():
    for file, episode_no in zip(sorted_files, episode_nos):
        if (episode_no and episode_no not in trace[file.suffix]):
            trace[file.suffix].add(episode_no)
            new_file_name = f"Naruto Shippuden - Episode {episode_no:02d}{file.suffix}"
            trace['progress'].add(f"{file.name} -> '{new_file_name}'")
            new_file_path = file_folder / new_file_name
            file.rename(new_file_path)
        else:
            trace['unmodified'].add(file.name)
            continue
     
def status():
    if trace.get('progress'):
        trace['status'].add("successful!")
    else:
        trace['status'].add("failed!")

try:
	file_folder = Path('/home/gifted-24/download/Naruto Shippuden')
	Log.info(f"retrieving files in -> '{file_folder}'")
	files = [file for file in file_folder.iterdir() if file.suffix in {".mp4", ".mkv", ".srt"}]
	pattern = re.compile(r'EP\.(\d+)')
	Log.info("setting [Trace] -> 'a dictionary object to cache certain details'")
	trace = defaultdict(set)
	Log.info(f"sorting files in -> '{file_folder.name}'")
	sorted_files = sorted(files, key=lambda file: get_episode_no(file) or 0)
	Log.info(f"extracting episode no.s from files in -> '{file_folder.name}'")
	episode_nos = map(get_episode_no, sorted_files)
	Log.info("Renaming The files")
	rename()
	status()
	trace_json = Path('trace.json')
	save_trace(trace_json)
	Log.debug(f"[Trace] -> '{trace_json}' -> {trace}")
except:
    Log.error()
   	
	
