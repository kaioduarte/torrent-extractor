import re
from requests import get
from bs4 import BeautifulSoup
from collections import OrderedDict


def get_torrents(url: str) -> OrderedDict:
  response = get(url)
  if not response.ok:
    return None

  soup = BeautifulSoup(response.text, "lxml")
  parents = OrderedDict()
  parents_bs = [t.parent for t in soup.find_all(href=re.compile("magnet"))]

  if not parents_bs:
    return None

  for i in range(len(parents_bs)):
    if parents_bs[i] not in parents.values():
      parents[str(i)] = parents_bs[i]

  for key, value in parents.items():
    parents[key] = [tag.attrs["href"]
                    for tag in value.findChildren(href=re.compile("magnet"))]
  return parents
