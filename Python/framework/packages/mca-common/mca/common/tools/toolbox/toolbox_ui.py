"""
Toolbox main UI
"""

# python imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore
# software specific imports
# mca python imports
from mca.common.pyqt import common_windows, movies
from mca.common.resources import resources
from mca.common.utils import dcc_util
from mca.common.tools.toolbox import toolbox_data, toolbox_prefs
from mca.common import log

logger = log.MCA_LOGGER
TOOLBOX_PREFS = None


class ToolboxGui(common_windows.MCADockableWindow):
    VERSION = '3.0.1'

    def __init__(self, toolbox_class, style=None, dcc_app=None, is_floating=False, area='left', single_insta=True, parent=None):
        self.tbm = toolbox_class

        toolbox_name = toolbox_class.toolbox_name
        if dcc_app:
            TOOLBOX_P = toolbox_prefs.ToolBoxPreferences(toolbox=toolbox_name, dcc=dcc_app)
            is_floating = not TOOLBOX_P.start_docked
        super().__init__(ui_path=None,
                         title=toolbox_name,
                         version=self.VERSION,
                         style=style,
                         isfloating=is_floating,
                         area=area,
                         single_insta=single_insta,
                         parent=parent)
        
        global TOOLBOX_PREFS

        self.toolbox_name = toolbox_name
        if not dcc_app:
            dcc_app = dcc_util.application()

        # Get the Toolbox Preferences.  This gets the state of the toolbar buttons and checkboxes.
        TOOLBOX_PREFS = toolbox_prefs.ToolBoxPreferences(toolbox=self.toolbox_name, dcc=dcc_app)
        
        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
        self.setMinimumHeight(600)
        self.setMinimumWidth(300)

        self.main_v_layout = qtwidgets.QVBoxLayout()
        self.main_v_layout.setObjectName(f'MainVerticalLayout')
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.main_v_layout)

        # Main UI
        # Filter Layout
        self.filter_layout = qtwidgets.QHBoxLayout()
        self.filter_layout.setContentsMargins(0, 4, 0, 1)
        self.filter_layout.setObjectName(f'FilterLayout')
        self.main_v_layout.addLayout(self.filter_layout)

        # Filter Label
        self.filter_label = qtwidgets.QLabel('  Filter: ')
        self.filter_label.setContentsMargins(0, 0, 0, 0)
        self.filter_label.setMinimumHeight(25)
        self.filter_label.setMaximumHeight(25)
        self.filter_label.setObjectName(f'FilterLabel')
        self.filter_layout.addWidget(self.filter_label)

        # Filter Line Edit
        self.filter_edit = qtwidgets.QLineEdit()
        self.filter_edit.setContentsMargins(2, 0, 2, 0)
        self.filter_edit.setMinimumHeight(25)
        self.filter_edit.setMaximumHeight(25)
        self.filter_edit.setMinimumWidth(80)
        self.filter_edit.setObjectName(f'FilterLineEdit')
        self.filter_layout.addWidget(self.filter_edit)

        self.movie_file = movies.MovieLabel(ag_file=resources.movie('glitch_logo_small_02'),
                                            parent=self)
        self.movie_file.setObjectName(u"movie_logo")
        self.movie_file.setFixedSize(25, 22)
        self.movie_file.setAlignment(qtcore.Qt.AlignCenter)
        self.filter_layout.addWidget(self.movie_file)
        self.movie_file.setContentsMargins(0, 2, 4, 0)

        # self.main_h_layout = qtwidgets.QHBoxLayout()
        # self.main_h_layout.setContentsMargins(0, 4, 0, 4)
        # self.main_h_layout.setObjectName(f'MainHorizontalLayout')
        # self.main_v_layout.addLayout(self.main_h_layout)

        self.scroll_area = qtwidgets.QScrollArea()
        self.scroll_area.setObjectName(f'MainScrollFrame')
        self.scroll_area.setFrameStyle(qtwidgets.QFrame.WinPanel | qtwidgets.QFrame.Sunken)
        self.scroll_area.setContentsMargins(0, 0, 4, 0)
        # self.scroll_area.setMinimumHeight(735)
        self.scroll_area.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
        self.scroll_area.setVerticalScrollBarPolicy(qtcore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(qtcore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.main_v_layout.addWidget(self.scroll_area)

        self.scrollAreaWidgetContents = qtwidgets.QWidget(self.scroll_area)
        self.scrollAreaWidgetContents.setMinimumWidth(250)
        self.scrollAreaWidgetContents.setMinimumHeight(1700)
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        # Create the layout that has all of the toolbar buttons and actions.
        self.v_layout = qtwidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.v_layout.setObjectName(f'CategoryVerticalLayout')
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaWidgetContents.setLayout(self.v_layout)

        # Create the info box at the bottom of the toolbox
        self.infobox_layout = qtwidgets.QHBoxLayout()
        self.infobox_layout.setContentsMargins(4, 4, 4, 4)
        self.infobox_layout.setObjectName(f'InfoBoxLayout')
        self.main_v_layout.addLayout(self.infobox_layout)

        self.infobox_v_layout = qtwidgets.QVBoxLayout()
        self.infobox_v_layout.setContentsMargins(4, 4, 4, 4)
        self.infobox_v_layout.setObjectName(f'InfoVBoxLayout')
        self.infobox_layout.addLayout(self.infobox_v_layout)

        # self.v_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Minimum, qtwidgets.QSizePolicy.Expanding)
        # self.infobox_v_layout.addItem(self.v_spacer)

        # self.description_label = qtwidgets.QLabel()
        # self.description_label.setText('Description:')
        # self.description_label.setStyleSheet("font-weight: bold")
        # self.infobox_v_layout.addWidget(self.description_label)
        #
        # self.info_box = qtwidgets.QTextEdit()
        # self.info_box.setContentsMargins(4, 4, 4, 4)
        # self.info_box.setObjectName(f'InfoBox')
        # self.info_box.setMinimumHeight(100)
        # self.info_box.setMaximumHeight(100)
        # self.info_box.setReadOnly(True)
        # self.info_box.setAlignment(qtcore.Qt.AlignLeft)
        # self.info_box.setVerticalScrollBarPolicy(qtcore.Qt.ScrollBarAlwaysOff)
        # self.info_box.setText('')
        # self.infobox_v_layout.addWidget(self.info_box)

        self.startup_layout = qtwidgets.QHBoxLayout()
        self.startup_layout.setContentsMargins(4, 0, 8, 4)
        self.startup_layout.setObjectName(f'StartLayout')
        self.main_v_layout.addLayout(self.startup_layout)

        self.on_start_checkBox = qtwidgets.QCheckBox()
        self.on_start_checkBox.setText('Open on Startup')
        self.on_start_checkBox.setObjectName(f'OnStartupCheckBox')
        self.on_start_checkBox.setContentsMargins(4, 0, 0, 4)
        self.on_start_checkBox.setLayoutDirection(qtcore.Qt.RightToLeft)
        self.on_start_checkBox.setCheckable(True)
        self.startup_layout.addWidget(self.on_start_checkBox)

        self.startup_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Minimum)
        self.startup_layout.addItem(self.startup_spacer)

        self.docked_checkBox = qtwidgets.QCheckBox()
        self.docked_checkBox.setText('Start Docked')
        self.docked_checkBox.setObjectName(f'DockedCheckBox')
        self.docked_checkBox.setContentsMargins(0, 0, 8, 4)
        self.docked_checkBox.setLayoutDirection(qtcore.Qt.RightToLeft)
        self.docked_checkBox.setCheckable(True)
        self.startup_layout.addWidget(self.docked_checkBox)

        # Adds the categories and actions.  Note: These get added to the self.v_layout.
        # The layout in the middle of the toolbox
        self.build_toolbox_ui()

        # Start watching events
        self.installEventFilter(self)

        # Set startup Widgets
        self.on_start_checkBox.setChecked(TOOLBOX_PREFS.on_start)
        self.docked_checkBox.setChecked(TOOLBOX_PREFS.start_docked)

        ###############################
        # Signals
        ###############################
        self.filter_edit.returnPressed.connect(self.filter_actions)
        self.docked_checkBox.clicked.connect(self.set_docked)
        self.on_start_checkBox.clicked.connect(self.set_on_start)

    ###############################
    # Slots
    ###############################
    def set_docked(self):
        """
        Sets the checkbox preferences to either docked or not when opened.
        """

        TOOLBOX_PREFS.start_docked = self.docked_checkBox.isChecked()
        TOOLBOX_PREFS.write_file()

    def set_on_start(self):
        """
        Sets the checkbox preferences to either Open toolbox when dcc opens.
        """

        TOOLBOX_PREFS.on_start = self.on_start_checkBox.isChecked()
        TOOLBOX_PREFS.write_file()

    def filter_actions(self):
        """
        Filters the actions
        """

        self.remove_all_categories()
        self.build_toolbox_ui()
        self.filter_edit.setFocus()

        children = self.findChildren(TBUI)
        if not children:
            return
        for child in children:
            # print(child)
            child.update()
            child.repaint()

    def _get_build_order(self):
        build_order_dict = self.tbm.get_build_order()
        filter_text = self.filter_edit.text()
        split_list = filter_text.lower().split(' ')
        include_list = []
        exclude_list = []
        for x in split_list:
            # Setup our filter lists.
            if x.startswith('-'):
                exclude_list.append(x[1:])
            else:
                include_list.append(x)

        if include_list or exclude_list:
            build_order_dict = self._filter_build_list(build_order_dict, include_list, exclude_list)

        return build_order_dict

    def _filter_build_list(self, partial_build_dict, include_list, exclude_list):
        # Some filtering checks.
        keep_build_dict = False
        build_entry = partial_build_dict['toolbox_class']
        return_dict = {'toolbox_class': build_entry}
        # Do we filter only actions or actions and categories?
        if isinstance(build_entry, toolbox_data.ToolboxAction):
            if any(True if x in build_entry.display_name.lower() else False for x in include_list):
                keep_build_dict = True
            if any(True if x in build_entry.display_name.lower() else False for x in exclude_list):
                keep_build_dict = False

        for child_build_dict in partial_build_dict.get('children', []):
            # For each of the children registered here check for filters if we find any we keep this portion of the build dict. If not we discard it.
            child_build_dict = self._filter_build_list(child_build_dict, include_list, exclude_list)
            if child_build_dict:
                if 'children' not in return_dict:
                    return_dict['children'] = []
                keep_build_dict = True
                return_dict['children'].append(child_build_dict)

        if keep_build_dict:
            return return_dict
        return {}

    def get_category(self, category_id):
        """
        Returns the Category qtwidgets.QFrame using the id.

        :param str category_id: String name/id of the category
        :return: Returns the Category qtwidgets.QFrame using the id.
        :rtype: qtwidgets.QFrame
        """

        category = self.findChild(qtwidgets.QFrame, category_id)
        return category

    def get_category_tool_button(self, category_id):
        """
        Returns the qtwidgets.QToolButton using the category id.

        :param str category_id: String name/id of the category
        :return: Returns the qtwidgets.QToolButton using the category id.
        :rtype: qtwidgets.QToolButton
        """

        button_id = f'{category_id}_toolButton'
        button = self.findChild(qtwidgets.QToolButton, button_id)
        return button

    def get_category_frame(self, category_id):
        """
        Returns a categories sub qtwidgets.QFrame using the category id.

        :param str category_id: String name/id of the category
        :return: Returns a categories sub qtwidgets.QFrame using the category id.
        :rtype: qtwidgets.QFrame
        """

        frame_id = f'{category_id}_frame'
        frame = self.findChild(qtwidgets.QFrame, frame_id)
        return frame

    def get_category_layout(self, category_id):
        """
        Returns a categories sub qtwidgets.QHBoxLayout using the category id.

        :param str category_id: String name/id of the category
        :return: Returns a categories sub qtwidgets.QHBoxLayout using the category id.
        :rtype: qtwidgets.QHBoxLayout
        """

        layout_id = f'{category_id}_category_layout'
        layout = self.findChild(qtwidgets.QVBoxLayout, layout_id)
        return layout

    def get_layout(self, layout_id):
        """
        Returns an actions qtwidgets.QHBoxLayout using the layout id.

        :param str layout_id: String name/id of the layout
        :return: Returns an actions qtwidgets.QHBoxLayout using the layout id.
        :rtype: qtwidgets.QHBoxLayout
        """

        layout_id = f'{layout_id}_layout'
        layout = self.findChild(qtwidgets.QHBoxLayout, layout_id)
        return layout

    def build_toolbox_ui(self):
        """
        We're going to get the filter build order associated with this toolbox and build out all categories/layouts/actions

        """
        build_order_dict = self._get_build_order()
        for child_entry in build_order_dict.get('children'):
            # From the root entry find all childen and add them to the main layout.
            self._build_ui(child_entry, self.v_layout)

        self.vertical_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Minimum, qtwidgets.QSizePolicy.Expanding)
        self.v_layout.addItem(self.vertical_spacer)

    def _build_ui(self, partial_build_dict, parent):
        """
        Recursive build function. When passed an ordered build dict it will recursively generate UI elements.

        :param dict partial_build_dict: A formatted build dictionary containing toolbox data classes, and their children.
        :param QUiClass parent: A Q ui element the build objects should be parented to.
        """
        toolbox_data_class = partial_build_dict.get('toolbox_class')
        if not isinstance(toolbox_data_class, toolbox_data.ToolboxAction) and not partial_build_dict.get('children'):
            # If we do not have an action. (We have a category or layout) and it has no children. Skip this build as
            # the category or layout will be empty.
            logger.warning(f'Category or layout has no children and will not be built.')
            return

        if not parent:
            logger.warning(f'Parent UI element is missing.')
            return

        parent_ui = None
        if isinstance(toolbox_data_class, toolbox_data.ToolboxCategory):
            # If we have a category
            # Adds a category. This is a qtwidgets.QToolButton to the Toolbox
            new_category = TBCategoryButton(toolbox_data_class.display_name,
                                            tb_id=toolbox_data_class.id,
                                            icon=toolbox_data_class.icon,
                                            parent=self)
            parent_ui = self.get_category_layout(toolbox_data_class.id)
            parent.addWidget(new_category)
        elif isinstance(toolbox_data_class, toolbox_data.ToolboxLayout):
            # If we have a layout
            # Adds a Layout. This is a qtwidgets.QFrame that groups actions together under a category.
            new_layout = TBLayout(frame_id=toolbox_data_class.id, parent=self)
            parent_ui = self.get_layout(toolbox_data_class.id)
            parent.addWidget(new_layout)
        elif isinstance(toolbox_data_class, toolbox_data.ToolboxAction):
            # If we have an action
            # Adds an action to the toolbox.
            action_ui = None
            if toolbox_data_class.action_type == 'QPushButton':
                # If we have a simple push button
                action_ui = TBButton(title=toolbox_data_class.display_name,
                                     button_id=toolbox_data_class.id,
                                     command=toolbox_data_class.command,
                                     tooltip=toolbox_data_class.tooltip,
                                     icon=toolbox_data_class.icon,
                                     color=toolbox_data_class.color,
                                     parent=self)
            elif toolbox_data_class.action_type == 'QWidget':
                # If we have an embeded UI
                action_ui = TBUI(title=toolbox_data_class.display_name,
                                 id=toolbox_data_class.id,
                                 command=toolbox_data_class.command,
                                 tooltip=toolbox_data_class.tooltip,
                                 parent=self)
            if action_ui:
                parent.addWidget(action_ui)

        if parent_ui:
            for child_entry in partial_build_dict.get('children'):
                # From this entry repeat this process for all children.
                self._build_ui(child_entry, parent_ui)

    def remove_all_categories(self):
        """
        Removes all the categories from the toolbox.
        """

        self.clear_layout(self.v_layout)

    def clear_layout(self, layout):
        """
        Removes all qtwidgets.QWidgets from a QLayout

        :param QLayout layout:
        """

        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().close()
                    child.widget().setParent(None)
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == qtcore.QEvent.Close:
                TOOLBOX_PREFS.write_file()
                self.closeEvent(event)
                return True
            else:
                return super().eventFilter(obj, event)


