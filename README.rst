Presentations
=============

Presentations using reveal.js.

.. code::

    present gen [-h] [-s SOURCE] -o OUTPUT [-f]

    optional arguments:
      -h, --help            show this help message and exit
      -s SOURCE, --source SOURCE
                            Path to a presentation file. If not specified, then the data will be read from stdin.
      -o OUTPUT, --output OUTPUT
                            Output slides file.
      -f, --force-overwrite
                            Overwrite existing files and directories if they already exist


Example
-------

.. code::

    config presentation
      title = Presentation Title

    config revealjs
      controls = true
      progress = true
      history = true
      center = true


    presentation

      slide
        h2 Slide 1 Caption

      slide
        h2 Slide 2 Caption
        fragment: h4 Fragment
