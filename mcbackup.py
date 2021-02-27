import os
from codecs import open
from shutil import copytree, make_archive, rmtree
from datetime import datetime
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.validation import Validator, ValidationError

def main(mc_path, dest):
    print("welcome to mc backup.")

    class WorldValidator(Validator):
        def validate(self, document):
            text = document.text
            if text and text not in worlds:
                raise ValidationError(message="this world doesen't exist", cursor_position=text.__len__())


    worlds = os.listdir(mc_path)
    bull = chr(8226)

    world_completer = WordCompleter(worlds,ignore_case=True,)
    wrld = prompt("what world do you want to backup? (tab for options): ",completer=world_completer,validator=WorldValidator(),complete_while_typing=True,validate_while_typing=False)
    wrldpath = "{}\\{}".format(mc_path, wrld)
    print(bull +" selected world '{}' in '{}'".format(wrld, wrldpath))

    folder_name = "## Autobackup for {} ##".format(wrld)
    if not os.path.isdir("{}\\{}".format(dest, folder_name)):
        os.mkdir("{}\\{}".format(dest, folder_name))
        print("{} created directory '{}' in backup folder".format(bull,folder_name))

    message = input("add anything to the backup zip name? (blank if no): ")

    now = datetime.now()
    time = "_{}_m{}.d{}_{};{};{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2), str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2))
    new = wrld + "_" + message[0:40] + time

    #copy the dir from original save directory to the backup destination
    copytree(wrldpath, "{}\\{}\\{}".format(dest, folder_name, new))
    print("{} backed up world '{}' to '{}\\{}'".format(bull, wrld, folder_name, new))

    #zip the folder in the backup directory
    print("{} zipping '{}.zip'...".format(bull, new))
    zip = "{}\\{}\\{}".format(dest,folder_name,new)
    make_archive(zip, 'zip', wrldpath)

    #delete the folder in the backup directory after zip is successful
    print("{} cleaning up...".format(bull))
    rmtree(zip)
    print("done. backup successful.")

    os.system('pause')

def generateconfig():
    print("config file 'mcbackup_config.txt' not found.")
    mc_path_candidate = input("enter the path to your minecraft 'saves' folder: ").replace("/", "\\")
    if not os.path.isdir(mc_path_candidate):
        print("path either not a directory or doesen't exist.")
        os.system("pause")
        quit()
    else:
        mc_path = mc_path_candidate

    dest_candidate = input("enter the path to desired backup folder: ").replace("/", "\\")
    if not os.path.isdir(dest_candidate):
        print("path either not a directory or doesen't exist.")
        os.system("pause")
        quit()
    else:
        dest = dest_candidate

    f = open(".\\mcbackup_config.txt", "w", "utf-8")
    f.write(mc_path + "\n" + dest)
    f.close()
    print("mc path: {}, dest: {}".format(mc_path, dest))
    print("config saved.")
    return [mc_path, dest]

if os.path.isfile(".\\mcbackup_config.txt"):
    f = open(".\\mcbackup_config.txt", "r", "utf-8")
    lines = f.read().split("\n")
    mc_path = lines[0]
    dest = lines[1]
    f.close()

    if os.path.isdir(mc_path) == False or os.path.isdir(dest) == False:
        config = generateconfig()
        main(config[0], config[1])
    else:
        main(mc_path, dest)
else:
    config = generateconfig()
    main(config[0], config[1])

