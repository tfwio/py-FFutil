PyFFutil
===================

FFmpeg and AtomicParsley utility functions wrapped into a python script.

- requires FFmpeg.exe and AtomicParsley executables somewhere on ENVIRONMENT PATH to work.
- \_O\_o\_ if theres no *.cmd for the flag, I'm not sure if it works.
- couldn't be too much work to adapt this to \*nix or mac but I don't have either.
- don't think `--ff-update` \&| `--ff-check` options work...  
  was sort of playing around with the idea of auto-downloading FFmpeg and AtomicParsley, extracting, etc...
- create GIF from a movie
- other crappy utility scripts I was tinkering around with and didn't bother writing up here...

> IKNOW there are probably plenty of FF-scripts out there but I needet to brush up on my Py3.  Hadn't tinkered with it in over a decade until recent...

> Only thing I really use is the fixer for ID3 since I'm running WIN7 which doesn't display newer (common) ID3 thumbnails (via the `--id3v2` option) ---so I use the drag-drop script (drag multiple files into it) to regress the id3 tag so I can see pretty image-thumbnails.

> And I kind of like where the GIF writer thing is headed but it needs work.
  Feel free to file an issue to kick me into getting it working better, or
  FORK and fix it.  PRs are welcome.

feel free to bugreport any issue you'd like resolved or clarified!

license: do as you will with it

DEPENDENCIES (external ones)
--------------------

you know, from PIL...

- requests
- imageio (for making GIFs from movies)

Example Help Output
----------------------

```text
$ ./source/ff --help
usage: ff [-h] [--verbose] [--ff-update] [--ff-check] [--gif]
          [--gif-iframe GIF_NIDX] [--gif-fcount GIF_NLEN]
          [--gif-size GIF_SIZE] [--gif-fpsx GIF_FPSX] [--list-gif] [--clean]
          [--pix] [--dump] [--cover] [--cover-dump] [--cover-rm] [--enima]
          [--info] [--dump-meta] [--meta] [--id3v2] [--id3] [--audio]
          [file [file ...]]

:)

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v
  --ff-update           Download/update FFmpeg
  --ff-check            Download/update FFmpeg
  --gif                 Imageio makes a nice GIF for us.
  --gif-iframe GIF_NIDX
                        [see --gif] Number of indexes into the movie.
                        DEFAULT=20
  --gif-fcount GIF_NLEN
                        [see --gif] Number of frames to grab at each index
                        point. DEFAULT=10
  --gif-size GIF_SIZE   [see --gif] Size of the produced GIF window.".
                        DEFAULT=320x240
  --gif-fpsx GIF_FPSX   [see --gif] A multiplier applied to the GIF FPS.
                        DEFAULT=0.5
  --list-gif            [see --gif] Since we generate GIFs, lets try to find
                        them all starting at a given path.
  --clean               DELETE cover and metadata IF EXIST.
  --pix                 EXPORT cover image with AtomicParsley (if present).
  --dump, -d            EXPORT cover image and metadata.
  --cover, -c           IMPORT [file]-cover[.ext].
  --cover-dump, -C      EXPORT PNG cover image if one exists.
  --cover-rm, -crm      Remove cover [m4a, mp4] with AtomicParsley.
  --enima, -ae          Remove cover [m4a, mp4] with AtomicParsley.
  --info, -i            PRINT FFmpeg info(s).
  --dump-meta, -M       Dump FFmpeg Metadat-info(s).
  --meta, -m            IMPORT FFmpeg Metadat-info(s).
  --id3v2               Complete re-write of Metadata (DUMP) and Cover-art.
                        NOTE: This is for windows -id3v2 3
  --id3                 Override id3 v2.[x] (the 'x') with 2.4 perhaps.
  --audio, -a           Extract m4a audio from mp4 AV file with meta-data and
                        cover-image.
```

Python 2.7 Usage?
---------------------

These scripts are generally written to be used with 'current' Python 3.x (v3.7
at the time I've written this).

These scripts can be easily ported to v2.7 (e.g. v2.x) provided a small utility
script `./ff_2_py27` however the naming conventionality of the produced files
is not quite succinct and you have to rename the created files and perhaps place
them elsewhere or rename the files as 


Feature Commands
---------------------

The featured commands are provided to windows command scripts.

`-ae`, `-enima`
: Though the name is a bit mis-leading, the flags were at a time
  wrapping AtomicParsley's atomic-enima flag/feature.

  Now, it just removes the cover-art and strips the title from
  the input media file.

