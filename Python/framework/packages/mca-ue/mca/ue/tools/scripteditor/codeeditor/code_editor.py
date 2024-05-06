# -*- coding: utf-8 -*-

"""
This is the editor part of the script editor
"""

# mca python imports
# Qt imports
# software specific imports
# mca python imports

from PySide2 import QtCore, QtGui, QtWidgets

from mca.common import log

logger = log.MCA_LOGGER


class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self._code_editor = editor

    def sizeHint(self):
        return QtCore.QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_editor.lineNumberAreaPaintEvent(event)


class CodeTextEdit(QtWidgets.QPlainTextEdit):
    is_first = False
    pressed_keys = list()

    indented = QtCore.Signal(object)
    unindented = QtCore.Signal(object)
    commented = QtCore.Signal(object)
    uncommented = QtCore.Signal(object)
    dup_lines = QtCore.Signal(object)
    run_command = QtCore.Signal(object)
    save_tab = QtCore.Signal(object)
    return_command = QtCore.Signal(object)
    add_tab = QtCore.Signal(object)

    def __init__(self):
        super(CodeTextEdit, self).__init__()

        self.indented.connect(self.do_indent)
        self.unindented.connect(self.undo_indent)
        self.commented.connect(self.do_comment)
        self.uncommented.connect(self.undo_comment)
        self.dup_lines.connect(self.do_duplicate_lines)
        self.run_command.connect(self.do_run_command)
        self.save_tab.connect(self.do_save)
        self.return_command.connect(self.new_line_return)
        self.add_tab.connect(self.add_tab_command)

    def clear_selection(self):
        """
        Clear text selection on cursor
        """
        pos = self.textCursor().selectionEnd()
        self.textCursor().movePosition(pos)

    def get_all_lines(self):
        start_line = 0
        end_line = self.blockCount()
        return [start_line, end_line]

    def get_curser_position(self):
        cursor = self.textCursor()
        y = cursor.blockNumber()
        x = cursor.columnNumber()
        return [y, x]

    def get_selection_range(self):
        """
        Get text selection line range from cursor
        Note: currently only support continuous selection
        :return: (int, int). start line number and end line number
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            y = cursor.blockNumber()
            # x = cursor.columnNumber()
            return [y, y]

        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()

        cursor.setPosition(start_pos)
        start_line = cursor.blockNumber()
        cursor.setPosition(end_pos)
        end_line = cursor.blockNumber()

        return start_line, end_line

    def remove_line_start(self, string, line_number):
        """
        Remove certain string occurrence online start
        :param string: str. string pattern to remove
        :param line_number: int. line number
        """
        cursor = QtGui.QTextCursor(
            self.document().findBlockByLineNumber(line_number))
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        if text.startswith(string):
            cursor.removeSelectedText()
            cursor.insertText(text.split(string, 1)[-1])

    def insert_line_start(self, string, line_number):
        """
        Insert certain string pattern online start
        :param string: str. string pattern to insert
        :param line_number: int. line number
        """
        cursor = QtGui.QTextCursor(
            self.document().findBlockByLineNumber(line_number))
        self.setTextCursor(cursor)
        self.textCursor().insertText(string)

    def comment_line(self, line_number):
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        cursor.removeSelectedText()

        if text[:2] == '# ':
            text = text.replace('# ', '', 1)
            self.insert_line_start(text, line_number)
        elif text[:1] == '#':
            text = text.replace('#', '', 1)
            self.insert_line_start(text, line_number)
        else:
            self.insert_line_start(f'# {text}', line_number)

    def duplicate_line(self, line_number):
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        cursor.removeSelectedText()
        self.insert_line_start(f'{text}\n{text}', line_number)

    def do_run_command(self):
        if not self.window():
            return
        self.window().execute_sel()

    def save_tab_file(self):
        if not self.window():
            return
        self.window().save_script()

    def add_tab_command(self):
        if not self.window():
            return

        index = self.window().ui.ui_tab_widget.count() - 1
        self.window().insert_tab(index, '', 'Python')

    def keyPressEvent(self, event):
        """
        Extend the key press event to create key shortcuts
        """
        self.is_first = True
        self.pressed_keys.append(event.key())
        start_line, end_line = self.get_selection_range()

        # indent event
        if event.key() == QtCore.Qt.Key_Tab:
            lines = range(start_line, end_line+1)
            self.indented.emit(lines)
            return

        # un-indent event
        elif event.key() == QtCore.Qt.Key_Backtab:
            lines = range(start_line, end_line+1)
            self.unindented.emit(lines)
            return

        # Enter Do Command event
        elif event.key() == QtCore.Qt.Key_Enter:
            lines = range(start_line, end_line + 1)
            self.run_command.emit(lines)
            return

        # Enter Do return event
        elif event.key() == QtCore.Qt.Key_Return:
            lines = range(start_line, end_line + 1)
            self.return_command.emit(lines)
            return

        super(CodeTextEdit, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """
        Extend the key release event to catch key combos
        """
        if self.is_first:
            self.process_multi_keys(self.pressed_keys)

        self.is_first = False
        self.pressed_keys.pop()
        super(CodeTextEdit, self).keyReleaseEvent(event)

    def process_multi_keys(self, keys):
        """
        Placeholder for processing multiple key combo events
        :param keys: [QtCore.Qt.Key]. key combos
        """
        start_line, end_line = self.get_selection_range()
        # toggle comments indent event
        lines = range(start_line, end_line + 1)
        if keys == [QtCore.Qt.Key_Control, QtCore.Qt.Key_Slash]:
            self.commented.emit(lines)
        elif keys == [QtCore.Qt.Key_Control, QtCore.Qt.Key_D]:
            self.dup_lines.emit(lines)
        elif keys == [QtCore.Qt.Key_Control, QtCore.Qt.Key_Return]:
            self.run_command.emit(lines)
        elif keys == [QtCore.Qt.Key_Control, QtCore.Qt.Key_S]:
            self.save_tab.emit(lines)
        elif keys == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Tab]:
            self.unindented.emit(lines)
        elif keys == [QtCore.Qt.Key_Control, QtCore.Qt.Key_T]:
            self.add_tab.emit(lines)

    def convert_all_to_spaces(self):
        start_line, end_line = self.get_all_lines()
        lines = range(start_line, end_line + 1)
        for line in lines:
            cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line))
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            text = cursor.selectedText()
            cursor.removeSelectedText()
            text = text.replace('\t', '    ')
            self.insert_line_start(f'{text}', line)

    def convert_all_to_tabs(self):
        start_line, end_line = self.get_all_lines()
        lines = range(start_line, end_line + 1)
        for line in lines:
            cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line))
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            text = cursor.selectedText()
            cursor.removeSelectedText()
            text = text.replace('    ', '\t')
            self.insert_line_start(f'{text}', line)

    def new_line_return(self):   ############### Todo ncomes.  Needs a lot of work.  Must be a better way
        key_words = ['def', 'class', 'if', 'else', 'elif']

        curser_pos = self.get_curser_position()
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(curser_pos[0]))
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        key_word_found = False
        split_text = text.split(' ')
        long_split = (text.split())
        if long_split and ':' in long_split[-1]:
            self.textCursor().insertText('\n    ')
            return
        for word in key_words:
            if word in split_text:
                key_word_found = True
                self.textCursor().insertText('\n    ')
                break
        if not key_word_found:
            self.textCursor().insertText('\n')

    def do_indent(self, lines):
        """
        Indent lines
        :param lines: [int]. line numbers
        """

        cursor = self.textCursor()
        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()

        selection = sel_start - sel_end

        if selection == 0:
            self.textCursor().insertText('    ')
            return

        for line in lines:
            self.insert_line_start('    ', line)

    def undo_indent(self, lines):
        """
        Un-indent lines
        :param lines: [int]. line numbers
        """
        for line in lines:
            self.remove_line_start('    ', line)

    def do_comment(self, lines):
        """
        Comment out lines
        :param lines: [int]. line numbers
        """
        for line in lines:
            self.comment_line(line)

    def do_duplicate_lines(self, lines):
        """
        Comment out lines
        :param lines: [int]. line numbers
        """
        for line in lines:
            self.duplicate_line(line)

    def undo_comment(self, lines):
        """
        Un-comment lines
        :param lines: [int]. line numbers
        """
        for line in lines:
            pass

    def do_save(self, lines):
        """
        Un-comment lines
        :param lines: [int]. line numbers
        """
        self.save_tab_file()


class CodeEditor(CodeTextEdit):
    def __init__(self):
        super(CodeEditor, self).__init__()
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)

        self.line_number_area = LineNumberArea(self)

        self.font = QtGui.QFont()
        self.font.setFamily("Consolas")
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.tab_size = 4
        self.setTabStopWidth(self.tab_size * self.fontMetrics().width(' '))

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 20 + self.fontMetrics().width('9') * digits
        return space

    def resizeEvent(self, e):
        super(CodeEditor, self).resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QtCore.QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        BACKGROUND_COLOR = QtGui.QColor(21, 21, 21)
        LINENUMBER_COLOR = QtGui.QColor(200, 200, 200)

        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), BACKGROUND_COLOR)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(LINENUMBER_COLOR)
                width = self.line_number_area.width() - 10
                height = self.fontMetrics().height()
                painter.drawText(
                    0,
                    int(top),
                    int(width),
                    int(height),
                    QtCore.Qt.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def update_line_number_area_width(self, new_block_count):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
