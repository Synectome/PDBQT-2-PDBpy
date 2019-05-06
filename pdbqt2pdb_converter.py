###########################################
#####   PDBQT -> PDB file converter   #####
#####  Neoventures Biotechnology Inc. #####
#####     Jesse Bourret-Gheysen       #####
#####         May 6th 2019            #####
###########################################

import re
import os
import time
from os.path import isfile, join

print('''########################################################################
########################################################################
####                _ _           _                                 ####
####               | | |         | |                                ####
####      _ __   __| | |__   __ _| |_      NeoVentures              ####
####     | '_ \ / _` | '_ \ / _` | __|     Biotechnology Inc.       ####
####     | |_) | (_| | |_) | (_| | |_      2019                     ####
####     | .__/ \__,_|_.__/ \__, |\__|                              ####
####     | |                   | |         Jesse Bourret-Gheysen    ####
####     |_|_              _ _ |_|                                  ####
####     |__ \            | | |                                     ####
####        ) |  _ __   __| | |__                                   ####
####       / /  | '_ \ / _` | '_ \                                  ####
####      / /_  | |_) | (_| | |_) |                                 ####
####     |____| | .__/ \__,_|_.__/      _                           ####
####            | |                    | |                          ####
####       ___ _|_| _ ____   _____ _ __| |_ ___ _ __                ####
####      / __/ _ \| '_ \ \ / / _ | '__| __/ _ | '__|               ####
####     | (_| (_) | | | \ V |  __| |  | ||  __| |                  ####
####      \___\___/|_| |_|\_/ \___|_|   \__\___|_|                  ####
####                                                                ####
########################################################################
########################################################################''')

time.sleep(2)

print('''This program converts pdbqt files into pdb files by splitting
the individual models into seperate files, while also adding in the
receptor model to these files so the receptor and ligand can be seen
together in their respective docking conformations.

To use this program, make sure that the executable is in the same directory as
both the receptor and output pdbqt files that you wish to use. ''')
time.sleep(1)
print(".")
time.sleep(1)
print("..")
time.sleep(1)
print("...")



#pdb file writing function
def pdb_writer(pdb, pdb_num):
    '''function which pulls a pdb from the pdb dictionary
    and writes it to an independantly labeled file'''
    pdb_name = pdbqt_file_name[:-6] + ".0" + str(pdb_num) + ".pdb"
    pdb_file = open(pdb_name, "a+")
    for line in pdb:
        pdb_file.write(line)
    pdb_file.write("  \n")
    pdb_file.close()
    return pdb_name

#Current working directory
cwd = os.getcwd()

#list pdbqt files in cwd
list_of_pdbqts = []
for f in os.listdir(cwd):
    if isfile(join(cwd, f)) and bool(re.search('pdbqt$|PDBQT$', f)):
        list_of_pdbqts.append(f)
print(list_of_pdbqts)
print("  ")

#enter the name of the desired file (pdbqt to split up)
pdbqt_file_name = str(input("please enter the pdbqt file name(no extension)"))
print("  ")

#list pdb files in cwd, so that the receptor can be selected
list_of_pdbs = []
for f in os.listdir(cwd):
    if isfile(join(cwd, f)) and bool(re.search('pdb$|PDB$', f)):
        list_of_pdbs.append(f)
print(list_of_pdbs)
print("  ")

#enter the name of the desired file (pdb receptor)
print("""Please enter the name of the pdb file listed above corresponding
to the receptor for the current pdbqt file""")
receptor_file_name = str(input("pdb receptor name (no extension): "))
print("  ")

#appends the file extension if its missing for the pdbqt
if pdbqt_file_name[-6:] != ".pdbqt" or pdbqt_file_name[-6:] != ".PDBQT":
    pdbqt_file_name += ".PDBQT"

#appends the file extension if its missing for the pdb
if receptor_file_name[-4:] != ".pdbqt" or receptor_file_name[-4:] != ".PDBQT":
    receptor_file_name += ".PDB"

#open file into this var
pdbqt_file = open(pdbqt_file_name, "r")

#a list, a dict, and a var
pdb_list = []
count = 0
pdb_dictionary = {}

#pump and and dump pdb's
for line in pdbqt_file:
    if not re.match("ENDMDL", line):
        pdb_list.append(line)
    else:
        count += 1
        pdb_dictionary[str(count)] = pdb_list
        pdb_list = []

pdbqt_file.close()

#open the receptor file
#receptor_file = open(receptor_file_name, "r")

list_of_pdb_names = []
for k, v in pdb_dictionary.items():
    list_of_pdb_names.append(pdb_writer(v, k))

#concatenate the output pdb's with the receptor pdb file
#the receptor file is read and then written into the pdb out file
for pdb_file in list_of_pdb_names:
    pdb_file_new = "recp_" + pdb_file
    with open(pdb_file_new, 'w') as outfile:
        with open(pdb_file) as infile:
            outfile.write(infile.read())
        with open(receptor_file_name) as infile:
            outfile.write(infile.read())
    os.remove(pdb_file)


print('Program complete, thank you.')