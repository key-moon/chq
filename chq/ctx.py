from typing import Dict, Optional
from chq.fs.ctxfile import CTXFile

from chq.fs.root import Root

CTX_FILENAME = ".ctx"
DEFAULT_KEY_LOCATION = {
    "ctf": "global",
}
class CTX:
    _root: Root
    _ctx_dics: Dict[str, Dict[str, str]]
    _ctxfile_dic: Dict[str, CTXFile]
    known_key: Dict[str, str]
    def __init__(self) -> None:
        pass

    @property
    def root(self):
        return self._root
    @property
    def ctf(self):
        if "ctf" not in self:
            raise KeyError('ctf')
        return self.root.get_ctf(self["ctf"])

    def _get_dict_and_file_from_key(self, key: str):
        if key not in self.known_key:
            raise KeyError(key)
        
        location = self.known_key[key]
        if location not in self._ctxfile_dic:
            raise KeyError(location)
        
        return self._ctx_dics[location], self._ctxfile_dic[location]

    def __getitem__(self, key: str) -> str:
        ctx_dic, _ = self._get_dict_and_file_from_key(key)
        return ctx_dic[key]

    def set_and_save(self, key: str, val: Optional[str]):
        ctx_dic, ctxfile = self._get_dict_and_file_from_key(key)
        if val is None:
            del ctx_dic[key]
        else:
            ctx_dic[key] = val
        ctxfile.set_content(ctx_dic)
        self.update()

    def update(self):
        if self._root is None:
            raise Exception()
        try:
            self._ctxfile_dic = {}
            self._ctx_dics = {}
            self._ctxfile_dic["global"] = self.root.ctxfile
            self._ctx_dics["global"] = self.root.ctxfile.get_content()
            if "ctf" not in self: return
        except:
            raise Exception("Error while reading the ctx from file")

    def __contains__(self, key: str) -> bool:
        if key not in self.known_key:
            return False
        location = self.known_key[key]
        if location not in self._ctx_dics:
            return False
        if key not in self._ctx_dics[location]:
            return False
        return True

    @staticmethod
    def get(root: Root):
        ctx = CTX()
        ctx._root = root
        ctx.known_key = DEFAULT_KEY_LOCATION
        ctx.update()
        return ctx
