"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
# Qt imports
from mca.common.pyqt.pygui import qtcore, qtgui
# software specific imports
# mca python imports


def color_format(color, style=''):
	"""
	Return a qtgui.QTextCharFormat with the given attributes.

	:param str/list/tuple color: The string color or the RGBA color
	:param str style: Bold or italic
	:return: Return a qtgui.QTextCharFormat with the given attributes.
	:rtype: qtgui.QTextCharFormat
	"""
	
	_color = qtgui.QColor()
	if isinstance(color, (list, tuple)):
		_color.setRgb(color[0], color[1], color[2], color[3])
	elif isinstance(color, str):
		_color.setNamedColor(color)
	
	_format = qtgui.QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(qtgui.QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)
	
	return _format


# Syntax styles that can be shared by all languages
STYLES = {
	'keyword': color_format(color=(185, 128, 92, 255), style='bold'),
	'operator': color_format(color=(100, 130, 150, 255)),
	'brace': color_format(color=(232, 186, 54, 255)),
	'defclass': color_format(color=(139, 153, 198, 255)),
	'string': color_format(color=(206, 215, 74, 255)),
	'string2': color_format(color=(80, 155, 85, 255)),
	'comment': color_format(color=(0, 255, 53, 255), style='italic'),
	'self': color_format(color=(0, 255, 233, 255)),
	'numbers': color_format(color=(104, 151, 187, 255)),
	'built_in': color_format(color=(136, 136, 198, 255))
}


class PythonHighlighter(qtgui.QSyntaxHighlighter):
	"""
	Syntax highlighter for the Python language.
	"""
	
	# Python keywords
	keywords = [
		'and', 'assert', 'break', 'continue', 'class', 'def',
		'del', 'elif', 'else', 'except', 'exec', 'finally',
		'for', 'from', 'global', 'if', 'import', 'in',
		'is', 'lambda', 'not', 'or', 'pass', 'print',
		'raise', 'return', 'try', 'while', 'yield',
		'None', 'True', 'False'
	]
	
	built_in = [
		'tuple', 'list', 'str', 'dict'
	]
	
	# Python operators
	operators = [
		'=',
		# Comparison
		'==', '!=', '<', '<=', '>', '>=',
		# Arithmetic
		'\+', '-', '\*', '/', '//', '\%', '\*\*',
		# In-place
		'\+=', '-=', '\*=', '/=', '\%=',
		# Bitwise
		'\^', '\|', '\&', '\~', '>>', '<<',
	]
	
	# Python braces
	braces = [
		'\{', '\}', '\(', '\)', '\[', '\]',
	]
	
	def __init__(self, parent: qtgui.QTextDocument) -> None:
		super().__init__(parent)
		
		# Multi-line strings (expression, flag, style)
		try:
			self.tri_single = (qtcore.QRegExp("'''"), 1, STYLES['string2'])
			self.tri_double = (qtcore.QRegExp('"""'), 2, STYLES['string2'])
		except:
			self.tri_single = (qtcore.QRegularExpression("'''"), 1, STYLES['string2'])
			self.tri_double = (qtcore.QRegularExpression('"""'), 2, STYLES['string2'])

		rules = []
		
		# Keyword, operator, and brace rules
		rules += [(fr'\b{w}\b', 0, STYLES['keyword']) for w in PythonHighlighter.keywords]
		rules += [(fr'\b{w}\b', 0, STYLES['built_in']) for w in PythonHighlighter.built_in]
		rules += [(fr'{o}', 0, STYLES['operator']) for o in PythonHighlighter.operators]
		rules += [(fr'{b}', 0, STYLES['brace']) for b in PythonHighlighter.braces]
		
		# All other rules
		rules += [
			# 'self'
			(r'\bself\b', 0, STYLES['self']),
			(r'\bcls\b', 0, STYLES['self']),
			
			# 'def' followed by an identifier
			(r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
			# 'class' followed by an identifier
			(r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),
			
			# Numeric literals
			(r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
			
			# Double-quoted string, possibly containing escape sequences
			(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
			# Single-quoted string, possibly containing escape sequences
			(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
			
			# From '#' until a newline
			(r'#[^\n]*', 0, STYLES['comment']),
		]
		
		# Build a qtcore.QRegExp for each pattern
		try:
			self.rules = [(qtcore.QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]
		except:
			self.rules = [(qtcore.QRegularExpression(pat), index, fmt) for (pat, index, fmt) in rules]
	
	# This is an overwrite
	def highlightBlock(self, text):
		"""
		Apply syntax highlighting to the given block of text.

		:param str text: text that will get highlighted
		"""
		
		self.tripleQuoutesWithinStrings = []
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)
			if index >= 0:
				# if there is a string we check
				# if there are some triple quotes within the string
				# they will be ignored if they are matched again
				if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
					inner_index = self.tri_single[0].indexIn(text, index + 1)
					if inner_index == -1:
						inner_index = self.tri_double[0].indexIn(text, index + 1)
					
					if inner_index != -1:
						triple_quote_indexes = range(inner_index, inner_index + 3)
						self.tripleQuoutesWithinStrings.extend(triple_quote_indexes)
			
			while index >= 0:
				# skipping triple quotes within strings
				if index in self.tripleQuoutesWithinStrings:
					index += 1
					expression.indexIn(text, index)
					continue
				
				# We actually want the index of the nth match
				index = expression.pos(nth)
				length = len(expression.cap(nth))
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)
		
		self.setCurrentBlockState(0)
		
		# Do multi-line strings
		in_multiline = self.match_multiline(text, *self.tri_single)
		if not in_multiline:
			in_multiline = self.match_multiline(text, *self.tri_double)
	
	def match_multiline(self, text, delimiter, in_state, style):
		"""
		Do highlighting of multi-line strings.  Returns True if we're still
		inside a multi-line string when this function is finished.
		
		:param str text: text that will get highlighted
		:param qtcore.QRegExp delimiter: for triple-single-quotes or triple-double-quotes, and
		state changes when inside those strings
		:param int in_state: Unique integer to represent the corresponding
		:param qtgui.QTextCharFormat style: A Character Format
		:return: Return True if still inside a multi-line string, False otherwise
		:rtype: bool
		"""
		
		# If inside triple-single quotes, start at 0
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		# Otherwise, look for the delimiter on this line
		else:
			start = delimiter.indexIn(text)
			# skipping triple quotes within strings
			if start in self.tripleQuoutesWithinStrings:
				return False
			# Move past this match
			add = delimiter.matchedLength()
		
		# As long as there's a delimiter match on this line...
		while start >= 0:
			# Look for the ending delimiter
			end = delimiter.indexIn(text, start + add)
			# Ending delimiter on this line?
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			# No; multi-line string
			else:
				self.setCurrentBlockState(in_state)
				length = len(text) - start + add
			# Apply formatting
			self.setFormat(start, length, style)
			# Look for the next match
			start = delimiter.indexIn(text, start + length)
		
		# Return True if still inside a multi-line string, False otherwise
		if self.currentBlockState() == in_state:
			return True
		else:
			return False
