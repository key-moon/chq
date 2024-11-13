from pathlib import Path
from chq.ctx import CTX
from chq.util.path_normalize import normalize

def get_ctf_and_chall(ctx: CTX, dir: Path):
  root = ctx.root.path
  parents = [dir] + list(dir.parents)
  # [root]/ctf/chall
  while 3 <= len(parents):
    if parents[2] == root:
      ctf_name = parents[1].name
      chall_name = parents[0].name
      return normalize(ctf_name), normalize(chall_name)
    parents.pop(0)
  return normalize(ctx["ctf"]), normalize(ctx["chall"])

def get_ctf(ctx: CTX, dir: Path):
  root = ctx.root
  parents = [dir] + list(dir.parents)
  # [root]/ctf
  while 2 <= len(parents):
    if parents[1] == root:
      ctf_name = parents[0].name
      return normalize(ctf_name)
    parents.pop(0)
  return normalize(ctx["ctf"])
