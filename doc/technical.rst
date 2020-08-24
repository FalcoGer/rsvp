Technical Details
=================

Each script file is thoroughly commented to describe both what the code is doing, but also more importantly *why*. The section titles on this page links to the relevant source file.

.. contents::
   :local:

`Lambert Solver <https://github.com/maneatingape/rsvp/blob/master/src/lambert.ks>`__
------------------------------------------------------------------------------------
The core functionality is built around a `Lambert's problem <https://en.wikipedia.org/wiki/Lambert%27s_problem>`__ solver. Given the position of two planets and a duration, this calculates the delta-v required for a transfer orbit between the two positions that will take exactly that duration.

The Lambert solver code is a kOS port of the `PyKep project <https://github.com/esa/pykep>`__ developed by the European Space Agency. The algorithm and equations are described in excellent detail in the paper `Revisiting Lambert’s problem <https://www.esa.int/gsp/ACT/doc/MAD/pub/ACT-RPR-MAD-2014-RevisitingLambertProblem.pdf>`__ by Dario Izzio.

The original code is very robust and flexible. For the KSP universe some simplifications have been made, in particular multi-revolution transfer orbits are not considered. Interestingly, the Kerboscript code is more concise than the C++ original, thanks to first class support for vector math and the exponent operator, coming in at around 100 lines not including comments.

`Porkchop Plot Search <https://github.com/maneatingape/rsvp/blob/master/src/search.ks>`__
-----------------------------------------------------------------------------------------
Graphing the delta-v values returned by the Lambert solver, with departure time along the x-axis and arrival time (or time of flight) along the y-axis, yields the famous `porkchop plot <https://en.wikipedia.org/wiki/Porkchop_plot>`__. This shows the lowest delta-v transfer times between two planets.

However the brute force approach of generating every point of this graph would take far too long on kOS. Instead an `iterated local search <https://en.wikipedia.org/wiki/Iterated_local_search>`__ gives a decent probability of finding the global minimum in a shorter time.

Simple heuristics based on the origin and destination orbits provide sensible defaults for the search parameters. These parameters can be overriden by the user for fine-grained control.

`Coordinate Descent <https://github.com/maneatingape/rsvp/blob/master/src/hill_climb.ks>`__
-------------------------------------------------------------------------------------------
The `coordinate descent <https://en.wikipedia.org/wiki/Coordinate_descent>`__ implementation used by RSVP is a variant of the classic `hill climbing <https://en.wikipedia.org/wiki/Hill_climbing>`__ algorithm. Given a starting point, it always attempts to go "downhill" to a region of lower value, stopping once it cannot go any further. The algorithm is completely general purpose and flexible, taking an arbitrary "cost" function, for example delta-v magnitude or distance to periapsis. The implementation can search up to three dimensions, however currently only the one and two dimensional variants are used.

`Orbital Utilities <https://github.com/maneatingape/rsvp/blob/master/src/orbit.ks>`__
-------------------------------------------------------------------------------------
Toolkit of functions related to orbital mechanics that:
* Use the `vis-viva equation <https://en.wikipedia.org/wiki/Vis-viva_equation>`__ to calculate the delta-v between elliptical orbits and hyperbolic transfers, in order to determine the ejection and insertion delta-v values.
* Calculate projected `orbital state vectors <https://en.wikipedia.org/wiki/Orbital_state_vectors>`__ for planets and vessels at any time.
* Determine the amount that planets bend hyperbolic trajectories to determine both the correct ejection angle.
* Provide default value for the time of flight based on the `Hohmann transfer <https://en.wikipedia.org/wiki/Hohmann_transfer_orbit>`__ period.
* Provide default value for search duration based on `Synodic period <https://en.wikipedia.org/wiki/Orbital_period#Synodic_period>`__.
* Determine the time at periapsis using the Keplerian orbital parameters and the formula for `mean anomaly <https://en.wikipedia.org/wiki/Mean_anomaly>`__.

