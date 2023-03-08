import argparse
import urllib.request
import zipfile
import shutil
import subprocess
import uuid

from os import makedirs, remove, getcwd
from os.path import join, basename

PROJECT_NAME = basename(getcwd())

# Directories
COMPILER_DIR = "compiler"
SOURCE_DIR = "src"
DIST_DIR = "gamemodes"
SAMPBP_DIR = ".sampbp"
INCLUDE_DIR = join(COMPILER_DIR, "include")
PLUGINS_DIR = "plugins"
FILTERSCRIPTS_DIR = "filterscripts"
SCRIPTFILES_DIR = "scriptfiles"

# Filenames
SAMP_SERVER_FILENAME = "samp-server.exe"
COMPILER_FILENAME = "pawncc.exe"
COMPILER_DLL_FILENAME = "pawnc.dll"
MAIN_ENTRY_FILENAME = f"{PROJECT_NAME}.pwn"
SERVER_CONFIG_FILENAME = "server.cfg"
RESOURCES_FILENAME = "resources.zip"
A_ACTOR_INC_FILENAME = "a_actor.inc"
A_HTTP_INC_FILENAME = "a_http.inc"
A_NPC_INC_FILENAME = "a_npc.inc"
A_OBJECTS_INC_FILENAME = "a_objects.inc"
A_PLAYERS_INC_FILENAME = "a_players.inc"
A_SAMP_INC_FILENAME = "a_samp.inc"
A_SAMPDB_INC_FILENAME = "a_sampdb.inc"
A_VEHICLES_INC_FILENAME = "a_vehicles.inc"
CONSOLE_INC_FILENAME = "console.inc"
CORE_INC_FILENAME = "core.inc"
DATAGRAM_INC_FILENAME = "datagram.inc"
DEFAULT_INC_FILENAME = "default.inc"
FILE_INC_FILENAME = "file.inc"
FLOAT_INC_FILENAME = "float.inc"
STRING_INC_FILENAME = "string.inc"
TIME_INC_FILENAME = "time.inc"

# Pathes
COMPILER_PATH = join(COMPILER_DIR, COMPILER_FILENAME)
COMPILER_DLL_PATH = join(COMPILER_DIR, COMPILER_DLL_FILENAME)
MAIN_ENTRY_PATH = join(SOURCE_DIR, MAIN_ENTRY_FILENAME)
MAIN_ENTRY_DIST_PATH = join(DIST_DIR, MAIN_ENTRY_FILENAME)
RESOURCES_TEMP_PATH = join(SAMPBP_DIR, RESOURCES_FILENAME)
A_ACTOR_INC_PATH = join(INCLUDE_DIR, A_ACTOR_INC_FILENAME)
A_HTTP_INC_PATH = join(INCLUDE_DIR, A_HTTP_INC_FILENAME)
A_NPC_INC_PATH = join(INCLUDE_DIR, A_NPC_INC_FILENAME)
A_OBJECTS_INC_PATH = join(INCLUDE_DIR, A_OBJECTS_INC_FILENAME)
A_PLAYERS_INC_PATH = join(INCLUDE_DIR, A_PLAYERS_INC_FILENAME)
A_SAMP_INC_PATH = join(INCLUDE_DIR, A_SAMP_INC_FILENAME)
A_SAMPDB_INC_PATH = join(INCLUDE_DIR, A_SAMPDB_INC_FILENAME)
A_VEHICLES_INC_PATH = join(INCLUDE_DIR, A_VEHICLES_INC_FILENAME)
CONSOLE_INC_PATH = join(INCLUDE_DIR, CONSOLE_INC_FILENAME)
CORE_INC_PATH = join(INCLUDE_DIR, CORE_INC_FILENAME)
DATAGRAM_INC_PATH = join(INCLUDE_DIR, DATAGRAM_INC_FILENAME)
DEFAULT_INC_PATH = join(INCLUDE_DIR, DEFAULT_INC_FILENAME)
FILE_INC_PATH = join(INCLUDE_DIR, FILE_INC_FILENAME)
FLOAT_INC_PATH = join(INCLUDE_DIR, FLOAT_INC_FILENAME)
STRING_INC_PATH = join(INCLUDE_DIR, STRING_INC_FILENAME)
TIME_INC_PATH = join(INCLUDE_DIR, TIME_INC_FILENAME)

