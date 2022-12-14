import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path
from xml.dom import NotFoundErr
from chq.fs.ctxfile import CTXFile

from chq.fs.root import Root, get_initialized_default_root

CTX_FILENAME = ".ctx"
DEFAULT_KEY_LOCATION = {
    "ctf": "global",
    "chall": "ctf"
}
class CTX:
    _root: Root
    _ctx_dics: Dict[str, Dict[str, str]]
    _ctxfile_dic: Dict[str, CTXFile]
    key_location: Dict[str, str]
    def __init__(self) -> None:
        pass

    @property
    def root(self):
        return self._root
    @property
    def ctf(self):
        if "ctf" not in self:
            raise NotFoundErr('ctf')
        return self.root.get_ctf(self["ctf"])
    @property
    def chall(self):
        if "chall" not in self:
            raise NotFoundErr('chall')
        return self.ctf.get_chall(self["chall"])

    def _get_dict_and_file_from_key(self, key: str):
        if key not in self.key_location:
            raise KeyError(key)
        
        location = self.key_location[key]
        if location not in self._ctxfile_dic:
            raise NotFoundErr(f'{location} has not been set')
        
        return self._ctx_dics[location], self._ctxfile_dic[location]

    def __getitem__(self, key: str) -> str:
        ctx_dic, _ = self._get_dict_and_file_from_key(key)
        return ctx_dic[key]

    def set_and_save(self, key: str, val: str):
        ctx_dic, ctxfile = self._get_dict_and_file_from_key(key)
        ctx_dic[key] = val
        ctxfile.set_content(ctx_dic)

    def __contains__(self, key: str) -> bool:
        if key not in self.key_location:
            return False
        
        location = self.key_location[key]
        if location not in self._ctxfile_dic:
            return False
        return True

    @staticmethod
    def get(root: Root):
        try:
            ctx = CTX()
            ctx._root = root
            ctx._ctx_dics = {}
            ctx._ctxfile_dic = {}
            ctx.key_location = DEFAULT_KEY_LOCATION

            ctx._ctxfile_dic["global"] = ctx.root.ctxfile
            ctx._ctx_dics["global"] = ctx.root.ctxfile.get_content()
            if "global" not in ctx: return ctx
            
            ctx._ctxfile_dic["ctf"] = ctx.ctf.ctxfile
            ctx._ctx_dics["ctf"] = ctx.ctf.ctxfile.get_content()
            if "chall" not in ctx: return ctx
            
            ctx._ctxfile_dic["chall"] = ctx.chall.ctxfile
            ctx._ctx_dics["chall"] = ctx.chall.ctxfile.get_content()

            return ctx
        except:

            raise Exception("Error while reading the ctx from file")

