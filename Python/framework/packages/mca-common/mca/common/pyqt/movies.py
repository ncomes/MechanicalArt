'''
purpose: Play gifs and movies in pyside.
'''

# python imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui
# Software specific imports
# mca imports


class MovieLabel(qtwidgets.QLabel):
	"""
	Creates a qtgui.QMovie using a .gif embedded in a qtwidgets.QLabel.
	"""

	def __init__(self, ag_file, speed=100, parent=None):
		super().__init__(parent)
		self.setMouseTracking(True)
		movie = qtgui.QMovie(ag_file, qtcore.QByteArray(), self)
		self.setMovie(movie)
		self.movie().setCacheMode(qtgui.QMovie.CacheAll)
		self.movie().setSpeed(speed)
		self.movie().start()
		self.show()


class GifToolButton(qtwidgets.QToolButton):
	"""
	Creates a qtgui.QMovie using a .gif embedded in a Button.
	"""

	def __init__(self, file_name, size=(100, 100), parent=None):
		"""
		:param str file_name: The path to the gif file.
		:param tuple size: The size of the button. (Width, Height)
		"""

		super().__init__(parent)
		self.size = list(size)  # Width, Height

		self.setIcon(qtgui.QIcon())
		self.movie = qtgui.QMovie(file_name, qtcore.QByteArray(), self)
		self.movie.frameChanged.connect(self.update_movie_icon)
		self.movie.setCacheMode(qtgui.QMovie.CacheAll)
		self.movie.setSpeed(100)

		self.setMinimumSize(self.size[0], self.size[1])

		self.movie.start()

	def update_movie_icon(self):
		"""
		sets the Pixmap for the icon.
		"""

		self.setText("")
		self.setIcon(qtgui.QIcon(self.movie.currentPixmap()))
		self.setIconSize(qtcore.QSize(self.size[0], self.size[1]))


class GifHoverToolButton(GifToolButton):
	"""
	Creates a qtgui.QMovie using a .gif embedded in a Button.  Starts the movie when the mouse enters the button.
	"""
	def __init__(self, file_name, size=(100, 100), parent=None):
		"""
		:param str file_name: The path to the gif file.
		:param tuple size: The size of the button. (Width, Height)
		"""

		super().__init__(file_name=file_name, size=size, parent=parent)
		self.movie.stop()

	def enterEvent(self, event):
		"""
		Starts the movie when the mouse enters the button.
		"""

		self.movie.start()

	def leaveEvent(self, event):
		"""
		Stops the movie when the mouse leaves the button.
		"""

		self.movie.stop()
