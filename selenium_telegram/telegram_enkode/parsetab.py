
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'DATE_TIME GROUP INDEX PRECIPITATION\n    groups : group groups\n           | group\n           | empty\n    \n    data : INDEX DATE_TIME groups PRECIPITATION \n    \n    group : GROUP\n    \n    empty :\n    '
    
_lr_action_items = {'GROUP':([0,2,4,],[4,4,-5,]),'$end':([0,1,2,3,4,5,],[-6,0,-2,-3,-5,-1,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'groups':([0,2,],[1,5,]),'group':([0,2,],[2,2,]),'empty':([0,2,],[3,3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> groups","S'",1,None,None,None),
  ('groups -> group groups','groups',2,'p_groups','parser_gidro.py',141),
  ('groups -> group','groups',1,'p_groups','parser_gidro.py',142),
  ('groups -> empty','groups',1,'p_groups','parser_gidro.py',143),
  ('data -> INDEX DATE_TIME groups PRECIPITATION','data',4,'p_data','parser_gidro.py',159),
  ('group -> GROUP','group',1,'p_group','parser_gidro.py',177),
  ('empty -> <empty>','empty',0,'p_empty','parser_gidro.py',217),
]
