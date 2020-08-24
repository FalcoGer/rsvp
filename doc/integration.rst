Integrating with your scripts
=============================

RSVP is designed with the following quality of life features to make it as straightforward as possible to use within your own scripts.

.. contents::
   :local:

Single Entrypoint
-----------------
There is only a single global ``rsvp`` variable as the entrypoint. All other functions, variables and delegates are locally scoped so that you don't have to worry about name collisions.

Flexible Location
-----------------
The library can be located anywhere as long as all script files are in the same directory. The suggested location is ``0:/rsvp``, however you are free to choose any other volume or path.

Compact Compilation
-------------------
To save space on the limited hard disks of kOS processors you can compile the source to ``.ksm`` files that are about 20% of the size of the raw source. A convenience ``rsvp:compile_to`` function exists for this purpose. For example, the following code will compile the source from the archive then copy the compiled files to the hard disk of the current processor.
::

    runoncepath("0:/rsvp/main").
    createdir("1:/rsvp").
    rsvp:compile_to("1:/rsvp").

Detailed Return Values
----------------------

Detailed return values indicate success or failure. The return value is a lexicon that will always have a top-level boolean ``success`` key. Check this value before proceeding with the rest of your script. For example, a successful result is:
::

    LEXICON of 3 items:
    ["success"] = True
    ["predicted"] = LEXICON of 2 items:
      ["departure"] = LEXICON of 2 items:
        ["time"] = 5055453.38357352
        ["deltav"] = 1036.59841185951
      ["arrival"] = LEXICON of 2 items:
        ["time"] = 10766955.6939971
        ["deltav"] = 642.186439333725
    ["actual"] = LEXICON of 2 items:
      ["departure"] = LEXICON of 2 items:
        ["time"] = 5055629.63357352
        ["deltav"] = 1056.03106245216
      ["arrival"] = LEXICON of 2 items:
        ["time"] = 10768356.5846979
        ["deltav"] = 647.973826829273

An example of a transfer with problems is:
::

    LEXICON of 2 items:
    ["success"] = False
    ["problems"] = LEXICON of 2 items:
      [1] = "Option 'verbose' is 'qux', expected boolean"
      [303] = "Option 'foo_bar' not recognised"