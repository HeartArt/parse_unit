from unit.parser import create_unit_from_string

# angles
def hr_angle():
  return create_unit_from_string('hourangle')
def deg():
  return create_unit_from_string('degree')
def arcsec():
  return create_unit_from_string('arcsec')
def arcmin():
  return create_unit_from_string('arcmin')
def steradian():
  return create_unit_from_string('steradian')

# distance
def Mpc():
  return create_unit_from_string('Mpc')
def kpc():
  return create_unit_from_string('kpc')
def pc():
  return create_unit_from_string('pc')
def m():
  return create_unit_from_string('m')
def mm():
  return create_unit_from_string('mm')
def um():
  return create_unit_from_string('micron')

# frequency
def GHz():
  return reate_unit_from_string('GHz')
def Hz():
  return create_unit_from_string('Hz')

# speed
def kms():
  return create_unit_from_string('km/s')
def ms():
  return create_unit_from_string('m/s')

# brightness
def MJy():
  return create_unit_from_string('MJy')
def Jy():
  return create_unit_from_string('Jy')
def mJy():
  return create_unit_from_string('mJy')
def uJy():
  return create_unit_from_string('uJy')
def solLum():
  return create_unit_from_string('solLum')

# temperature
def K():
  return create_unit_from_string('K')

# mass
def solMass():
  return create_unit_from_string('solMass')
def kg():
  return create_unit_from_string('kg')

# time
def yr():
  return create_unit_from_string('yr')
def s():
  return create_unit_from_string('s')
