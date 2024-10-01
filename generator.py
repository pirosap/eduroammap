import csv
import xml.etree.ElementTree as ET
from datetime import datetime

def csv_to_xml(institutions_csv, output_xml):
    root = ET.Element("institutions")
    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # institutions.csv を読み込み
    with open(institutions_csv, 'r', encoding='utf-8-sig') as inst_csvfile:
        inst_reader = csv.DictReader(inst_csvfile)
        
        for inst_row in inst_reader:
            institution = ET.SubElement(root, 'institution')
            ET.SubElement(institution, 'instid').text = inst_row['instid']
            ET.SubElement(institution, 'ROid').text = inst_row['ROid']
            ET.SubElement(institution, 'type').text = inst_row['type']
            ET.SubElement(institution, 'stage').text = inst_row['stage']
            ET.SubElement(institution, 'inst_realm').text = inst_row['inst_realm']
            ET.SubElement(institution, 'inst_name', lang='en').text = inst_row['inst_name_en']
            ET.SubElement(institution, 'inst_name', lang='ja').text = inst_row['inst_name_ja']
            ET.SubElement(institution, 'info_URL', lang='en').text = inst_row['info_URL_en']
            ET.SubElement(institution, 'info_URL', lang='ja').text = inst_row['info_URL_ja']
            ET.SubElement(institution, 'policy_URL', lang='en').text = inst_row['policy_URL_en']
            ET.SubElement(institution, 'policy_URL', lang='ja').text = inst_row['policy_URL_ja']
            ET.SubElement(institution, 'ts').text = ts

            # 各 instid に対応する CSV を読み込み
            location_csv = f"{inst_row['instid']}.csv"
            with open(location_csv, 'r', encoding='utf-8-sig') as loc_csvfile:
                loc_reader = csv.DictReader(loc_csvfile)
                
                for loc_row in loc_reader:
                    location = ET.SubElement(institution, 'location')
                    ET.SubElement(location, 'coordinates').text = loc_row.get('coordinates', '')
                    ET.SubElement(location, 'stage').text = '1'
                    ET.SubElement(location, 'type').text = '0'
                    ET.SubElement(location, 'loc_name', lang='en').text = loc_row.get('locnameen', '')
                    ET.SubElement(location, 'loc_name', lang='ja').text = loc_row.get('locnameja', '')
                    
                    address = ET.SubElement(location, 'address')
                    ET.SubElement(address, 'street', lang='en').text = loc_row.get('street lang="en"', '')
                    ET.SubElement(address, 'city', lang='en').text = loc_row.get('city lang="en"', '')
                    ET.SubElement(address, 'street', lang='ja').text = loc_row.get('street lang="ja"', '')
                    ET.SubElement(address, 'city', lang='ja').text = loc_row.get('city lang="ja"', '')
                    
                    contact = ET.SubElement(location, 'contact')
                    ET.SubElement(contact, 'name').text = inst_row['inst_name_ja']
                    ET.SubElement(contact, 'email').text = 'hoge@cityroam.jp'
                    ET.SubElement(contact, 'phone').text = '011-0000-0000'
                    ET.SubElement(contact, 'type').text = '1'
                    ET.SubElement(contact, 'privacy').text = '1'
                    
                    ET.SubElement(location, 'SSID').text = 'eduroam'
                    ET.SubElement(location, 'enc_level').text = 'WPA2/AES'
                    ET.SubElement(location, 'AP_no').text = '1'

    # XMLファイルにインデントを付けて書き込み
    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    indent(root)
    tree = ET.ElementTree(root)
    with open(output_xml, 'wb') as file:
        file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(file, encoding='utf-8', xml_declaration=False)

if __name__ == "__main__":
    csv_to_xml('institutions.csv', 'output.xml')

