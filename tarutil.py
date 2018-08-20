# !/usr/env/bash python3

import contextlib
import lzma
import os
import sys
import tarfile

# http://docs.python-requests.org/en/master/user/install/#install

try:
  import requests
except:
  print('requests module not found, from a command-line shell, try:')
  sys.exit('python -m pip install requests')

__is_verbose__ = False
__py_2x__ = sys.version_info[0] < 3
__py_3x__ = not __py_2x__
__refresh__ = True # A value of True tells us to destroy prior dowload archives.
__keep_archives__ = True
__original_path__ = os.path.abspath('.')

### tarutil.py
'''
This module is taken from another script and is probably dependent upon several things, or is by proxy.

Another way of looking at the above statement would be through my knowing that our usage of tarutil is from the context of urlutils or `purl`.

The other things that I'm aware of that would be useful here would be the file-system utilities such as listing files with a particular extension, and database operations which is scripted in other locations like the plex-playlist scripts that I've looked at a little bit.

'''

# extract tar.xz and tar.gz archive format(s)
class tarutil:
  
  @staticmethod
  def strip2(name):
    n = name
    if (name.endswith('.tar.gz')): n = n.replace('.tar.gz','')
    if (name.endswith('.tgz')): n = n.replace('.tgz','')
    if (name.endswith('.tar.xz')): n = n.replace('.tar.xz','')
    return n
  
  @staticmethod
  def untar_xz(file,target_dir='.'):
    if __py_3x__:
      with tarfile.open(file) as f:
        f.extractall(target_dir)
    else:
      with contextlib.closing(lzma.LZMAFile(file)) as xz:
        with tarfile.open(file) as f:
          f.extractall(target_dir)
  
  @staticmethod
  def untar_gz(file,target_dir='.'):
    tar = tarfile.open(file, "r:gz")
    tar.extractall()
    tar.close()

  @staticmethod
  def untar_xz2(file,target_dir='.'):
    tar = tarfile.open(file, "r:xz")
    tar.extractall()
    tar.close()

  @staticmethod
  def untar_tar(file, target_dir='.'):
    tar = tarfile.open(file, "r:")
    tar.extractall(target_dir)
    tar.close()

  @staticmethod
  def untar(file,target_dir='.'):
    print('  - extracting: %s' % file)
    
    if file.endswith('.tar'):
      if __is_verbose__: print('  - ext: .tar', file=sys.stderr)
      tarutil.untar_tar(file,target_dir)
      
    if file.endswith('.tar.xz'):
      if __is_verbose__: print('  - ext: .tar.xz', file=sys.stderr)
      tarutil.untar_xz(file,target_dir)
      
    elif file.endswith('.tar.gz') or file.endswith('.tgz'):
      if __is_verbose__: print('  - ext: .tar.gz', file=sys.stderr)
      tarutil.untar_gz(file,target_dir)
      
    else:
      _,ext = os.path.splitext(file)    
      print('  - ext: %s (unexpected)' % ext, file=sys.stderr)

class nurl:
  '''
  nurl is a class which has been taken from another script (getstuff.py).

  Somewhere within this python script should be defined a variable or PATH
  to which we download archive files as it is here that we place any download.

  wherever a path is referenced, we deal with absolute paths.
  '''
  name = None  # strip extension and file-version from target.
  target = None  # name of the archive (target) do download.
  target_abs = None  # absolute path to the target.
  target_dir = None  # __original_path__+'name'
  target_nam = None  # the name of the archive (without file extension)
  url = None  # input URI

  @staticmethod
  def get_name(target):
    '''
    The idea here is to strip out the version information from a traditional
    tar.gz archive so that only the name of the archive remains.
    '''
    ndx = target.find('-')
    if ndx > 0:
      return target[0:ndx]
    return target

  @staticmethod
  def get_filename(url):
    '''
    This method simply parses out a file-name from a given URI.
    Its designed speicifically for Source Forge downloads and detecting
    or rather removing the '/download' portion of the URI and is basically
    this filter in addition to the `os.path.basename` function.
    '''
    fname = url
    if fname.endswith('/download'):
      fname = fname.replace('/download', '')
    bname = os.path.basename(fname)
    return bname

  @staticmethod
  def get_filename_abs(url):
    '''
    Like the function's sibling `get_filename(url)`, this method
    gets the targeted file-name --- yet this method is designed
    to project a full path to the downloaded file.

    This method simply parses out a file-name from a given URI.
    Its designed speicifically for Source Forge downloads and detecting
    or rather removing the '/download' portion of the URI and is basically
    this filter in addition to the `os.path.abspath` function.
    '''
    fname = url
    if fname.endswith('/download'):
      fname = fname.replace('/download', '')
    bname = os.path.basename(fname)
    return os.path.abspath(bname)

  @staticmethod
  def has_key(response, key, get_key=False):
    for k in response.headers.keys():
      if (key == k):
        if (get_key):
          return response.headers[key]
        else:
          return True

    if get_key:
      return None
    return False

  @staticmethod
  def get_response_filename(URL, download=False):
    '''it appears that this method may be unfinished lest it merely contains erronious 'location' usage'''
    if download:
      r = requests.get(URL)
    else:
      r = requests.head(URL)

    print('- is: %s' % str(r))

    location = None
    if nurl.has_key(r, 'Location'):
      location = r.headers['Location']

    # print('- mode:    %s' % r.mode, file=sys.stderr)
    '''
    expected headers;
      
      - Content-Length
      - Location: if this is present, we're dealing with a redirect.
      - Content-Type:
          - application/octet-stream
          - text

    '''
    print('- headers: %s' % r.headers, file=sys.stderr)
  #
  def __init__(self, url):
    self.target_abs = nurl.get_filename_abs(url)
    self.target     = nurl.get_filename(url)
    self.url        = url
    self.name       = nurl.get_name(self.target)
    self.target_nam = tarutil.strip2(self.target)
    self.target_dir = os.path.abspath(__original_path__+'/'+self.name)

  # 
  def get_file(self):
    '''take in an item and get the frigging file!'''
    exists = os.path.isfile(self.target)
    delete_anyways = __refresh__ and (not __keep_archives__)
    if (os.path.isfile(self.target) and delete_anyways) or (not os.path.isfile(self.target)):
      if exists: deleting = ' (deleting first)'
      else: deleting = ''
      print('- downloading: \'%s\'%s' % (self.target,deleting))
      if exists: os.unlink(self.target)
      r = requests.get(self.url)
      nurl.to_file(r, self.target, True)
    else:
      print('- no need to download: \'%s\'' % self.target)
      return

  @staticmethod
  def to_file(response, filename, overwrite=False):
    '''
    write binary to file-name from response `r.iter_content`.
    
    we're not using overwrite in the class's non-static context (obviously).
    '''
    
    global __is_verbose__
    
    if os.path.isfile(filename) and overwrite:
      print('  - file \'%s\' exists; deleting' % filename)
      os.remove(filename)
    elif not os.path.isfile(filename):
      pass
    else:
      print('  - file \'%s\' exists; skipping' % filename)
      return
    
    with open(filename, 'wb') as fd:
      
      if nurl.has_key(response, 'Content-Length'):
        length = int(response.headers['Content-Length'])
      else:
        length = -1

      iter8  = int(1024 * 16 * 16)
      accum  = 0
      for chunk in response.iter_content(chunk_size=iter8):
        accum += iter8
        if __is_verbose__: print('  - writing: %s - %d of %d' % (filename, accum, length))
        fd.write(chunk)