class TBCategoryButton(qtwidgets.QFrame):
    def __init__(self, title, tb_id, icon=None, parent=None):
        super().__init__(parent=parent)

        self.id = tb_id
        self.title = title
        self.icon = icon

        self.setObjectName(tb_id)
        self.setContentsMargins(1, 0, 0, 1)
        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(26)

        self.tool_v_layout = qtwidgets.QVBoxLayout(self)
        self.tool_v_layout.setContentsMargins(0, 0, 0, 0)

        self.tool_button = qtwidgets.QToolButton(self)
        self.tool_button.setObjectName(f'{tb_id}_toolButton')
        self.tool_button.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
        self.tool_button.setArrowType(qtcore.Qt.RightArrow)
        self.tool_button.setText(title)
        self.tool_button.setToolButtonStyle(qtcore.Qt.ToolButtonTextBesideIcon)
        self.tool_button.setContentsMargins(2, 0, 0, 1)
        self.tool_button.setMaximumHeight(25)
        self.tool_button.setMinimumHeight(25)
        self.tool_button.setParent(self)
        self.tool_v_layout.addWidget(self.tool_button)

        # if self.icon:
        #     qicon = resources.icon('software', self.icon)
        #     self.tool_button.setIcon(qicon)

        self.q_frame = qtwidgets.QFrame(self)
        self.q_frame.setObjectName(f'{tb_id}_frame')
        self.q_frame.setContentsMargins(2, 0, 1, 0)
        self.q_frame.setMinimumHeight(25)
        self.tool_v_layout.addWidget(self.q_frame)
        self.q_frame.setVisible(0)
        self.q_frame.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)

        self.tool_v2_layout = qtwidgets.QVBoxLayout(self.q_frame)
        self.tool_v2_layout.setContentsMargins(2, 0, 1, 0)
        self.tool_v2_layout.setObjectName(f'{tb_id}_category_layout')

        # Update the prefs
        if not TOOLBOX_PREFS.toolbar_entry_exist(self.id):
            TOOLBOX_PREFS.update_toolbar_button(self.id, 0)
        else:
            button_state = TOOLBOX_PREFS.get_toolbar_button_state(self.id)
            if button_state == 1:
                self.open_button()
            else:
                self.close_button()

        #############
        # Signals
        #############
        self.tool_button.pressed.connect(self.button_pressed)

    ##########
    # Slots
    ##########
    def button_pressed(self):
        """
        Opens or closes the QToolbarButton
        """

        if self.q_frame and not self.q_frame.isVisible():
            self.open_button()
        else:
            self.close_button()

    def open_button(self):
        """
        Opens the QToolbarButton
        """

        self.tool_button.setArrowType(qtcore.Qt.DownArrow)
        self.q_frame.setVisible(1)
        TOOLBOX_PREFS.update_toolbar_button(self.id, 1)

    def close_button(self):
        """
        Closes the QToolbarButton
        """

        self.tool_button.setArrowType(qtcore.Qt.RightArrow)
        self.q_frame.setVisible(0)
        TOOLBOX_PREFS.update_toolbar_button(self.id, 0)


