import os
import shutil as s
import shapefile


def save_kontur_shp():
    # properties = bdict['EGB_DzialkaEwidencyjna']
    ...

def save_dz_shp(bdict, path):
    properties = bdict['EGB_DzialkaEwidencyjna']

    file_prefix = os.path.basename(path)

    dir_name = os.path.abspath(path)[:-len(os.path.basename(path))]

    epsg = None

    if not os.path.exists(f'{dir_name}shapefiles'):
        os.mkdir(f'{dir_name}shapefiles')



    with shapefile.Writer(f'{dir_name}shapefiles/{file_prefix}-dzialki_ewidencyjne', shapeType=shapefile.POLYGON) as w:
        w.field('id', 'C', 80)
        w.field('pow', 'C', 80)

        for props in properties:

            number = ''
            poli = []
            pow = None

            for key, val in props.items():
                if key == "idDzialki":
                    number = val

                if key == 'posList' or key == 'pos':
                    vl = [v for v in val.split(" ")]

                    for k in range(0, len(vl), 2):
                        # print(k)
                        poli.append([float(vl[k+1]), float(vl[k])])

                        if epsg is None:
                            epsg = find_epsg(vl[k+1])

                    # print(poli)
                if key == 'powierzchniaEwidencyjna' or key == 'poleEwidencyjne':
                    pow = val


            if len(poli) < 1:
                continue


            w.poly([poli])
            w.record(id=number, pow=pow)

    epsg_path = f'resources/epsg/{epsg}.prj'
    if epsg is not None and os.path.exists(epsg_path):
        s.copy(epsg_path, f'{dir_name}shapefiles/{file_prefix}-dzialki_ewidencyjne.prj')

    if os.path.exists('resources/qml/dzialki_ewidencyjne.qml'):
        s.copy('resources/qml/dzialki_ewidencyjne.qml',
               f'{dir_name}shapefiles/{file_prefix}-dzialki_ewidencyjne.qml')

def save_pts_shp(bdict, path, version):
    properties = bdict['EGB_PunktGraniczny']

    epsg = None
    file_prefix = os.path.basename(path)
    dir_name = os.path.abspath(path)[:-len(os.path.basename(path))]

    if not os.path.exists(f'{dir_name}shapefiles'):
        os.mkdir(f'{dir_name}shapefiles')



    with shapefile.Writer(f'{dir_name}shapefiles/{file_prefix}-punkty_graniczne', shapeType=shapefile.POINT) as w:

        if version == "2015":
            w.field('id', 'C', 80)
            w.field('ZRD', 'N')
            w.field('BPP', 'N')
            w.field('STB', 'N')
        else:
            w.field('id', 'C', 80)
            w.field('SPD', 'N')
            w.field('ISD', 'N')
            w.field('STB', 'N')

        for props in properties:

            number = ''
            x, y = 0.0, 0.0

            zrd, bpp, stb, spd, isd = None, None, None, None, None


            for key, val in props.items():
                if key == "idPunktu":
                    number = val

                if key == 'pos':
                    vl = [v for v in val.split(" ")]

                    if len(vl) == 2:
                        x = float(vl[1])
                        y = float(vl[0])

                if version == "2015":

                    if key == 'zrodloDanychZRD':
                        if val != '':
                            zrd = int(val)

                    if key == 'bladPolozeniaWzgledemOsnowy':
                        if val != '':
                            bpp = int(val)

                    if key == 'kodStabilizacji':
                        if val != '':
                            stb = int(val)
                else:
                    if key == 'sposobPozyskania':
                        if val != '':
                            spd = int(val)

                    if key == 'spelnienieWarunkowDokl':
                        if val != '':
                            isd = int(val)

                    if key == 'rodzajStabilizacji':
                        if val != '':
                            stb = int(val)
            w.point(x, y)

            if epsg is None:
                epsg = find_epsg(x)

            if version == "2015":
                w.record(id=number, ZRD=zrd, BPP=bpp, STB=stb)
            else:
                w.record(id=number, SPD=spd, ISD=isd, STB=stb)

    epsg_path = f'resources/epsg/{epsg}.prj'
    if epsg is not None and os.path.exists(epsg_path):
        s.copy(epsg_path, f'{dir_name}shapefiles/{file_prefix}-punkty_graniczne.prj')

    if os.path.exists('resources/qml/punkty_graniczne.qml'):
        s.copy('resources/qml/punkty_graniczne.qml',
               f'{dir_name}shapefiles/{file_prefix}-punkty_graniczne.qml')

def find_epsg(x):
    value = str(x)[0]

    match value:
        case '5':
            return 'epsg-2176'
        case '6':
            return 'epsg-2177'
        case '7':
            return 'epsg-2178'
        case '8':
            return 'epsg-2178'
        case _:
            return None


if __name__ == "__main__":
    ...