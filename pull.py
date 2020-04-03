#!/usr/bin/python

import os
import shutil
import argparse

VERBOSE = 0
DEGUB	= 0

ITERATIONS = 7
BACKUP_FOLDER = "/home/ubuntu/backups/maskiner/" # where to put backup
CONFIG = "backup_policy.conf"

SCP_USER = "ubuntu@"

#################################

# Pase arguments

parser = argparse.ArgumentParser(prog='pull_backup.py')
parser.add_argument('-d','--debug',dest="debug",help="Turn debug info on",default=False,action="store_true")
parser.add_argument('-v','--verbose',dest="verbose",help="Turn verbosity on", default=False,action="store_true")
parser.add_argument('-c','--config',dest="config",help="Where to find the backup config",metavar="FILE",default=CONFIG)
parser.add_argument('-i','--iterations',dest="iterations",type=int,help="How many backup interations to do",metavar="N",default=7)
parser.add_argument('-b','--backup-directory',dest="backup_folder",help="Where to keep backup files",metavar="FOLDER",default=BACKUP_FOLDER)
arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEGUB = arguments.debug
ITERATIONS = arguments.iterations
BACKUP_FOLDER = arguments.backup_folder
CONFIG = str(arguments.config) # Spesify to be a string.

##################################

# For easy aksess to print in the form of verbose/debug
def verbose(text):
	if VERBOSE :
		print(text)

def debug(text):
	if DEGUB :
		print(text)

verbose("Verbose is enabled")
debug("Debug is enabled")

# Funktionality

# Open and 
verbose("Opening config file: " + CONFIG); 	# Skriver ut fil navnet
with open(CONFIG) as config:				# Open file + give it a file pointer with = "if this works"
	for line in config:						# Reads line by line
		verbose(f"Readline: {line}")		# Prints line read
		configlist = line.split(":")		# Gets the host name, splits stops at ":".
		pathlist = configlist[1].split(",")	# Gets "the other" part split above.
		verbose(f"Host:{configlist[0]}")	# Prints host name
		host = configlist[0]			# Gets host name.



		# Step 0: Check if there is a backup folder, if not make it.
		host_backup_path = BACKUP_FOLDER + host 							# Gets name for the folder
		if not os.path.exists(f"{host_backup_path}"): 	# checks if folder exists
			verbose(f"Creating backup folder {host_backup_path}")			# Prints info
			os.makedirs(host_backup_path)									# Makes folder if not exists


		# Step 1: Remove the oldest folder
		if os.path.isdir(f"{host_backup_path}.{ITERATIONS}"):			# Checks if folder exists
			verbose("Deleting oldest version of backup directory")
			shutil.rmtree(f"{host_backup_path}.{ITERATIONS}")			# rm -r



		# Step 2: Move folder up one step
		for i in range(ITERATIONS -1,0,-1):								# range(start, stop, step)
			if os.path.isdir(f"{host_backup_path}.{i}"):
				verbose(f"Moving {host_backup_path} from {i} to {i+1}")
				shutil.move(f"{host_backup_path}.{i}", f"{host_backup_path}.{i+1}")


		# Step 3: cp -al current folder

		verbose(" Copying main folder with hard links")
		os.system(f"cp -al {host_backup_path} {host_backup_path}.1")		# cp med hardlink, a = prover å beholde eierskal og rettigheter, l = hardlink


		# Step 4: sync current folder from remote server
		verbose("Synchronizing folders")
		for folder in pathlist:
			folder = folder.rstrip()	# Removes invissibl signs --> only "letters" left
			verbose(f"-> {folder}")
			if not os.path.isdir(host_backup_path + folder):
				os.makedirs(host_backup_path + folder)



			os.system(f"rsync -a{'v' if VERBOSE else ''} --delete {SCP_USER}{host}:{folder} {host_backup_path}{folder}")
