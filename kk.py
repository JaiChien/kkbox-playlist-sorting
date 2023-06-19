
import json
import argparse
import xmltodict
import xml.etree.ElementTree as ET
from xml.dom import minidom


def createXMLByList(data_list, key, ele):
	for index, item_key in enumerate(data_list):
		temp = ET.SubElement(ele, key)
		for rel_key in data_list[index]:
			temp2 = ET.SubElement(temp, rel_key)
			temp2.text = data_list[index][rel_key]

			if rel_key in ["song_song_idx"]:
				# print("song_song_idx %s" % (index))
				temp2.text = str(index+1)
			else:
				temp2.text = data_list[index][rel_key]				

			# "song_artist","song_album"
			if rel_key in ["song_name"]:
				print(data_list[index][rel_key])

def createXMLByJSON(data, ele):
	for subkey in data:
		temp2 = ET.SubElement(ele, subkey)
		temp2.text = data[subkey]

def createXML(data, path='new.kbl'):
	root = ET.Element("utf-8_data")
	kkbox_package = ET.SubElement(root, "kkbox_package")

	kkbox_ver = ET.SubElement(kkbox_package, "kkbox_ver")
	kkbox_ver.text = data['utf-8_data']["kkbox_package"]['kkbox_ver']

	playlist = ET.SubElement(kkbox_package, "playlist")

	playlist_id = ET.SubElement(playlist, "playlist_id")
	playlist_id.text = data['utf-8_data']["kkbox_package"]['playlist']['playlist_id']

	playlist_name = ET.SubElement(playlist, "playlist_name")
	playlist_name.text = data['utf-8_data']["kkbox_package"]['playlist']['playlist_name']

	playlist_descr = ET.SubElement(playlist, "playlist_descr")
	
	playlist_data = ET.SubElement(playlist, "playlist_data")

	createXMLByList(
		data['utf-8_data']["kkbox_package"]['playlist']['playlist_data']['song_data'],
		"song_data",
		playlist_data
	)

	package = ET.SubElement(kkbox_package, "package")
	createXMLByJSON(data['utf-8_data']["kkbox_package"]['package'], package)

	tree = ET.ElementTree(root)
	
	ET.indent(tree, space="\t", level=0)
	tree.write(path, encoding="utf-8")
	# tree.write(path)

def sort_by( songs, key ):
	new_dict = dict()
	for song in songs:
		if song[ key ] not in new_dict:
			new_dict[ song[ key ] ] = list()
		new_dict[ song[ key ] ].append(song)

	sorted_song_data = list()
	for songs in new_dict:
		sorted_song_data = sorted_song_data + new_dict[songs]

	return sorted_song_data

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	parser.add_argument( "-p", "--filepath", help="Import File Path, ex. D://K.kbl", type=str )
	args = parser.parse_args()

	with open( args.filepath, "r", encoding="utf-8" ) as xml_file:
	    data_dict = xmltodict.parse(xml_file.read())

	print(len(data_dict['utf-8_data']['kkbox_package']['playlist']['playlist_data']['song_data']))

	sorted_song_data = sort_by(data_dict['utf-8_data']['kkbox_package']['playlist']['playlist_data']['song_data'], "song_artist")
	sorted_song_data = sort_by(data_dict['utf-8_data']['kkbox_package']['playlist']['playlist_data']['song_data'], "song_album")

	data_dict['utf-8_data']['kkbox_package']['playlist']['playlist_data']['song_data'] = sorted_song_data

	createXML(data_dict, args.filepath[:-4]+"-new.kbl")