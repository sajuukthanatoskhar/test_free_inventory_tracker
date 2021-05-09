# test_free_inventory_tracker

- input a PYFA fitting block
- input a target count to keep assembled for each fit
- count how many ships have the fit's name in a hangar (or text copied/pasted from a hangar) and compare against the target number
- return how many of each fit to assemble
- input a global multiplier for a packaged hull and fitting inventory surplus — "I want to be able to assemble this many times a fit's target number with my inventory on hand."
- count how many hulls and fittings are in containers (or pasted text)
- return which industry jobs to run to reach inventory targets
- input a multiplier for materials surplus — "I want to be able to build the assembled inventory and the inventory surplus this many times."
- get blueprint materials for all used blueprints (assume zero research)
- use inventory surplus multiplier and materials surplus multiplier to calculate total materials target values
- count how many of each material is available in a container (or pasted text)
- return materials deficits below materials target
