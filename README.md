# test_free_inventory_tracker

DELAY : This can be manually done and put into a .fit file
- input a PYFA fitting block
  - [DONE] Save to ****.fit
    - Use Pyeasgygui to do this, it can do it rather well
  - [DONE] Update ***.fit
    - Use Pyeasgygui to do this, it can do it rather well
  - [DONE] The ***.fit file is read and dealt with appropriately


- [DONE] input a target count to keep assembled for each fit
  - [DONE] needs a way to edit. ATM needs to be done by hand.
    - [PROP] This will be a main menu item in the update section
      - Involve the generation of a text window using pyeasygui, which
        will then be populated with what is existing currently, then it
        can be edited and then confirmed. If invalid, return to dialog
        box.
  - [DONE] Can be a config file
    - [INFO] This is in the *.stn
- [TBD] count how many ships have the fit's name in a hangar (or text
  copied/pasted from a hangar) and compare against the target number
  - [DONE] Hangar is fetched via copy paste from game (No ESI, thank
    fuck)
    - [PROBLEM]Some parsing problems with some strings
      - [EXAMPLE]Fucking Kevin Spacey and his capsule
  - [DONE] Containers have to seen and interpreted
  - [ACCEPT] Accepted Limitation: Fit in fitted ship could be unknown
    and broken
  - Assumption: Properly named fit will be assumed to be fit properly
  - Assumption: user will copy paste all root hangars into main.cargo

- [TBD-50%] return how many of each fit to assemble
  - The program retrieves a fit and multiplies it by quantity required
  - Program does not take into account pre-existing ships
- [DONE] input a global fit multiplier for a packaged hull and fitting
  inventory surplus — "I want to be able to assemble this many times a
  fit's target number with my inventory on hand."
  - [DONE] Fits
    - Here is what is ready to be handed out
      - Currently have total values calculated, just need delta values
    - Here is what is ready to be fitted and then handed out
      - - Currently have total values calculated, just need delta values

    - [EXAMPLE] EG - 20x condors + fits, ready to go, another 20x in
      storage
- [DONE] count how many hulls and fittings are in containers (or pasted
  text)

  - [BUG] Fitting names sometimes bug out

- [DONE] input a global material multiplier for materials surplus — "I
  want to be able to build the assembled inventory and the inventory
  surplus this many times."
  - [DONE] Minerals required to make that
    - [DONE] Here is what is ready to be used to build an entire new set
      of ship+fits. - get blueprint materials for all used blueprints
      (assume zero research)
  - [DONE] Multiplies the global material multiplier with the global fit
    multiplier.
    - [EXAMPLE] EG. GFM -> 2x, GMM -> 2x, therefore 8x the minerals
      required for a given fit

- [DONE] Account for station (for class building)

- [DONE] use inventory surplus multiplier and materials surplus
  multiplier to calculate total materials target values
  - [REQ] Assume ME 0
- [DONE]count how many of each material is available in a container (or
  pasted text)
- [DONE]return materials deficits below materials target


- [TBD][PRIORITY - LOW] return which industry jobs to run to reach inventory targets
  - [PRIORITY - LOW]This is regarding how many job runs



# How to setup

- Folder (Station Name, must end with "*.stn", it is a JSON compatible
  file)
- Contains the following:
  - station name
  - config
    - GFM
    - GMM
  - Hangars
    - Date updated - Datetime ISO standard
    - contained items
      - name
      - quantity
      - volume
      - value (in isk)
    - Name of Hangar
    - Is it a hangar (or is it a container) --> True/False
  - Fits Required
    - "FIT NAME": $Quantity$


## Config file
There is no config file, part of *.stn  
Name Global Fitting Multiplier  
Global Material Multiplier


# Issues

For output files
- Required Items is used as a shipping tool
  - Volume should be implemented but can be done later (beyond scope)
  - Shipping report (beyond scope)
- Delta-Required/Existing Items needs to be added ( planned anyway)
  - Refer to link.note about this
- Delta-Required/Existing Fits need to be added
- Report conclusion should be up the top
- GUI managing this? (beyond scope)
- Fix Datetime when updating a hangar.