`Transfer <https://github.com/maneatingape/rsvp/blob/master/src/transfer.ks>`__
-------------------------------------------------------------------------------
Takes the raw search information returned by `search.ks` then uses it to create initial maneuver nodes. The maneuver nodes are then refined using feedback loops that depend on the specific situation.

There are four situations:

* **Vessel to Vessel** *(asteroids and comets also count as vessels)*
    Vessel to vessel transfers within the same `SOI <https://en.wikipedia.org/wiki/Sphere_of_influence_(astrodynamics)>`__ are the most straightforward case. The values from the Lambert solver are accurate enough to be used directly with no modifications, resulting in very precise intercepts, even over interplanetary distances.
* **Vessel to Body**
    The initial Vessel to Body transfer is *too* accurate, resulting in a transfer that collides dead center with the destination. An ``orbit.ks`` function returns the impact parameter, that is the distance that we should offset in order to miss by roughly our desired periapsis. This is used as an inital value to a feedback loop, where the value is refined until the projected orbit is very close (to within 1%) of the target figure.
* **Body to Vessel**
    The transfer velocities returned by the raw search make some simplifying assumptions. The vessel is assumed to leave from a point at exactly the center of the planet and the affect of the planet's gravity are not taken into account. To refine the initial transfer, a feedback loop measures the projected velocity of the vessel just at the moment it leaves the origin planet's SOI, then re-runs the Lambert solver to calculate what it should actually be. This error is applied to the original maneuver node, then the procedure repeats until the error drops below a threshold, resulting in a much more accurate transfer.
* **Body to Body**
    The previous two approaches are combined when travelling from planet to planet. Firstly the body-to-vessel feedback loop is used to create a transfer that hits the destination planet dead center. Then the impact parameter and desired final orbit orientation are combined to calculate an offset from the planet in order to "miss" by the right amount in the right direction. Finally the transfer feedback loop is re-run with this new offset, resulting in a good approximation to the final desired orbit.

`Maneuver Node Helper <https://github.com/maneatingape/rsvp/blob/master/src/maneuver.ks>`__
--------------------------------------------------------------------------------------------
Wrapper around a raw kOS maneuver node that provides methods to predict details of future encounters. Projected arrival time and arrival velocity at the moment the ship enters an SOI are used to calculate the impact parameter and also used in the `transfer.ks` feedback loop refinement. Projected periapsis time and periapsis altitude are used to create arrival maneuver nodes at a destination body.

`Parameter Validation <https://github.com/maneatingape/rsvp/blob/master/src/validate.ks>`__
-------------------------------------------------------------------------------------------
Checks that the types and values of user-supplied options match expectations. Additionally checks that the desired transfer is possible and reasonable, then also sanity checks that the save game actually allows maneuver nodes and flight planning (if career mode). Accumulates descriptive error messages to assist and guide the user. As this library is intended to be used within other scripts, the goal is to catch as much as possible up front then fail fast, rather than fail later with a difficult to understand stack trace.

`Entrypoint <https://github.com/maneatingape/rsvp/blob/master/src/main.ks>`__
-----------------------------------------------------------------------------
Loads all the other scripts, then orchestrates the high level logic flow. When loading other scripts, the kOS ``scriptpath`` function is used so that the library can be located anywhere the user wants. To prevent pollution of the global namespace, all functions are scoped local then loaded into the ``rsvp`` lexicon, so that there is only a single external interface.

`Refine <https://github.com/maneatingape/rsvp/blob/master/src/refine.ks>`__
---------------------------------------------------------------------------
Compose several orbital sub-functions to build the overall "cost" function used when searching the porkchop plot. The most important difference is between point-to-point transfers and soi-to-soi transfers.

Point to point transfers treat the origin and destination as zero-width points and only use a single invocation of the Lamber solver for each point on the plot.

SOI to SOI transfers take the spherical nature of the source and destination into account and run the Lambert solver multiple times, refining the position and time of the transfer for more accuracy. However as this is slower, it is only used when the ration of a body's SOI to its periapsis exceeds a threshold.