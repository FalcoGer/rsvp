Download & Quickstart
=====================
1. Go to the `GitHub Releases <https://github.com/maneatingape/rsvp/releases>`__ page, then download latest version of ``rsvp.zip``.
2. Unzip into ``<KSP install location>/Ships/Script`` directory. This step adds the library to the kOS archive volume, making it available to all vessels.
3. Launch a craft into a stable orbit of Kerbin.
4. Run this script from the craft::

    runoncepath("0:/rsvp/main").
    local options is lexicon("create_maneuver_nodes", "both", "verbose", true).
    rsvp:goto(duna, options).

This will find the next transfer window from Kerbin to Duna then create the corresponding maneuver nodes necessary to make the journey. Additionally it will print details to the console during the search.