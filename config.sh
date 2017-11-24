#!/bin/bash

#Global
root=$(cd $(dirname $(readlink -f  $0)) && pwd)
image_name=ubuntu-emacs-ide
user_id=$UID
group_id=$user_id


#Docker Run
mount_point=/volume
emacs_config=.emacs
through_point=/ide
env_config=env-config.sh
ctags_exclude_config=ctags-exclude.list
ide_tmp_dir_name=ide-tmp
ide_tmp_dir=$through_point/${ide_tmp_dir_name%${ide_tmp_dir_name##*[!/]}}/
storage=/storage
workdir=$mount_point
label=${image_name}
ide_external_root=~/.ide
ide_home_dir_name=home
ide_server_dir_name=server
ide_project_dir_name=.project
ide_packages_dir_name=ide-packages


#Docker Build
docker_file=$root/Dockerfile
build_root=/build
build_script=${build_root}/init.sh
entrypoint_script=${build_root}/entrypoint.sh
dist_point=${build_root}
volume=${image_name}-volume

nvm_root=/opt/nvm

#install
install_name=ide
install_dir=/usr/local/bin
install_point=${install_dir}/${install_name}
