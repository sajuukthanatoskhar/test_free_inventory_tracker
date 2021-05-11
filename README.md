# test_free_inventory_tracker

DELAY : This can be manually done and put into a .fit file
- input a PYFA fitting block
  - Save to ****.fit
  - Update ***.fit
  - The ***.fit file is read and dealt with appropriately


- input a target count to keep assembled for each fit
  - Can be a config file
- count how many ships have the fit's name in a hangar (or text copied/pasted from a hangar) and compare against the target number
  - Hangar is fetched via copy paste from game (No ESI, thank fuck)
  - Containers have to seen and interpreted
  - Accepted Limitation: Fit in fitted ship could be unknown and broken
  - Assumption: Properly named fit will be assumed to be fit properly
  - Assumption: user will copy paste all root hangars into main.cargo

- return how many of each fit to assemble
  - How many r-click multifits from target number
- input a global fit multiplier for a packaged hull and fitting
  inventory surplus — "I want to be able to assemble this many times a
  fit's target number with my inventory on hand."
  - Fits
    - Here is what is ready to be handed out
    - Here is what is ready to be fitted and then handed out

  - EG - 20x condors + fits, ready to go, another 20x in storage
- count how many hulls and fittings are in containers (or pasted text)

- input a global material multiplier for materials surplus — "I want to
  be able to build the assembled inventory and the inventory surplus
  this many times."
  - Minerals required to make that
    - Here is what is ready to be used to build an entire new set of
      ship+fits. - get blueprint materials for all used blueprints
      (assume zero research)
  - Multiplies the global material multiplier with the global fit
    multiplier.
    - EG. GFM -> 2x, GMM -> 2x, therefore 8x the minerals required for a
      given fit

- Account for station (for class building)

- use inventory surplus multiplier and materials surplus multiplier to calculate total materials target values
  - Assume ME 0
- count how many of each material is available in a container (or pasted text)
- return materials deficits below materials target


- return which industry jobs to run to reach inventory targets