class TBLayout(qtwidgets.QFrame):
    def __init__(self, frame_id, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(frame_id)
        self.id = frame_id
        self.setMinimumHeight(25)

        self.tool_h_layout = qtwidgets.QHBoxLayout(self)
        self.tool_h_layout.setContentsMargins(2, 0, 2, 0)
        self.tool_h_layout.setObjectName(f'{self.id}_layout')


class TBButton(qtwidgets.QPushButton):
    def __init__(self, title,
                 button_id,
                 command="print('Button Test!')",
                 tooltip=None,
                 icon=None,
                 color=None,
                 parent=None):
        super().__init__(parent=parent)

        self.title = title
        self.command = command
        self.tooltip = tooltip
        self.id = button_id
        self.icon = icon
        self.color = color
        self.info_box = None
        for x in self.parent().children():
            info_box = x.findChild(qtwidgets.QTextEdit, 'InfoBox')
            if info_box:
                self.info_box = info_box
                break

        # if self.icon:
        #     qicon = resources.icon('software', self.icon)
        #     self.setIcon(qicon)

        self.setToolTip(self.tooltip)
        self.setMinimumHeight(25)
        self.setMaximumHeight(25)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)
        self.setText(title)
        if self.color:
            r, g, b = self.color
            self.setStyleSheet(f'background-color:rgb{r, g, b}')
        self.setObjectName(self.id)

        self.clicked.connect(self.button_command)

    def button_command(self):
        """
        Runs the command that is stored in the action data
        """

        exec(self.command)

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == qtcore.QEvent.HoverEnter:
                if self.info_box:
                    self.info_box.setText(self.tooltip)
                    return True
            else:
                return super().eventFilter(obj, event)


