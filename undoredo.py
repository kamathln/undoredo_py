#!/usr/bin/python
# The MIT License (MIT)
# Copyright (c) 2017 "Laxminarayan Kamath G A"<kamathln@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from kivy.properties import *
from kivy.event import EventDispatcher

class UndoRedoItem(object):
    def __init__(self,
                 do_action = None,
                 do_args = None,
                 do_kwargs = None,
                 undo_action = None,
                 undo_args = None,
                 undo_kwargs = None,
                 complete = False
                 ):

        self.do_action = do_action
        self.do_args = do_args
        self.do_kwargs = do_kwargs
        self.undo_action = undo_action
        self.undo_args = undo_args
        self.undo_kwargs = undo_kwargs
    
    def undo(self):
        self.undo_action(*self.undo_args, **self.undo_kwargs)

    def redo(self):
        self.do_action(*self.do_args, **self.do_kwargs)

class UndoStack(EventDispatcher):
    stack = ListProperty([])
    cursor = NumericProperty(0)
    can_redo = BooleanProperty(False)
    can_undo = BooleanProperty(False)
    
    def undo(self):
        if not self.can_undo:
            return
        self.cursor -= 1
        self.stack[self.cursor].undo()
        self.check_can_undo()
        self.check_can_redo()
    
    def redo(self):
        if not self.can_redo:
            return
        self.stack[self.cursor].redo()
        self.cursor += 1
        self.check_can_undo()
        self.check_can_redo()
            
    def check_can_undo(self):
        self.can_undo = self.cursor > 0

    def check_can_redo(self):
        self.can_redo = self.cursor < len(self.stack)

    def register_action(self, undoredo_item):
        if not undoredo_item.complete:
            raise Exception("Incomplete UndoItem")

        if len(self.stack) > 0 and self.cursor < len(self.stack):
            self.stack = self.stack[self.cursor: len(self.stack)]
        self.stack.append(undoredo_item)
        self.cursor +=1
        self.check_can_undo()
        self.check_can_redo()
