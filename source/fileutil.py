
"""
File Utilities and Path Utilities

class futil
class pathutil

"""

import codecs
import glob
import os
import shutil
import subprocess
import sys
import tarfile

'''
these are used in 

- make_zipfile
- make_tarfile

remember to write over these values and that if running as a module,
we just don't have a way to provide these (because it isn't scoped).

'''
root              = os.path.abspath  (os.path.dirname(sys.argv[0]))
public_path       = os.path.join     (root,      'public')

class futil:
  
  @staticmethod
  def rm_all(folder):
    '''https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python#185941'''
    import os, shutil
    for the_file in os.listdir(folder):
      file_path = os.path.join(folder, the_file)
      try:
        if os.path.isfile(file_path):
          os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
      except Exception as e:
        print(e)
  
  @staticmethod
  def read(fileIn):
    d = None
    with open(fileIn, 'r') as myfile:
      d = myfile.read()
      myfile.close()
    return d
  
  @staticmethod
  def write(file_out, file_content, byte_content=False):
    if byte_content: w_mode = 'wb'
    else: w_mode = 'w'
    with open(file_out, w_mode) as text_file:
      text_file.write(file_content)
      text_file.close()

class pathutil:
  
  @staticmethod
  def clean_path(input):
    '''alias for `os.path.abspath(input)`'''
    # .replace('/','\\\\')
    # .replace('/','\\')
    return os.path.abspath(input)
  
  @staticmethod
  def combine(*args):
    '''combine lists — probably in a way plausable to py2 and 3.'''
    result = []
    for arg in args: result = result + arg
    return result
  """
    # NOT USED!
    @staticmethod
    def jpath(*args):
      '''
      Merges some paths but uses the first argument as a title.

      Returns a tuple (title, args)
      '''
      m_list = []
      for arg in args[1:]: m_list.append(str(arg))
      return args[0], os.sep.join(m_list)
  """
  @staticmethod
  def mpath(*args, strip=False):
    '''
    just merges some paths
    '''
    m_list = []
    if strip:
      for arg in args: m_list.append(str(arg).rstrip(os.sep))
    else:
      for arg in args: m_list.append(str(arg))
    return os.sep.join(m_list)

  @staticmethod
  def mfilter(filter:str, *inputs):
    '''
    each input is placed in to the filtered string.

    param: inputs — each subsidiary element being used in filter string.
    
    param: filter — filter applied to each input (EG: path) element.
    
    '''
    items = []
    for x in inputs: items.append((filter.format(x), x))
    return items

  @staticmethod
  def mcopy(filter: str, target:str, *inputs):
    '''
    filtered inputs represent the path of a file, where we are copying
    each file input(s) to the target directory.

    see: `pathutil.mfilter(*inputs, filter:str)`

    param: inputs — each subsidiary element being used in filter string.
    
    param: path_filter — filter applied to each input (path) element.
    
    param: target — directory where inputs are copied.
    '''
    for x in pathutil.mfilter(filter, inputs): shutil.copy(x, target)

