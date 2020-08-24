Configuration
=============
The following options allow players to customize and tweak the desired transfer orbit. The general philosophy is that sensible defaults are provided for each option so that only custom values need to be provided. Specify options by adding them as key/value pairs to the ``options`` lexicon parameter.

.. contents::
   :local:

Verbose
-------
Prints comprehensive details to the kOS console if set to "True".

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``verbose``
     - False
     - Boolean

Create Maneuver Nodes
---------------------
Whether or not to create maneuver nodes that will execute the desired journey. The value "none" can be used for planning, the script will return details of the next transfer window.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``create_maneuver_nodes``
     - None
     - One of string values "none", "first" or "both"

Cleanup Maneuver Nodes
----------------------
If any problems are enountered when creating the transfer then remove and cleanup any maneuver nodes that have been created. Defaults to true but can be disabled for debugging purposes.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``cleanup_maneuver_nodes``
     - True
     - Boolean

Earliest Departure
------------------
When to start searching for transfer windows. Time can be in the vessel's past, present or future. The only restriction is that the time must be greater than the epoch time (Year 1, Day 1, 0:00:00)

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``earliest_departure``
     - Current universal time of CPU vessel plus 2 minutes
     - Seconds from epoch as scalar

Search Duration
---------------
Only search for transfer windows within the specified duration from earliest departure. Restricting the search duration can come in handy when time is of the essence. Increasing the duration may reveal a lower cost delta-v transfer to patient players.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``search_duration``
     - Maximum of origin orbital period, destination orbital period or their synodic period
     - Duration in seconds as scalar

Search Interval
---------------
How frequently new sub-searches are started within the search duration. Lower values may result in better delta-v values being discovered, however the search will take longer to complete.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``search_interval``
     - Half the minimum of origin orbital period and destination orbital period
     - Duration in seconds as scalar

Maximum time of flight
----------------------
Maximum duration of the transfer orbit between origin and destination. Some reasons it may come in useful to adjust this are life support mods, challenge requirements and career mode contract deadlines.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``max_time_of_flight``
     - Twice the time of a idealized Hohmann transfer between origin and destination
     - Duration in seconds as scalar

Final Orbit Periapsis
---------------------
Sets desired destination orbit periapsis in meters.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``final_orbit_periapsis``
     - 100,000m
     - Altitude in meters as scalar

Final Orbit Type
----------------
The insertion orbit can be one of three types:

* **None** Use when an aerocapture, flyby or extreme lithobraking is intended at the destination. When calculating the total delta-v the insertion portion is considered zero.
* **Circular** Capture into a circular orbit at the altitude specified by `final_orbit_periapsis`. Does not change inclination. If the origin and destination bodies are inclined then this orbit will be inclined too.
* **Elliptical** Capture into a highly elliptical orbit with apoapsis *just* inside the destination's SOI and periapsis at the altitude specified by `final_orbit_periapsis`. This can come in useful if the vessel will send a separate lander down to the surface or its intended to visit moons of the destination.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``final_orbit_type``
     - Circular
     - One of string values "none", "circular" or "elliptical"         

Final Orbit Orientation
-----------------------
The orbit orientation can be one of three types:

* **Prograde** Rotation of the final orbit will be the same as the rotation of the planet. Suitable for most missions.
* **Polar** Orbit will pass over the poles of the planet at 90 degrees inclination. Useful for survey missions.
* **Retrograde** Orbit will be the opposite to the rotation of the planet. An example use for this setting is solar powered craft that need to arrive on the daylight side of the planet.

.. list-table::
   :header-rows: 1

   * - Key
     - Default value
     - Accepted values
   * - ``final_orbit_orientation``
     - Prograde
     - One of string values "prograde", "polar" or "retrograde"

.. note::
   Vessel destinations are treated slightly differently to Celestial body destinations. Setting a vessel as the destination disables the ``final_orbit_periapsis``, ``final_orbit_type`` and ``final_orbit_orientation`` options.