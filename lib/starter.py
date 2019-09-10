import getpass
import os
from string import Template
import logging
import tempfile
import uuid
import subprocess
import time

class LexetStarter():
  def __init__(self, conf, project):
    self.conf = conf
    self.project = project

  def start(self, mode):
    if mode == 'text':
      self.run()
    elif mode == 'ui':
      self.run_x()
    elif mode == 'uis':
      # self.run_x_ssh()
      pass

  def run(self):
    parts = ['docker']
    parts.append('run')
    parts.append(
      Template('--label "label=$label"')
      .substitute(
        label = self.conf['environment']['label']
      )
    )
    parts.append(
      Template('--volume $project_external_dir:$mount_point')
      .substitute(
        project_external_dir = self.project.get_lexet_project_external_dir(),
        mount_point = self.conf['docker']['mount_point']
      )
    )
    parts.append(
      Template('--volume $lexet_project_external_dir:$lexet_project_dir')
      .substitute(
        lexet_project_external_dir = self.project.get_lexet_project_external_dir(),
        lexet_project_dir = self.project.get_lexet_project_dir()
      )
    )
    parts.append(
      Template('--volume $root/config/$emacs_config:$through_point/$emacs_config')
      .substitute(
        root = self.conf['global']['root'],
        emacs_config = self.conf['docker']['emacs_config'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $root/config/$ctags_exclude_config:$through_point/$ctags_exclude_config')
      .substitute(
        root = self.conf['global']['root'],
        ctags_exclude_config = self.conf['docker']['ctags_exclude_config'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $lexet_tmp_external_dir:$lexet_tmp_dir')
      .substitute(
        lexet_tmp_external_dir = self.project.get_lexet_tmp_external_dir(),
        lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
      )
    )
    parts.append(
      Template('--volume $root/packages:$lexet_packages_dir')
      .substitute(
        root = self.conf['global']['root'],
        lexet_packages_dir = self.project.get_lexet_packages_dir()
      )
    )
    parts.append(
      Template('--volume $lexet_vendor_packages_external_dir:$lexet_vendor_packages_dir')
      .substitute(
        lexet_vendor_packages_external_dir = self.project.get_lexet_vendor_packages_external_dir(),
        lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
      )
    )
    parts.append(
      Template('--env-file $env_config')
      .substitute(
        env_config = self.conf['docker']['env_config']
      )
    )
    parts.append(
      Template('-e USER=$user')
      .substitute(
        user = getpass.getuser()
      )
    )
    parts.append(
      Template('-e HOME=$lexet_home')
      .substitute(
        lexet_home = self.project.get_lexet_home()
      )
    )
    parts.append(
      Template('-e lexet_home=$lexet_home')
      .substitute(
        lexet_home = self.project.get_lexet_home()
      )
    )
    parts.append(
      Template('-e lexet_server_dir=$lexet_server_dir')
      .substitute(
        lexet_server_dir = self.project.get_lexet_server_dir()
      )
    )
    parts.append(
      Template('-e lexet_tmp_dir=$lexet_tmp_dir')
      .substitute(
        lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
      )
    )
    parts.append(
      Template('-e lexet_packages_dir=$lexet_packages_dir')
      .substitute(
        lexet_packages_dir = self.project.get_lexet_packages_dir()
      )
    )
    parts.append(
      Template('-e lexet_vendor_packages_dir=$lexet_vendor_packages_dir')
      .substitute(
        lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
      )
    )
    parts.append(
      Template('-e mount_point=$mount_point')
      .substitute(
        mount_point = self.conf['docker']['mount_point']
      )
    )
    parts.append(
      Template('-e through_point=$through_point')
      .substitute(
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('-e emacs_config=$emacs_config')
      .substitute(
        emacs_config = self.conf['docker']['emacs_config']
      )
    )
    parts.append(
      Template('-e project_name=$project_name')
      .substitute(
        project_name = self.project.name
      )
    )
    parts.append(
      Template('-e lexet_tags_dir=$lexet_tags_dir')
      .substitute(
        lexet_tags_dir = self.project.get_lexet_tags_dir()
      )
    )
    parts.append(
      Template('--workdir $workdir')
      .substitute(
        workdir = self.conf['environment']['workdir']
      )
    )
    parts.append('--interactive')
    parts.append('--tty')
    parts.append('--rm')
    parts.append(
      Template('--user $user_id:$group_id')
      .substitute(
        user_id = os.getuid(),
        group_id = os.getuid()
      )
    )
    parts.append(self.conf['global']['image_tag'])
    logging.info('run command "{command}"'.format(command=' '.join(parts)))
    # import pdb; pdb.set_trace()
    os.system(' '.join(parts))

  def run_x(self):
    parts = ['docker']
    parts.append('run')
    parts.append(
      Template('--name $project_name')
      .substitute(
        project_name = self.project.name
      )
    )
    parts.append(
      Template('--label "label=$label"')
      .substitute(
        label = self.conf['environment']['label']
      )
    )
    parts.append(
      Template('--volume $project_external_dir:$mount_point')
      .substitute(
        project_external_dir = self.project.get_lexet_project_external_dir(),
        mount_point = self.conf['docker']['mount_point']
      )
    )
    parts.append(
      Template('--volume $lexet_project_external_dir:$lexet_project_dir')
      .substitute(
        lexet_project_external_dir = self.project.get_lexet_project_external_dir(),
        lexet_project_dir = self.project.get_lexet_project_dir()
      )
    )
    parts.append(
      Template('--volume $_dir/lib:$through_point/lib')
      .substitute(
        _dir = os.path.join(
          self.conf['global']['root'],
          'scripts'
        ),
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $root/config/$emacs_config:$through_point/$emacs_config')
      .substitute(
        root = self.conf['global']['root'],
        emacs_config = self.conf['docker']['emacs_config'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $root/config/$ctags_exclude_config:$through_point/$ctags_exclude_config')
      .substitute(
        root = self.conf['global']['root'],
        ctags_exclude_config = self.conf['docker']['ctags_exclude_config'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $lexet_external_root/init:$through_point/init')
      .substitute(
        lexet_external_root = self.conf['environment']['lexet_external_root'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $lexet_external_root/env:$through_point/env')
      .substitute(
        lexet_external_root = self.conf['environment']['lexet_external_root'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $_dir/$entrypoint_run_lexet:$through_point/$entrypoint_run_lexet')
      .substitute(
        _dir = os.path.join(
          self.conf['global']['root'],
          'scripts'
        ),
        entrypoint_run_lexet = self.conf['environment']['entrypoint_run_lexet'],
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('--volume $lexet_tmp_external_dir:$lexet_tmp_dir')
      .substitute(
        lexet_tmp_external_dir = self.project.get_lexet_tmp_external_dir(),
        lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
      )
    )
    parts.append(
      Template('--volume $root/packages:$lexet_packages_dir')
      .substitute(
        root = self.conf['global']['root'],
        lexet_packages_dir = self.project.get_lexet_packages_dir()
      )
    )
    parts.append(
      Template('--volume $lexet_vendor_packages_external_dir:$lexet_vendor_packages_dir')
      .substitute(
        lexet_vendor_packages_external_dir = self.project.get_lexet_vendor_packages_external_dir(),
        lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
      )
    )
    parts.append('--volume /tmp/.X11-unix:/tmp/.X11-unix:rw')
    parts.append(
      Template('--env-file $env_config')
      .substitute(
        env_config = self.conf['docker']['env_config']
      )
    )
    parts.append(
      Template('-e DISPLAY=$DISPLAY')
      .substitute(
        DISPLAY = os.environ['DISPLAY']
      )
    )
    parts.append('-e QT_X11_NO_MITSHM=1')
    parts.append('-e NO_AT_BRIDGE=1')
    parts.append(
      Template('-e USER=$USER')
      .substitute(
        USER = getpass.getuser()
      )
    )
    parts.append(
      Template('-e HOME=$lexet_home')
      .substitute(
        lexet_home = self.project.get_lexet_home()
      )
    )
    parts.append(
      Template('-e lexet_home=$lexet_home')
      .substitute(
        lexet_home = self.project.get_lexet_home()
      )
    )
    parts.append(
      Template('-e lexet_server_dir=$lexet_server_dir')
      .substitute(
        lexet_server_dir = self.project.get_lexet_server_dir()
      )
    )
    parts.append(
      Template('-e lexet_tmp_dir=$lexet_tmp_dir')
      .substitute(
        lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
      )
    )
    parts.append(
      Template('-e lexet_packages_dir=$lexet_packages_dir')
      .substitute(
        lexet_packages_dir = self.project.get_lexet_packages_dir()
      )
    )
    parts.append(
      Template('-e lexet_vendor_packages_dir=$lexet_vendor_packages_dir')
      .substitute(
        lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
      )
    )
    parts.append(
      Template('-e mount_point=$mount_point')
      .substitute(
        mount_point = self.conf['docker']['mount_point']
      )
    )
    parts.append(
      Template('-e through_point=$through_point')
      .substitute(
        through_point = self.conf['docker']['through_point']
      )
    )
    parts.append(
      Template('-e emacs_config=$emacs_config')
      .substitute(
        emacs_config = self.conf['docker']['emacs_config']
      )
    )
    parts.append(
      Template('-e ctags_exclude_config_path=$through_point/$ctags_exclude_config')
      .substitute(
        through_point = self.conf['docker']['through_point'],
        ctags_exclude_config = self.conf['docker']['ctags_exclude_config']
      )
    )
    parts.append(
      Template('-e project_name=$project_name')
      .substitute(
        project_name = self.project.name
      )
    )
    parts.append(
      Template('-e lexet_tags_dir=$lexet_tags_dir')
      .substitute(
        lexet_tags_dir = self.project.get_lexet_tags_dir()
      )
    )
    parts.append(
      Template('--workdir $workdir')
      .substitute(
        workdir = self.conf['environment']['workdir'],
      )
    )
    parts.append('--rm')
    parts.append(
      Template('--entrypoint $through_point/$entrypoint_run_lexet')
      .substitute(
        through_point = self.conf['docker']['through_point'],
        entrypoint_run_lexet = self.conf['environment']['entrypoint_run_lexet']
      )
    )
    parts.append(
      Template('--user $user_id:$group_id')
      .substitute(
        user_id = os.getuid(),
        group_id = os.getuid()
      )
    )
    parts.append(self.conf['global']['image_tag'])
    logging.info('run command "{command}"'.format(command=' '.join(parts)))
    os.system(' '.join(parts))

  def get_container_id_file(self):
    return Template('$lexet_project_external_dir/docker-container-id')
      .substitute(
        lexet_project_external_dir = self.project.get_lexet_project_external_dir()
      )

  def create_lexet_ssh_session_file(self):
    uid = uuid.uuid1()
    lexet_ssh_session_file=$(mktemp $project_sessions_dir/lexet.ssh.session.XXXXXXXXX)

  def generate_sshd_config(self):
    pid_file = os.path.join(
      self.project.get_lexet_project_dir(),
      '.ssh',
      'run',
      'sshd.pid'
    )

    authorized_keys_file = os.path.join(
      self.project.get_lexet_project_dir(),
      '.ssh',
      'key.pub'
    )
    rsa_host_key_file = os.path.join(
      self.project.get_lexet_project_dir(),
      '.ssh',
      'ssh_host_rsa_key'
    )
    dsa_host_key_file = os.path.join(
      self.project.get_lexet_project_dir(),
      '.ssh',
      'ssh_host_dsa_key'
    )
    ecdsa_host_key_file = os.path.join(
      self.project.get_lexet_project_dir(),
      '.ssh',
      'ssh_host_ecdsa_key'
    )
    return Template("""
Port $port
PidFile $pid_file
UsePrivilegeSeparation no
AuthorizedKeysFile $authorized_keys_file
HostKey $rsa_host_key_file
HostKey $dsa_host_key_file
HostKey $ecdsa_host_key_file
PasswordAuthentication no
UsePAM no
PermitRootLogin no
PermitEmptyPasswords no
RSAAuthentication yes
PubkeyAuthentication yes
X11Forwarding yes
X11UseLocalHost no
LogLevel VERBOSE
AllowUsers $user
""")
      .substitute(
        port = self.conf['docker']['sshd_port'],
        pid_file = pid_file,
        authorized_keys_file = authorized_keys_file,
        rsa_host_key_file = rsa_host_key_file,
        dsa_host_key_file = dsa_host_key_file,
        ecdsa_host_key_file = ecdsa_host_key_file,
        user = getpass.getuser()
      )

  def generate_lexet_user_profile() {
      return Template("""
export USER=$USER
export HOME=$lexet_home
export lexet_home=$lexet_home
export lexet_server_dir=$lexet_server_dir
export lexet_tmp_dir=$lexet_tmp_dir
export lexet_packages_dir=$lexet_packages_dir
export lexet_vendor_packages_dir=$lexet_vendor_packages_dir
export mount_point=$mount_point
export through_point=$through_point
export sshd_config=$sshd_config
export emacs_config=$emacs_config
export group_id=$group_id
export project_name=$project_name
export lexet_tags_dir=$lexet_tags_dir

if [ -d $through_point/init ]; then
  for i in $through_point/init/*.sh; do
    if [ -r \$i ]; then
      . \$i
    fi
  done
  unset i
fi
""")
      .substitute(
        USER = getpass.getuser(),
        HOME = self.project.get_lexet_home()
        lexet_home = self.project.get_lexet_home()
        lexet_server_dir = self.project.get_lexet_server_dir()
        lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
        lexet_packages_dir = self.project.get_lexet_packages_dir()
        lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
        mount_point = self.conf['docker']['mount_point']
        through_point = self.conf['docker']['through_point']
        sshd_config = self.conf['ssh']['sshd_config']
        emacs_config = self.conf['docker']['emacs_config']
        group_id = os.getuid()
        project_name = self.project.name
        lexet_tags_dir = self.project.get_lexet_tags_dir()
      )

  def run_x_ssh(self):
    project_sessions_dir = self.project.get_project_sessions_dir()
    container_id_file = self.get_container_id_file()

    if not os.path.exists(project_sessions_dir):
        os.makedirs(project_sessions_dir)

    self.create_lexet_ssh_session_file()

    if not os.path.exists(project_sessions_dir):

      lexet_sshd_config_external_file = os.path.join(
        self.project.get_lexet_project_external_dir(),
        self.conf['ssh']['sshd_config']
      )

      logging.info("lexet_sshd_config_external_file=$lexet_sshd_config_external_file")

      logging.info("workdir=$workdir")

      open(
        lexet_sshd_config_external_file,
        'w'
      )
      .write(self.generate_sshd_config())
      .close()

      open(
        os.path.join(
          self.project.get_lexet_home_external_dir()
          '.profile'
        ),
        'w'
      )
      .write(self.generate_lexet_user_profile())
      .close()

      open(
        os.path.join(
          self.project.get_lexet_home_external_dir()
          '.bashrc'
        ),
        'w'
      )
      .write(self.generate_lexet_user_profile())
      .close()

      parts = ['docker']
      parts.append('run')
      parts.append(
        Template('--name $project_name')
        .substitute(
          project_name = self.project.name
        )
      )
      parts.append(
        Template('--label "label=$label"')
        .substitute(
          label = self.conf['environment']['label']
        )
      )
      parts.append(
        Template('--volume $project_external_dir:$mount_point')
        .substitute(
          project_external_dir = self.project.get_lexet_project_external_dir(),
          mount_point = self.conf['docker']['mount_point']
        )
      )
      parts.append(
        Template('--volume $lexet_project_external_dir:$lexet_project_dir')
        .substitute(
          lexet_project_external_dir = self.project.get_lexet_project_external_dir(),
          lexet_project_dir = self.project.get_lexet_project_dir()
        )
      )
      parts.append(
        Template('--volume $_dir/lib:$through_point/lib')
        .substitute(
          _dir = os.path.join(
            self.conf['global']['root'],
            'scripts'
          ),
          through_point = self.conf['docker']['through_point']
        )
      )
      parts.append(
        Template('--volume $root/config/$emacs_config:$through_point/$emacs_config')
        .substitute(
          root = self.conf['global']['root'],
          emacs_config = self.conf['docker']['emacs_config'],
          through_point = self.conf['docker']['through_point']
        )
      )
      parts.append(
        Template('--volume $root/config/$ctags_exclude_config:$through_point/$ctags_exclude_config')
        .substitute(
          root = self.conf['global']['root'],
          ctags_exclude_config = self.conf['docker']['ctags_exclude_config'],
          through_point = self.conf['docker']['through_point']
        )
      )
      parts.append(
        Template('--volume $lexet_external_root/init:$through_point/init')
        .substitute(
          lexet_external_root = self.conf['environment']['lexet_external_root'],
          through_point = self.conf['docker']['through_point']
        )
      )
      parts.append(
        Template('--volume $lexet_external_root/env:$through_point/env')
        .substitute(
          lexet_external_root = self.conf['environment']['lexet_external_root'],
          through_point = self.conf['docker']['through_point']
        )
      )
      parts.append(
        Template('--volume $lexet_tmp_external_dir:$lexet_tmp_dir')
        .substitute(
          lexet_tmp_external_dir = self.project.get_lexet_tmp_external_dir(),
          lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
        )
      )
      parts.append(
        Template('--volume $root/packages:$lexet_packages_dir')
        .substitute(
          root = self.conf['global']['root'],
          lexet_packages_dir = self.project.get_lexet_packages_dir()
        )
      )
      parts.append(
        Template('--volume $lexet_vendor_packages_external_dir:$lexet_vendor_packages_dir')
        .substitute(
          lexet_vendor_packages_external_dir = self.project.get_lexet_vendor_packages_external_dir(),
          lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
        )
      )
      parts.append(
        Template('--env-file $env_config')
        .substitute(
          env_config = self.conf['docker']['env_config']
        )
      )
      parts.append(
        Template('-e USER=$USER')
        .substitute(
          USER = getpass.getuser()
        )
      )
      parts.append(
        Template('-e HOME=$lexet_home')
        .substitute(
          lexet_home = self.project.get_lexet_home()
        )
      )
      parts.append(
        Template('-e lexet_home=$lexet_home')
        .substitute(
          lexet_home = self.project.get_lexet_home()
        )
      )
      parts.append(
        Template('-e lexet_tmp_dir=$lexet_tmp_dir')
        .substitute(
          lexet_tmp_dir = self.conf['docker']['lexet_tmp_dir']
        )
      )
      parts.append(
        Template('-e lexet_packages_dir=$lexet_packages_dir')
        .substitute(
          lexet_packages_dir = self.project.get_lexet_packages_dir()
        )
      )
      parts.append(
        Template('-e lexet_vendor_packages_dir=$lexet_vendor_packages_dir')
        .substitute(
          lexet_vendor_packages_dir = self.project.get_lexet_vendor_packages_dir()
        )
      )
      parts.append(
        Template('-e mount_point=$mount_point')
        .substitute(
          mount_point = self.conf['docker']['mount_point']
        )
      )
      parts.append(
        Template('-e through_point=$through_point')
        .substitute(
          through_point = self.conf['docker']['through_point']
        )
      )
      parts.append(
        Template('-e emacs_config=$emacs_config')
        .substitute(
          emacs_config = self.conf['docker']['emacs_config']
        )
      )
      parts.append(
        Template('-e ctags_exclude_config_path=$through_point/$ctags_exclude_config')
        .substitute(
          through_point = self.conf['docker']['through_point'],
          ctags_exclude_config = self.conf['docker']['ctags_exclude_config']
        )
      )
      parts.append(
        Template('-e project_name=$project_name')
        .substitute(
          project_name = self.project.name
        )
      )
      parts.append(
        Template('-e lexet_tags_dir=$lexet_tags_dir')
        .substitute(
          lexet_tags_dir = self.project.get_lexet_tags_dir()
        )
      )
      parts.append(
        Template('--workdir $workdir')
        .substitute(
          workdir = self.conf['environment']['workdir'],
        )
      )
      parts.append('--rm')
      parts.append('--interactive')
      parts.append('--tty')
      parts.append('--detach')
      parts.append('--publish 2222')
      parts.append(
        Template('--volume $lexet_sshd_config_external_file:$through_point/$sshd_config')
        .substitute(
          lexet_sshd_config_external_file = lexet_sshd_config_external_file,
          through_point = self.conf['docker']['through_point'],
          sshd_config = self.conf['ssh']['sshd_config']
        )
      )
      parts.append(
        Template('-e sshd_config=$sshd_config')
        .substitute(
          sshd_config = self.conf['ssh']['sshd_config']
        )
      )
      parts.append(
        Template('-e group_id=$group_id')
        .substitute(
          group_id = os.getuid()
        )
      )
      parts.append(
        Template('-e user_id=$user_id')
        .substitute(
          user_id = os.getuid()
        )
      )
      parts.append(
        Template('--entrypoint $through_point/$entrypoint_sshd')
        .substitute(
          through_point = self.conf['docker']['through_point']
          entrypoint_sshd = self.conf['environment']['entrypoint_sshd']
        )
      )
      parts.append(self.conf['global']['image_tag'])
      p = subprocess.run(parts, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      container_id_file = p.stdout
      time.sleep( 5 )
    

    ssh_external_port=$(docker port $project_name 2222/tcp | sed -E "s/.*\:([0-9]+)/\1/g")

  run_lexetx_through_ssh() {
    ssh -v -X -p $ssh_external_port -i $lexet_key_external_dir/$lexet_key_name -o "IdentitiesOnly yes" -o "StrictHostKeyChecking no" localhost "cd $workdir; lexet;"
  }

  try --command run_lexetx_through_ssh --try-times 2

  if [ -e $lexet_ssh_session_file ]; then
     rm $lexet_ssh_session_file
  fi

  if [ -z "$(ls -A $project_sessions_dir)" ]; then
    logging.info('no active lexet sessions.')
    logging.info('stopping docker...')
    
    subprocess.run(
      [
        'docker',
        'stop',
        self.project.name
      ],
      universal_newlines=True,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
      
    
    
    logging.info('docker image stopped.')

    logging.info('removing docker ssh link from known hosts...')
    subprocess.run(
      [
        'ssh-keygen',
        '-f',
        "/home/$USER/.ssh/known_hosts"
        '-R',
        '[localhost]:$ssh_external_port'
      ],
      universal_newlines=True,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    logging.info('docker ssh link removed from known hosts.')

    if os.path.exists(container_id_file):
      rm $container_id_file
  else
    logging.info('exists active lexet sessions.')
