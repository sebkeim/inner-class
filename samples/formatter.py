import sys
sys.path.append('..')

from inner import class_inner

class EarthPoint :
    latitude  : float
    longitude : float
  
    def __init__(self,latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

    def __str__(self):
        fmt = self.formatter()
        return fmt.as_str(self)
             
    @class_inner
    class formatter:
        def as_str(self, v):
            ns,ew = "NS"[v.latitude<0],"EW"[v.longitude<0]
            return f"{abs(v.latitude):.4f}{ns} {abs(v.longitude):.4f}{ew}"

        def _parse(self, s, card):
            value,c = float(s[:-1]), s[-1].upper()
            sign =(1,-1)[card.index(c)]
            return sign*value
        def from_str(self , geostr):
             s = geostr.split()
             if len(s)!=2:
                 raise ValueError("invalid string")
             latitude = self._parse(s[0], "NS")
             longitude = self._parse(s[1], "EW")
             return  self.outer(latitude, longitude)


# formatting
Paris = EarthPoint(48.866667, 2.333333)
print(str(Paris))

# parsing
fmt = EarthPoint.formatter()
geo = fmt.from_str('48.8667N 2.3333E')
print(geo)
