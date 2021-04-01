#!/bin/bash

usage() {
  echo "$0 [db_name] [backup_dir]"
  exit 1
}

error() {
  msg "ERROR: $1"
  exit 1
}

info() {
  msg "INFO:  $1"
}

msg() {
  echo "$1"
}

if [ -z "$1" ]; then
  usage
else
  db_name="$1"
fi

if [ -z "$2" ]; then
  backup_dir="./"
else
  backup_dir="$2"
fi

backup_name="BACKUP-$db_name-`date +%Y-%m-%dT%H-%M-%S`"
tar_filename="$backup_name.tar"
zipped_filename="$tar_filename.gz"

db_server="localhost"
db_port="27017"

# BACKUP
info "MONGODUMP Running..."
/usr/bin/mongodump -h $db_server --port=$db_port -d $db_name -o $backup_name
if [ ! -d "$backup_name" ]; then
  error "MONGODUMP Backup Failed!"
else
  info "MONGODUMP Success!"
fi

info "TAR Running..."
/bin/tar -cf $tar_filename $backup_name
if [ ! -f "$tar_filename" ]; then
  error "TAR Packaging Failed!"
else
  info "TAR Packaging Success!"
fi

info "GZIP Running..."
/bin/gzip $tar_filename
if [ ! -f "$zipped_filename" ]; then
  error "GZIP Zipping Failed!"
else
  info "GZIP Zipping Success!"
fi

# MOVING TO BACKUP_DIR
info "MOVE Running..."
if [ "$backup_dir" == "./" ]; then
  info "Don't Need Moving To $backup_dir"
else
  if [ -d "$backup_dir" ]; then
    mv $zipped_filename $backup_dir
    info "$zipped_filename Has Been Moved To $backup_dir"
  else
    error "$backup_dir Not Exsits!"
  fi
fi

# CLEAN
info "CLEAN Running..."
if [ -d "$backup_name" ]; then
  /bin/rm -rf $backup_name
  info "Reomve $backup_name"
fi

if [ -f "$tar_filename" ]; then
  /bin/rm $tar_filename
  info "Remove $tar_filename"
fi
