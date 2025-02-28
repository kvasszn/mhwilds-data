import os
import json
from typing import Dict
import mwclient
from dotenv import load_dotenv
import re

def wiki_init():
    load_dotenv()
    WIKI_USERNAME = os.getenv('WIKI_USERNAME')
    WIKI_PASSWORD = os.getenv('WIKI_PASSWORD')
    site = mwclient.Site('monsterhunterwiki.org', path='/')
    site.login(WIKI_USERNAME, WIKI_PASSWORD)
    return site

def send_pages(site: mwclient.Site, pages: Dict, summary):
    for (title, content) in pages.items():
        page = site.pages[title]
        page.save(content, summary=summary)
        print(f"Created page {title}")



class Parser2:
    def __init__(self, parse_func, msg_file_paths=[], base="", lang="English", msg_ext=".539100710.json"):
        self.msg_files = []
        self.msg_file_paths = msg_file_paths
        self.lang = lang
        self.base = base
        for file in msg_file_paths:
            f = open(os.path.join(base, file + msg_ext))
            x = json.load(f)
            self.msg_files.append(x)
        self.exec = parse_func

    def parse(self, *args):
        return self.exec(self, *args)

    def get_msg(self, value, lang=None):
        if lang is None:
            lang = self.lang

        entry = None
        for msg_file in self.msg_files:
            if guid := msg_file["name_to_uuid"].get(value):
                entry = msg_file["msgs"][guid]
        if entry is not None:
            entry = entry["content"][lang].replace("\r\n", " ").replace("<COL", "<span style=\"color:")
            entry = entry.replace("YEL", "yellow;")
            entry = entry.replace("RED", "red;")
            entry = entry.replace("BLU", "blue;")
            entry = entry.replace("GRE", "green;")
            entry = entry.replace("COL>", "span>")
            return entry.replace("\r\n", " ")

    def eval_ref(self, entry, lang=None):
        refs = re.search('<REF (.*)>', entry)
        if refs is None:
            return entry
        ref = refs.group(1)
        ref_msg = self.get_msg(ref, lang=lang)
        if ref_msg is None: 
            return entry
        entry = entry.replace(f"<REF {ref}>", ref_msg) 
        if "<REF" in entry:
            entry = self.eval_ref(entry, lang)
        return entry

    
    def get_msg_by_guid(self, guid, lang=None):
        if lang is None:
            lang = self.lang

        entry = None
        for msg_file in self.msg_files:
            if entry := msg_file["msgs"].get(guid):
                break

        if entry is not None:
            entry = entry["content"][lang]

            entry = self.eval_ref(entry, lang)
            if entry is None:
                return None

            entry = entry.replace("\r\n", " ").replace("<COL", "<span style=\"color:")
            entry = entry.replace("YEL", "yellow;")
            entry = entry.replace("RED", "red;")
            entry = entry.replace("BLU", "blue;")
            entry = entry.replace("GRE", "green;")
            entry = entry.replace("COL>", "span>")
            entry = entry.replace("\r\n", " ")
        return entry

    def get_msg_by_guid_all_langs(self, guid):
        entry = None
        for msg_file in self.msg_files:
            if entry := msg_file["msgs"].get(guid):
                break

        if entry is not None:
            entry = entry["content"]
            
            for k, v in entry.items():
                entry[k] = self.eval_ref(v, k)
                if entry[k] is None:
                    return None

                entry[k] = entry[k].replace("\r\n", " ").replace("<COL", "<span style=\"color:")
                entry[k] = entry[k].replace("YEL", "yellow;")
                entry[k] = entry[k].replace("RED", "red;")
                entry[k] = entry[k].replace("BLU", "blue;")
                entry[k] = entry[k].replace("GRE", "green;")
                entry[k] = entry[k].replace("COL>", "span>")
                entry[k] = entry[k].replace("\r\n", " ")
        return entry


    def get_msg_indexed(self, idx, hints=[], is_mr=False, lang=None):
        if lang is None:
            lang = self.lang

        entry = None
        for i, msg_file in enumerate(self.msg_files):
            if is_mr:
                if "_mr" != self.msg_file_paths[i].split(".")[-2][-3:]:
                    continue
            else:
                if "_mr" == self.msg_file_paths[i].split(".")[-2][-3:]:
                    continue

            vals = msg_file["name_to_uuid"].values()
            if idx < len(vals):
                msg_guid = list(vals)[idx]
                msg = msg_file["msgs"][msg_guid]
                good = True
                for hint in hints:
                    if hint not in msg["name"]:
                        good = False
                    if good:
                        entry = msg

        if entry is not None:
            entry = entry["content"][lang].replace("\r\n", " ").replace("<COL", "<span style=\"color:")
            entry = entry.replace("YEL", "yellow;")
            entry = entry.replace("RED", "red;")
            entry = entry.replace("BLU", "blue;")
            entry = entry.replace("GRE", "green;")
            entry = entry.replace("COL>", "span>")
            return entry.replace("\r\n", " ")


class Parser:
    def __init__(self, parse_func, msg_file_paths=[], base="", lang="English"):
        self.msg_files = []
        self.msg_file_paths = msg_file_paths
        self.lang = lang
        self.base = base
        for file in msg_file_paths:
            f = open(os.path.join(base, file + ".539100710.json"))
            x = json.load(f)
            self.msg_files.append(x)
        self.exec = parse_func

    def __call__(self, *args):
        return self.exec(self, *args)

    def get_msg(self, value, lang=None):
        if lang is None:
            lang = self.lang

        entry = None
        for msg_file in self.msg_files:
            if guid := msg_file["name_to_uuid"].get(value):
                entry = msg_file["msgs"][guid]
        if entry is not None:
            entry = entry["content"][lang].replace("\r\n", " ").replace("<COL", "<span style=\"color:")
            entry = entry.replace("YEL", "yellow;")
            entry = entry.replace("RED", "red;")
            entry = entry.replace("BLU", "blue;")
            entry = entry.replace("GRE", "green;")
            entry = entry.replace("COL>", "span>")
            return entry.replace("\r\n", " ")

    def get_msg_indexed(self, idx, hints=[], is_mr=False, lang=None):
        if lang is None:
            lang = self.lang

        entry = None
        for i, msg_file in enumerate(self.msg_files):
            if is_mr:
                if "_mr" != self.msg_file_paths[i].split(".")[-2][-3:]:
                    continue
            else:
                if "_mr" == self.msg_file_paths[i].split(".")[-2][-3:]:
                    continue

            vals = msg_file["name_to_uuid"].values()
            if idx < len(vals):
                msg_guid = list(vals)[idx]
                msg = msg_file["msgs"][msg_guid]
                good = True
                for hint in hints:
                    if hint not in msg["name"]:
                        good = False
                    if good:
                        entry = msg

        if entry is not None:
            entry = entry["content"][lang].replace("\r\n", " ").replace("<COL", "<span style=\"color:")
            entry = entry.replace("YEL", "yellow;")
            entry = entry.replace("RED", "red;")
            entry = entry.replace("BLU", "blue;")
            entry = entry.replace("GRE", "green;")
            entry = entry.replace("COL>", "span>")
            return entry.replace("\r\n", " ")