class Util:
  """
    METHODS

    - dir_parent
    - recall
    - env_flag
    - env_var
    - rm_all
    - recursive_copy_files
    - par
    - execute
    - strip_ext
    - make_zipfile
    - make_tarfile
    - os_walk
    - walk
  """
  @staticmethod
  def dir_parent(filename):

    return pathutil.mpath(os.path.basename(os.path.dirname(filename)), os.path.basename(filename))

  @staticmethod
  def recall(*args, **kwargs):
    '''
    Generally same as `call` method using Popen with stderr to `subprocess.PIPE`.

    return: `tuple(rc, output, error)`

    param: `stdin` — default = None

    param: `stdout` — default = subprocess.PIPE

    param: `stderr` — default = subprocess.PIPE
    
    param: `strip` — default = False

    param: `cwd = os.curdir` — default is current working directory.
    
    '''

    strip = False if not 'strip' in kwargs else kwargs['strip']
    cwd   = os.curdir if not 'cwd' in kwargs else kwargs['cwd']

    p = subprocess.Popen(
      args,
      stdin   = None if (not 'stdin' in kwargs) else kwargs['stdin'],
      stderr  = subprocess.PIPE if (not 'stderr' in kwargs) else kwargs['stderr'],
      stdout  = subprocess.PIPE if (not 'stdout' in kwargs) else kwargs['stdout'],
      env     = os.environ if (not 'env' in kwargs) else kwargs['env'],
      cwd     = cwd
    )
    # p = subprocess.Popen(args, stdin=None, stderr=subprocess.PIPE,
    #                      stdout=subprocess.PIPE, env=os.environ)
    try:
      output, error = p.communicate()
      rc = p.returncode
      if output != None: output = output.decode('utf-8').strip() if strip else output.decode('utf-8')
      if error  != None: error  = error.decode('utf-8').strip()  if strip else  error.decode('utf-8')
    except:
      pass
    
    return rc, output, error

  @staticmethod
  def env_flag(var:str, default:str=None):
    if var not in os.environ:
      return False
    return True if os.environ[var] == default else False

  @staticmethod
  def env_var(var:str, default=None):

    return default if var not in os.environ else os.environ[var]
  
  @staticmethod
  def rm_all(folder:str):
    '''https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python#185941'''
    for the_file in os.listdir(folder):
      file_path = os.path.join(folder, the_file)
      try:
        if os.path.isfile(file_path): os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
      except Exception as e: print(e)
    if os.path.exists(folder): os.rmdir(folder)

  @staticmethod
  def recursive_copy_files(source_path:str, destination_path:str, overwrite:bool=False):
    """
    Recursive copies files from source  to destination directory.

    - param source_path: source directory
    - param destination_path: destination directory
    - param overwrite if True all files will be overridden otherwise skip if file exist
    - return: count of copied files
    """
    import shutil
    import glob
    files_count = 0
    if not os.path.exists(destination_path): os.mkdir(destination_path)
    items = glob.glob(source_path + '/*')
    for item in items:
      if os.path.isdir(item):
        path = os.path.join(destination_path, item.split('/')[-1])
        files_count += Util.recursive_copy_files(source_path=item, destination_path=path, overwrite=overwrite)
      else:
        file = os.path.join(destination_path, item.split('/')[-1])
        if not os.path.exists(file) or overwrite:
          shutil.copyfile(item, file)
          files_count += 1
    return files_count

  @staticmethod
  def par(key, default, **kwargs):
    '''check if a given key is present and supply (always) a default (null) value.'''
    return default if not key in kwargs else kwargs[key]

  @staticmethod
  def execute(*args, **kwargs):
    '''
    runs command; stdout to file [outfile].
    --------------------------------------
    
    params:

    args: Arguments appended to end of `base_cmd` args.
    
    base_cmd:list = []: a list telling us the forst portion of our command to execute.
    
    outfile:str = None: Path to our output file.  Raise Exception if path is None.
    
    print_out:bool = False: Weather or not we print output to stdout.
    
    cancel_on_error:bool = True: yeah.

    encoding:str = 'utf-8': encoding to (both) print to stdout and the encoding
    used to write to `outfile`.

    param: `cwd:str = os.curdir` — the working directory. Default is the script's start path.
    '''
    
    # wrk_dir = root if not 'wrk_dir' in kwargs else kwargs['wrk_dir']

    base_cmd        = Util.par('base_cmd',       [],         **kwargs)
    outfile         = Util.par('outfile',         None,      **kwargs)
    print_out       = Util.par('print_out',       False,     **kwargs)
    cancel_on_error = Util.par('cancel_on_error', True,      **kwargs)
    encoding        = Util.par('encoding',       'utf-8',    **kwargs)
    cwd             = Util.par('cwd',             os.curdir, **kwargs)

    os.chdir(cwd)

    # if outfile == None:
    #   raise Exception('crap.')

    input = pathutil.combine(base_cmd, list(args))
    rc, out, err = Util.recall(*input, cwd=cwd)

    if (rc != 0) and (err != ''):
      print(err.encode(encoding), file=sys.stderr)
      if (cancel_on_error): sys.exit("ERROR: {}".format(str(rc)))
    
    if print_out: print(out.encode(encoding))
    
    target = os.path.abspath(pathutil.mpath(root, outfile))

    if outfile != None:
      with codecs.open(target, 'w', encoding) as file:
        print ('writing:', target)
        file.write(out)

  @staticmethod
  def strip_ext(input, ext):
    result = input
    if type(ext) == str:
      return result.replace(ext, '').replace(ext.upper(), '')
    if type(ext) == list:
      for E in ext:
        result = result.replace(E, '').replace(E.upper(), '')
      return result

  @staticmethod
  def make_zipfile(*files, pre_name='statik', name='public', source=public_path):
    '''
    param: name is used given a single file-name.
    '''
    E = ['.zip']
    B = os.path.basename(source)
    X = Util.strip_ext(name, E) if name != None else Util.strip_ext(B, E)
    Y = Util.strip_ext(source, E)
    FN = os.path.relpath(root,'{}-{}.zip'.format(pre_name,X) if pre_name != None else '{}.zip'.format(X))
    os.chdir(root)
    print(FN)
    shutil.make_archive(
      FN,
      'zip',           # the archive format - or tar, bztar, gztar 
      root_dir='.',   # root for archive - current working dir if None
      base_dir=source,
      verbose=1)   # start archiving from here - cwd if None too
    # https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    
    # 
    # def dir(ziph, path):
    #   for root, dirs, files in os.walk(path):
    #       for file in files: ziph.write(os.path.join(root, file))
    # 
    # print('==> CREATE: \'statik-{}.zip\''.format(name))
    # X = name.replace('.zip', '')  # os.path.basename(name)
    # with zipfile.ZipFile('statik-{}.zip'.format(name), "w", zipfile.ZIP_LZMA) as zip:
    #   zip.write(name, arcname=X)
    #   for N in files: zip.write(N, arcname=N)
    #   zip.close()

  @staticmethod
  def make_tarfile(*files, source=public_path, name=None):
    '''
    param: name is used given a single file-name.
    
    (full path hasn't been tested).

    param: source is the directory being archived.

    Takes input `name` (path) to create a directory within
    the tar.gz file so by default the target tar.gz archive will contain
    one directory: 'public', unless we start adding files.
    '''
    print('==> CREATE: \'statik-{}.tar.gz\''.format(name))

    E = ['.tar.gz', '.tgz']
    B = os.path.basename(Util.strip_ext(source, E))
    X = Util.strip_ext(name, E)         # os.path.basename(name)
    Y = Util.strip_ext(source, E)

    with tarfile.open('statik-{}.tar.gz'.format(X), "w:gz") as tar:
      tar.add(name, arcname=X)
      for N in files: tar.add(N, arcname=N)
      tar.close()

  @staticmethod
  def os_walk(prior, dir):
    '''
    return an array of all files (as to be contained)
    in a zip archvie (tar er whatever).
    '''
    for ROOT, DIRS, FILES in os.walk(os.path.abspath(dir)):
      for D in DIRS: Util.os_walk(prior, dir=os.path.join(ROOT,D))
      for F in FILES: prior.append(os.path.join(ROOT,F))
  
  @staticmethod
  def walk(prior, m_dir, m_search='*'):
    '''
    return an array of all files (as to be contained)
    in a zip archvie (tar er whatever).
    '''
    # print('current directory:', dir)
    m_glob = pathutil.mpath(os.path.abspath(m_dir), m_search)
    # print(m_dir)
    for X in glob.glob(m_glob, recursive=False):
      if os.path.isdir(X): Util.walk(prior, m_dir=X)
      else: prior.append(X)

  @staticmethod
  def ext(input):
    return os.path.splitext(input)[-1]

  @staticmethod
  def of_ext(prior:list, m_dir, m_glob='*', m_ext=None):
    '''
    return an array of all files (as to be contained)
    in a zip archvie (tar er whatever).
    '''
    # print('current directory:', dir)
    n_glob = pathutil.mpath(os.path.abspath(m_dir), m_glob)
    for X in glob.glob(n_glob):
      if os.path.isdir(X):
        Util.of_ext(prior, m_dir=X, m_glob=m_glob, m_ext=m_ext)
      else:
        ext = Util.ext(X.lower())
        if m_ext == None:
          prior.append(X)
        elif ext == m_ext:
          prior.append(X)
