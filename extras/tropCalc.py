from birner import birner
from wmo import wmo
from coldestPoint import coldestPoint
from metpy.units import units
from wmo_nounit import f_wmo_nounit


def tropCalc(pFull, TFull, lapseC=2.0*units("K/km"), height=False, method="wmo"):
    if method == "birner":
        return birner(pFull,TFull,lapseC=lapseC,height=height)
    if method == 'wmo_nounit':
        return f_wmo_nounit(pFull, TFull, lapseC=lapseC, height=height)

    elif method == "cp":
        return coldestPoint(pFull,TFull,lapseC=lapseC,height=height)
    else:
        return wmo(pFull,TFull,lapseC=lapseC,height=height)

