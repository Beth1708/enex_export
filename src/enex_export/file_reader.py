"""
Class to read a file using beautiful soup & return a tree of the data, where the data in the files looks like:
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
<en-export export-date="20230819T225323Z" application="Evernote" version="10.56.9">
  <note>
  <note>
    <title>Some title</title>
    <created>20211023T124017Z</created>
    <updated>20211023T124041Z</updated>
    <note-attributes>
      <source>web.clip</source>
      <source-url>https://bookriot.com/books-about-tudor-england/</source-url>
      <source-application>android.clipper.evernote</source-application>
    </note-attributes>
        </content>
    <resource>
      <data encoding="base64">
       ...
       </data>
      <mime>image/jpeg</mime>
      <width>467</width>
      <height>248</height>
      <resource-attributes>
        <file-name>bb4f74247aebabad237354aa24b3baad.jpg</file-name>
        <source-url>en-cache://tokenKey%3D%22AuthToken%3AUser%3A2119%22+b4dcf575-0ff0-454a-b281-176572c2e252+bf080afd10591377a398b218e2fd13e7+https://www.evernote.com/shard/s1/res/ea2aacaa-9472-40fc-9cad-49d37103c898</source-url>
      </resource-attributes>
    </resource>
  </note>
   for multiple notes

   The class has a parse method that takes a filepath & returns the xml content as a json list
"""

import os
from bs4 import BeautifulSoup
from typing import Dict, List


class EnexFileReader:
    def __init__(self):
        pass

    def parse(self, filepath: str) -> List[Dict]:
        assert os.path.exists(filepath), f"The file at {filepath} does not exist."

        with open(filepath, "r", encoding="utf-8") as file:
            contents = file.read()

        soup = BeautifulSoup(contents, "xml")

        notes = soup.find_all("note")

        note_list = []
        for note in notes:
            note_dict = {
                "title": note.title.text if note.title else None,
                "created": note.created.text if note.created else None,
                "updated": note.updated.text if note.updated else None,
                "content": note.content.text if note.content else None,
            }

            note_attr = note.find("note-attributes")
            if note_attr:
                note_dict["source"] = (
                    note_attr.source.text if note_attr.source else None
                )
                note_dict["source-url"] = (
                    note_attr.find("source-url").text
                    if note_attr.find("source-url")
                    else None
                )
                note_dict["source-application"] = (
                    note_attr.find("source-application").text
                    if note_attr.find("source-application")
                    else None
                )

            resource_list = note.findAll("resource")
            if resource_list:
                dict_resource_list = []
                note_dict["resource_list"] = dict_resource_list
                for resource in resource_list:
                    item_dict = {
                        "mime": resource.mime.text if resource.mime else None,
                        "width": resource.width.text if resource.width else None,
                        "height": resource.height.text if resource.height else None,
                        "data": resource.data.text if resource.data else None,
                    }

                    res_attr = resource.find("resource-attributes")
                    if res_attr:
                        item_dict["filename"] = (
                            res_attr.find("file-name").text
                            if res_attr.find("file-name")
                            else None
                        )
                    dict_resource_list.append(item_dict)

            note_list.append(note_dict)

        return note_list
