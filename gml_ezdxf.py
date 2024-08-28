import ezdxf
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.enums import TextEntityAlignment

import shapely as sh

class Drawing:
    def __init__(self, bdict: dict):
        self.doc = ezdxf.new("R2010")
        self.msp = self.doc.modelspace()
        self.bdict = bdict

    def add_points(self):

        bdict = self.bdict
        self.doc.layers.new("Punkty Graniczne")
        attribs = GfxAttribs(layer="Punkty Graniczne", color=1)
        align = TextEntityAlignment.LEFT
        properties = bdict['EGB_PunktGraniczny']

        for props in properties:

            number = ''
            x, y = 0.0, 0.0

            for key, val in props.items():
                if key == "idPunktu":
                    number = val

                if key == 'pos':
                    vl = [v for v in val.split(" ")]
                    x, y = float(vl[1]), float(vl[0]) if len(vl) == 2 else print('')

            self.msp.add_text(number, height=1, dxfattribs=attribs).set_placement((x, y), align=align)

    def add_poly_with_centroid(self, shortname=False):

        bdict = self.bdict
        self.doc.layers.new("Działki Ewidencyjne")
        attribs = GfxAttribs(layer="Działki Ewidencyjne", color=3)
        align = TextEntityAlignment.LEFT
        properties = bdict['EGB_DzialkaEwidencyjna']

        for props in properties:

            number = ''
            poli = []

            for key, val in props.items():
                if key == "idDzialki":
                    number = val.split(".")[-1] if shortname else val

                if key == 'posList' or key == 'pos':
                    vl = [v for v in val.split(" ")]

                    for k in range(0, len(vl), 2):
                        poli.append([float(vl[k+1]), float(vl[k])])

            self.msp.add_lwpolyline(poli, close=True, dxfattribs=attribs)
            self.msp.add_text(number, height=1, dxfattribs=attribs).set_placement(get_centroid(poli), align=align)



    def save(self, path: str) -> bool:
        try:
            if not path.endswith(".dxf"):
                path = path + ".dxf"
            self.doc.saveas(path)
        except:
            return False
        return True


def get_centroid(poli: list) -> tuple:
    centroid = sh.Polygon(poli).representative_point()
    return centroid.coords[:][0]


if __name__ == "__main__":
    pass
