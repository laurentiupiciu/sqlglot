import typing as t
import sqlglot
from collections import defaultdict


def find_in_expression(expression, find, unquote=False):
  parts = [p for p in expression.find_all(find)]
  if unquote:
    for p in parts:
      identifiers = [i for i in p.find_all(sqlglot.exp.Identifier)]
      for i in identifiers:
        i.set('quoted', False)
  return parts


def get_table_aliases_in_query(expression: sqlglot.Expression, unquote=False) -> t.Dict:
  tables = find_in_expression(expression=expression, find=sqlglot.exp.Table, unquote=unquote)
  aliases = defaultdict(lambda: [])
  for tbl in tables:
    s = tbl.sql().replace('"', '')
    tokens = s.split(' AS ')
    if len(tokens) != 2:
      continue

    aliases[tokens[1]].append(tokens[0])
  #endfor

  keys = list(aliases.keys())
  for k in keys:
    aliases[k] = list(set(aliases[k]))

  return aliases