# Data
RESOURCES_ARCH_DATA = [
    {
        'entry': 'sampbp-resources-master/pawncc.exe',
        'dist': COMPILER_PATH
    },
    {
        'entry': 'sampbp-resources-master/pawnc.dll',
        'dist': COMPILER_DLL_PATH
    },
    {
        'entry': 'sampbp-resources-master/console.inc',
        'dist': CONSOLE_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/core.inc',
        'dist': CORE_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/datagram.inc',
        'dist': DATAGRAM_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/default.inc',
        'dist': DEFAULT_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/file.inc',
        'dist': FILE_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/float.inc',
        'dist': FLOAT_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/string.inc',
        'dist': STRING_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/time.inc',
        'dist': TIME_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_actor.inc',
        'dist': A_ACTOR_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_http.inc',
        'dist': A_HTTP_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_npc.inc',
        'dist': A_NPC_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_objects.inc',
        'dist': A_OBJECTS_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_players.inc',
        'dist': A_PLAYERS_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_samp.inc',
        'dist': A_SAMP_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_sampdb.inc',
        'dist': A_SAMPDB_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/a_vehicles.inc',
        'dist': A_VEHICLES_INC_PATH
    },
    {
        'entry': 'sampbp-resources-master/samp-server.exe',
        'dist': SAMP_SERVER_FILENAME
    }
]

MAIN_ENTRY_DATA = [
    "#include <a_samp>",
    "main() {}"
]

SERVER_CONFIG_DATA = [
    f"gamemode0 {PROJECT_NAME}",
    f"rcon_password {uuid.uuid4()}",
    f"hostname {PROJECT_NAME}",
    "port 7777",
    "maxplayers 50",
    "language English",
    f"mapname {PROJECT_NAME}",
    f"weburl www.{PROJECT_NAME}.com",
    f"gamemodetext {PROJECT_NAME}",
    "announce 0",
    "lanmode 0"
]

# Urls
RESOURCES_URL = "https://github.com/bqio/sampbp-resources/archive/refs/heads/master.zip"

def create_main_entry_file():
    print("Creating main entry file...")
    with open(MAIN_ENTRY_PATH, "w", encoding='utf-8') as fp:
        fp.write("\n".join(MAIN_ENTRY_DATA))

def remove_temporary_files():
    print("Removing temporary files...")
    shutil.rmtree(SAMPBP_DIR)

def create_server_config_file():
    print("Creating server config file...")
    with open(SERVER_CONFIG_FILENAME, "w", encoding='utf-8') as fp:
        fp.write("\n".join(SERVER_CONFIG_DATA))

def create_project_structure():
    print("Creating project structure...")
    makedirs(INCLUDE_DIR, exist_ok=True)
    makedirs(DIST_DIR, exist_ok=True)
    makedirs(PLUGINS_DIR, exist_ok=True)
    makedirs(SOURCE_DIR, exist_ok=True)
    makedirs(SAMPBP_DIR, exist_ok=True)
    makedirs(FILTERSCRIPTS_DIR, exist_ok=True)
    makedirs(SCRIPTFILES_DIR, exist_ok=True)

def download_server_resources():
    print("Downloading server resources...")
    urllib.request.urlretrieve(RESOURCES_URL, RESOURCES_TEMP_PATH)

def install_server_resources():
    print(f"Installing server resources...")
    with zipfile.ZipFile(RESOURCES_TEMP_PATH, 'r') as zip:
        for file in RESOURCES_ARCH_DATA:
            with open(file['dist'], "wb") as fd:
                fd.write(zip.read(file['entry']))
                print(f"- Copying {file['dist']}...")

def init():
    print(f"Initializing project {PROJECT_NAME}...")
    create_project_structure()
    create_server_config_file()
    create_main_entry_file()
    download_server_resources()
    install_server_resources()
    remove_temporary_files()
    build()

def run():
    subprocess.run([SAMP_SERVER_FILENAME])

def build():
    print(f"Building {PROJECT_NAME}...")
    shutil.copyfile(MAIN_ENTRY_PATH, MAIN_ENTRY_DIST_PATH)
    subprocess.run([COMPILER_PATH, f"-D{DIST_DIR}", MAIN_ENTRY_FILENAME])
    remove(MAIN_ENTRY_DIST_PATH)

def clean():
    print("Cleaning project...")
    shutil.rmtree(SAMPBP_DIR, ignore_errors=True)
    shutil.rmtree(COMPILER_DIR, ignore_errors=True)
    shutil.rmtree(FILTERSCRIPTS_DIR, ignore_errors=True)
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    shutil.rmtree(PLUGINS_DIR, ignore_errors=True)
    shutil.rmtree(SCRIPTFILES_DIR, ignore_errors=True)
    shutil.rmtree(SOURCE_DIR, ignore_errors=True)
    remove(SAMP_SERVER_FILENAME)
    remove(SERVER_CONFIG_FILENAME)

def main(args):
    if args.command == "init":
        init()
    if args.command == "build":
        build()
    if args.command == "run":
        run()
    if args.command == "clean":
        clean()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="sampbp",
        description="SA-MP Server Boilerplate generator."
    )
    parser.add_argument("command", choices=['init', 'build', 'run', 'clean'])
    args = parser.parse_args()
    main(args)