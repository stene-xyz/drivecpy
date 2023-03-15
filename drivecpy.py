#!/usr/bin/env python3
#    drivecpy - frontend for dd
#    Copyright (C) 2023 stene.xyz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import sys, os, subprocess, json

def print_header():
	os.system("clear")
	print(" ____  ____  __  _  _  ____  ___  ____  _  _ ")
	print("(    \(  _ \(  )/ )( \(  __)/ __)(  _ \( \/ )")
	print(" ) D ( )   / )( \ \/ / ) _)( (__  ) __/ )  / ")
	print("(____/(__\_)(__) \__/ (____)\___)(__)  (__/  ")
	print("version 0.1-alpha    copyright 2023 stene.xyz")
	print("")

print_header()
print("[*] Setting up...")
global drive_list
drive_list = json.loads(subprocess.check_output("lsblk -J", shell=True))
for drive in drive_list["blockdevices"]:
	print("[+] Found device /dev/" + drive["name"])
	print("[ ]     Device size: " + drive["size"])
	try:
		for partition in drive["children"]:
			print("[ ] Partition /dev/" + partition["name"] + ": " + partition["size"])
	except:
		print("[ ]     Drive has no partitions.")

menu = 1
while True:
	try:
		print_header()
		print("Please choose the source device:")
		drives = []
		i = 0
		for drive in drive_list["blockdevices"]:
			print(str(i) + ": " + drive["name"] + ": " + drive["size"] + " drive")
			drives.append(drive)
			i += 1
			if("children" in drive):
				for partition in drive["children"]:
					print(str(i) + ": " + partition["name"] + ": " + partition["size"] + " partition")
					drives.append(partition)
					i += 1
		source = int(input("source? "))
		if(source < len(drives)):
			print_header()
			print("Please choose the target device:")
			drives = []
			i = 0
			for drive in drive_list["blockdevices"]:
				print(str(i) + ": " + drive["name"] + ": " + drive["size"] + " drive")
				drives.append(drive)
				i += 1
				if("children" in drive):
					for partition in drive["children"]:
						print(str(i) + ": " + partition["name"] + ": " + partition["size"] + " partition")
						drives.append(partition)
						i += 1
			target = int(input("target? "))
			if(target < len(drives)):
				print_header()
				print("PLEASE CONFIRM CLONE:")
				print("CLONING DRIVE /dev/" + drives[source]["name"] + " (" + drives[source]["size"] + ") TO DRIVE /dev/" + drives[target]["name"] + "(" + drives[target]["size"] + ")")
				print("DATA ON DRIVE /dev/" + drives[target]["name"] + " WILL BE OVERWRITTEN.")
				print("TYPE \"YES, CONFIRM CLONE\" (CASE-SENSITIVE) TO CONTINUE.")
				confirmation = input("CONFIRM? ")
				if(confirmation == "YES, CONFIRM CLONE"):
					os.system("dd if=/dev/" + drives[source]["name"] + " of=/dev/" + drives[target]["name"] + " bs=1M status=progress")
					print("Done. Press enter to continue.")
					input()
				elif(confirmation == "DEBUG"):
					print("SOURCE:")
					print(drives[source])
					print("TARGET:")
					print(drives[target])
					print("COMMAND:")
					print("dd if=/dev/" + drives[source]["name"] + " of=/dev/" + drives[target]["name"] + " bs=1M status=progress")

					input()
				else:
					print("NOT CONFIRMED.")
					print("Press enter to continue.")
					input()
			else:
				print("Invalid target drive, press enter to continue")
				input()
		else:
			print("Invalid source drive, press enter to continue")
			input()
	except:
		print("There was an error processing your selection.")
		input("Press enter to continue.")
