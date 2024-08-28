import xml.etree.ElementTree as ET


clasic_keys ={"EGB_DzialkaEwidencyjna":
["idIIP",
"EGB_IdentyfikatorIIP",
"lokalnyId",
"przestrzenNazw",
"wersjaId",
"startObiekt",
"startWersjaObiekt",
"podstawaUtworzeniaWersjiObiektu",
"idDzialki",
"geometria",
"Polygon",
"LinearRing",
"pos",
"numerKW",
"poleEwidencyjne",
"dokladnoscReprezentacjiPola",
"klasouzytek",
"EGB_Klasouzytek",
"OFU",
"OZU",
"OZK",
"powierzchnia",
"JRG2",
"adresDzialki",
"punktGranicyDzialki",
"lokalizacjaDzialki"],
"EGB_UdzialWeWlasnosci": ["idIIP",
"EGB_IdentyfikatorIIP",
"lokalnyId",
"przestrzenNazw",
"wersjaId",
"startObiekt",
"startWersjaObiekt",
"podstawaUtworzeniaWersjiObiektu",
"rodzajPrawa",
"licznikUlamkaOkreslajacegoWartoscUdzialu",
"mianownikUlamkaOkreslajacegoWartoscUdzialu",
"podmiotUdzialuWlasnosci",
"EGB_Podmiot",
"osobaFizyczna",
"przedmiotUdzialuWlasnosci",
"EGB_JednostkaRejestrowa",
"JRG",
"dataNabycia",
"malzenstwo",
"podmiotGrupowy",
"instytucja1",
"JRB",
"JRL"
],
"EGB_WspolnotaGruntowa":
["nazwa",
"EGB_IdentyfikatorIIP",
"lokalnyId",
"przestrzenNazw",
"wersjaId",
"startObiekt",
"startWersjaObiekt",
"podstawaUtworzeniaWersjiObiektu",
"status",
"SpolkaZarzadajaca",
"osobaUprawniona"],
"EGB_PodmiotGrupowy":
["idIIP",
"EGB_IdentyfikatorIIP",
"lokalnyId",
"przestrzenNazw",
"wersjaId",
"startObiekt",
"startWersjaObiekt",
"podstawaUtworzeniaWersjiObiektu",
"nazwaPelna",
"nazwaSkrocona",
"regon",
"status",
"instytucja",
"osobaFizyczna4",
"malzenstwo3",
"adresPodmiotuGrupowego"]
}

from lxml import etree

def validate(xml_path: str, xsd_path: str) -> bool:

    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    return result

def read_dict(path):

    tree = ET.parse(path)
    root = tree.getroot()

    i = 5

    bdict = dict()
    tags = dict()

    for child in root:
        i += 1
        sdict = dict()
        # print(child.tag, child.attrib)
        tli = [elem.tag.split('}')[-1] for elem in child.iter()]
        ali = [elem.attrib for elem in child.iter()]
        j = 0
        name = ''
        for elem in child.iter():
            # print(j, elem.tag.split('}')[-1].strip(), elem.text)

            if j == 1:
                name = elem.tag.split('}')[-1].strip()
            if j < 2:
                j += 1
                continue
            else:
                j += 1

            if elem.text is not None:

                temp_tag = elem.tag.split('}')[-1].strip()
                val = elem.text.strip()

                if temp_tag in sdict.keys():
                    # print(type(sdict[temp_tag]), sdict[temp_tag])
                    """if type(sdict[temp_tag]) is not list:
                        sdict[temp_tag] = [sdict[temp_tag]]
                    sdict[temp_tag].append(val.strip())"""
                    sdict[temp_tag] = sdict[temp_tag] + " " + val.strip()
                else:
                    sdict[temp_tag] = val.strip()

                # sdict[elem.tag.split('}')[-1].strip()] = elem.text.strip()
            else:
                # sdict[elem.tag.split('}')[-1].strip()] = elem.attrib.values()

                for key, val in elem.items():
                    # print(key)
                    if 'type' in key:
                        continue
                    # print(type(val))
                    if val == 'true':
                        val = ''

                    temp_tag = elem.tag.split('}')[-1].strip()

                    if temp_tag in sdict.keys():

                        """if type(sdict[temp_tag]) is not list:
                            sdict[temp_tag] = [sdict[temp_tag]]
                        sdict[temp_tag].append(val.strip())"""

                        sdict[temp_tag] = sdict[temp_tag] + " " + val.strip()


                    else:

                        sdict[temp_tag] = val.strip()

                    break

        if len(name) > 31:
            name = name[:31]

        if name not in bdict.keys():
            bdict[name] = []

        if name not in tags.keys():
            tags[name] = set()

        if 'EGB_' in name:
            sdict['EGB_IdentyfikatorIIP'] = (sdict['przestrzenNazw'] + '_' + sdict['lokalnyId'] + '_' +
                                             sdict['wersjaId'].replace(":", "-"))

        for sd in sdict.keys():
            tags[name].add(sd)

        bdict[name].append(sdict)

    for key in clasic_keys.keys():
        for val in clasic_keys[key]:
            if key in tags.keys():
                tags[key].add(val)
            else:
                tags[key] = set(val)

    return bdict, tags

def get_gml_version(path):
    version = '2021'
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if 'PrezentacjaGraficzna' in line:
                version = '2021'
                break
            if 'ObiektKarto' in line:
                version = '2015'
                break
            if 'bt:BT_Identyfikator' in line:
                version = '2015'
                break
    return version

if __name__ == "__main__":
    xml_path = r"D:\Python\GML\xml-tree\gml\2021_03.gml"
    xsd_path = r"D:\Python\GML\xml-tree\resources\xsd\EGIB_1.9.xsd"
    xsd_path = r"C:\Users\BG-P\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\Walidator_plikow_gml/XSD/EGIB/EGIB_1.8.xsd"

    print(validate(xml_path, xsd_path))