class TBUI(qtwidgets.QWidget):
    def __init__(self, title,
                 id=None,
                 command=None,
                 tooltip=None,
                 info=None,
                 action=None,
                 parent=None):
        super().__init__(parent=parent)
        self.title = title
        self.id = id
        self.command = command
        self.tooltip = tooltip
        self.info = info
        self.action = action
        self.win = None
        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = qtwidgets.QVBoxLayout()
        self.main_layout.setObjectName(f'{title}_tbui')
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        # Need to make sure that each line is tabbed to the same difference as the wrapped command, adjust that here.
        modified_cmd = self.command.replace("\n", "\n\t")
        self.str_command = f'\ndef run_ui():\n\t{modified_cmd}\n\treturn win\nwindow = run_ui()'

        com = self.run_command(self.str_command)
        results = list(com.values())
        self.win = results[1]
        self.win.setParent(self)
        self.main_layout.addWidget(self.win)
        self.win.update()
        self.win.repaint()
        self.win.move(0, 0)
        # ToDo ncomes: Trying to find a way to get the comboboxes to work correctly after filtering
        # comboboxes = self.win.findChildren(QComboBox)
        # if not comboboxes:
        #     return
        # for box in comboboxes:
        #     print(comboboxes)
        #     box.update()
        #     box.repaint()
        #     box.move(0, 0)
        #     view = box.view()
        #     print(view)
        #     view.setMinimumWidth(10)
        #     view.update()
        #     view.repaint()
        #     view.move(0, 0)

    def run_command(self, command):
        """
        Opens a UI through a string command.

        :param str command: a python command that opens a UI.
        :return: Returns a dictionary of what was executed in the string command.
        :rtype: Dictionary
        """

        loc = {}
        logger.debug(command)
        win = exec(command, globals(), loc)
        return loc
