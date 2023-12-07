from datetime import datetime, timezone
import shutil
import os
import stat

def list_all_files(dir_path):
    return [os.path.abspath(os.path.join(dir_path, f)) for f in os.listdir(dir_path)]

def move_all_files(paths, dest):
    for path in paths:
        shutil.move(path, dest)

def copy_all_files(paths, dest):
    for path in paths:
        shutil.copy(path, dest) 

def remove_all_files(paths):
    for path in paths:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def create_directory(path):
    os.makedirs(path)

def create_empty_file(path):
    open(path, 'a').close()

def get_file_info(path):
    file_stat = os.stat(path)
   
    stat_dir = {}
    if stat.S_ISDIR(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "Directory"
    elif stat.S_ISCHR(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "Character special device"
    elif stat.S_ISBLK(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "Block special device"
    elif stat.S_ISREG(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "Regular File"
    elif stat.S_ISFIFO(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "FIFO"
    elif stat.S_ISLNK(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "Symbolic link"
    elif stat.S_ISSOCK(file_stat[stat.ST_MODE]):
        stat_dir["type"] = "Socket"

    stat_dir["permissions"] = stat.filemode(file_stat[stat.ST_MODE])
    stat_dir["size"] = file_stat[stat.ST_SIZE]
    stat_dir["lastmod"] = file_stat[stat.ST_MTIME]
    stat_dir["lastmod"] = datetime.fromtimestamp(stat_dir["lastmod"], tz=timezone.utc)
    stat_dir["lastaccess"] = file_stat[stat.ST_ATIME]
    stat_dir["lastaccess"] = datetime.fromtimestamp(stat_dir["lastaccess"], tz=timezone.utc)
    stat_dir["lastmeta"] = file_stat[stat.ST_CTIME]
    stat_dir["lastmeta"] = datetime.fromtimestamp(stat_dir["lastmeta"], tz=timezone.utc)

    return stat_dir

def change_unit(value):
    if value < 2**10:
        return value, "B"
    elif value <2**20:
        return value / 2**10, "KiB"
    elif value <2**30:
        return value / 2**20, "MiB"
    else:
        return value / 2**30, "GiB"

def get_part_usage(path):
    total, _, free = shutil.disk_usage(path)
    return change_unit(total), change_unit(free)

def rename_file(path, newname):
    os.rename(path, newname)
