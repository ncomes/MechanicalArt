#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains MCA Maya command plugin implementation
"""

from __future__ import print_function, division, absolute_import

import maya.cmds as cmds
import maya.api.OpenMaya

if not hasattr(maya.api.OpenMaya, '_MCA_COMMAND'):
    maya.api.OpenMaya._MCA_COMMAND = None
if not hasattr(maya.api.OpenMaya, '_MCA_COMMAND_RUNNER'):
    maya.api.OpenMaya._MCA_COMMAND_RUNNER = None


# mandatory to tell Maya that we are going to use OpenMaya 2.0
def maya_useNewAPI():
    pass


class UndoCommand(maya.api.OpenMaya.MPxCommand):
    """
    Custom undo command plugin that allow us to support the undo of custom Maya
    commands that uses both API and MEL code.
    """

    commandName = 'matUndoCmd'
    id = "-id"
    idLong = "-commandId"

    def __init__(self):
        super(UndoCommand, self).__init__()

        self._command = None
        self._command_runner = None
        self._command_name = ''

    @classmethod
    def command_creator(cls):
        return UndoCommand()

    @staticmethod
    def syntax_creator():
        syntax = maya.api.OpenMaya.MSyntax()
        syntax.addFlag(UndoCommand.id, UndoCommand.idLong, maya.api.OpenMaya.MSyntax.kString)
        return syntax

    def isUndoable(self):
        return self._command.is_undoable

    def doIt(self, args_list):
        parser = maya.api.OpenMaya.MArgParser(self.syntax(), args_list)
        command_id = parser.flagArgumentString(UndoCommand.id, 0)
        self._command_name = command_id
        self._command_runner = maya.api.OpenMaya._MCA_COMMAND_RUNNER
        if maya.api.OpenMaya._MCA_COMMAND is not None:
            self._command = maya.api.OpenMaya._MCA_COMMAND
            maya.api.OpenMaya._MCA_COMMAND = None
            self.redoIt()

    def redoIt(self):
        if self._command is None:
            return

        prev_state = cmds.undoInfo(stateWithoutFlush=True, q=True)

        try:
            if self._command.disable_queue:
                cmds.undoInfo(stateWithoutFlush=False)
            self._command_runner._call_do_it(self._command)
        finally:
            cmds.undoInfo(stateWithoutFlush=prev_state)

    def undoIt(self):
        if self._command is None:
            return

        stack = self._command_runner.undo_stack
        reversed_stack = list(reversed(stack))
        matched = False
        if not stack:
            self._command_runner.redo_stack.append(self._command)
            return

        index = 0
        prev_state = cmds.undoInfo(stateWithoutFlush=True, q=True)
        cmds.undoInfo(stateWithoutFlush=False)
        while not matched and index < len(reversed_stack):
            command = reversed_stack[index]
            if command.is_undoable:
                try:
                    command.undo_it()
                finally:
                    self._command_runner.undo_stack.pop()

            self._command_runner.redo_stack.append(command)
            if command.id == self._command.id:
                break
            index += 1
        cmds.undoInfo(stateWithoutFlush=prev_state)
