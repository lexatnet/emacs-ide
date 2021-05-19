#!/bin/bash

# https://www.python.org/downloads/release/python-2718/

install_python3_from_sources(){
  local src_url='https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz'
  local local_repo_cache='./python'
  local local_repo=''
  local prefix='/usr/local/share'
  local args=("$@")
  local cwd=$(pwd)
  local base=''
  local libs=''
  local includes=''

  while [[ $# -gt 0 ]]
  do
    key="$1"
    case $key in
      --base)
        base=$2
        shift # past argument
        shift # past value
        ;;
      --includes)
        includes=$2
        shift # past argument
        shift # past value
        ;;
      --libs)
        libs=$2
        shift # past argument
        shift # past value
        ;;
      --local-repo)
        local_repo=$2
        shift # past argument
        shift # past value
        ;;
      --local-repo-cache)
        local_repo_cache=$2
        shift # past argument
        shift # past value
        ;;
      --prefix)
        prefix=$2
        shift # past argument
        shift # past value
        ;;
      --src-url)
        src_url=$2
        shift # past argument
        shift # past value
        ;;
      *)    # unknown option
        shift # past argument
        ;;
    esac
  done
  set -- "${args[@]}" # restore positional parameters


  [ -d $local_repo_cache ] || wget --directory-prefix=${local_repo_cache}  ${src_url}

  cp -r $local_repo_cache $local_repo
  cd $local_repo
  tar -xvf Python-3.9.5.tgz
  cd ./Python-3.9.5
  ./configure --enable-optimizations --with-ensurepip=install --prefix ${prefix} LDFLAGS="-L${libs}" CFLAGS="${includes} -I${prefix}/includes/python3.9/iternal"
  make -j8
  # make check
  make install
  cd ../..

  # clear
  rm --recursive $local_repo
  # restore working directory
  cd $cwd
}
