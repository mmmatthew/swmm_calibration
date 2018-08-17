# swmm_calibration
A framework for calibrating SWMM models. Mostly built with other people's work:
- PYSWMM
- SPOTPY


# Changes to make to SPOTPY
At lines 156 of `algorithm.py`, replace
```
# use alt_objfun if alt_objfun is defined in objectivefunctions,
# else self.setup.objectivefunction
self.objectivefunction = getattr(
    objectivefunctions, alt_objfun or '', None) or self.setup.objectivefunction
```
with
```
# use objective function defined in spotpy setup
if spot_setup.objectivefunction is not None:
    self.objectivefunction = spot_setup.objectivefunction
else:
    # use alt_objfun if alt_objfun is defined in objectivefunctions,
    # else self.setup.objectivefunction
    self.objectivefunction = getattr(
        objectivefunctions, alt_objfun or '', None) or self.setup.objectivefunction
```