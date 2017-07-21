from kivy.properties import *
from kivy.event import EventDispatcher

class UndoRedoItem(object):
    def __init__(self,
                 do_action,
                 do_args,
                 do_kwargs,
                 undo_action,
                 undo_args,
                 undo_kwargs):

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
        if len(self.stack) > 0 and self.cursor < len(self.stack):
            self.stack = self.stack[self.cursor: len(self.stack)]
        self.stack.append(undoredo_item)
        self.cursor +=1
        self.check_can_undo()
        self.check_can_redo()
