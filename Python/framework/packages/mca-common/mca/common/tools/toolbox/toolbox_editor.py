"""
An Editor for the ToolBox
"""

# python imports
from enum import Enum
import os
import re
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui
# software specific imports
# mca python imports
from mca.common.pyqt import common_windows, messages, syntax_highlighter
from mca.common.resources import resources
from mca.common.utils import dcc_util, fileio, string_utils
from mca.common.tools.toolbox import toolbox_data, toolbox_prefs

from mca.common import log

logger = log.MCA_LOGGER
TOOLBOX_PREFS = None


def new_toolbox_prompt():
    """
    New toolbox prompt

    :return: Path to the new toolbox or ''
    :rtype: str
    """

    default_preview_text = 'Choose a name for the toolbox.'

    def preview_path(current_name, is_local, ui_element):
        """
        Updates the Message box UI elements to preview the final Toolbox path.

        :param str current_name: The current str value of the prompt lineedit.
        :param bool is_local: If the new toolbox should be a local toolbox or saved in the common directories.
        :param qtwidgets.QLabel ui_element: The label we're using to preview the final path.
        """
        preview_text = default_preview_text
        if current_name:
            base_path = toolbox_data.LOCAL_TOOLBOX_DIR if is_local else toolbox_data.DCC_TOOLBOX_DIR
            preview_text = os.path.join(base_path, f'{current_name}.tbx')
        ui_element.setText(preview_text)

    message_box = messages.MCAMessageBox(title='New Toolbox',
                            text='What would you like to name the new toolbox?',
                            detail_text=None,
                            style=None,
                            sound=None,
                            parent=None)
    message_box.setIconPixmap(resources.icon(r'color\question.png', typ=resources.ResourceTypes.PIXMAP))

    # MessageBox UI overrides.
    message_box_layout = message_box.layout()
    local_checkBox = qtwidgets.QCheckBox()
    local_checkBox.setText('Local Toolbox')
    message_box_layout.addWidget(local_checkBox, 2, 0, 1, -1)
    prompt_lineEdit = qtwidgets.QLineEdit()
    message_box_layout.addWidget(prompt_lineEdit, 3, 0, 1, -1)
    path_preview_label = qtwidgets.QLabel()
    path_preview_label.setText(f'{default_preview_text}')
    message_box_layout.addWidget(path_preview_label, 4, 0, 1, -1)
    local_checkBox.stateChanged.connect(lambda: preview_path(prompt_lineEdit.text(), local_checkBox.isChecked(), path_preview_label))
    prompt_lineEdit.textChanged.connect(lambda: preview_path(prompt_lineEdit.text(), local_checkBox.isChecked(), path_preview_label))
    message_box.setStandardButtons(qtwidgets.QMessageBox.Ok)
    horizontal_layout = qtwidgets.QHBoxLayout()
    message_box_layout.addLayout(horizontal_layout, 5, 0, 1, -1)
    for prompt_button in message_box.buttons():
        horizontal_layout.addWidget(prompt_button)
    message_box.exec_()
    return_val = path_preview_label.text()
    return '' if return_val == default_preview_text else return_val


class REF(Enum):
    NO_REF = 0
    IS_REF = 1
    PARENT_REF = 2


class ToolboxEditor(common_windows.MCAMainWindow):
    VERSION = '1.0.0'

    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'toolbox_editor_ui.ui')
        super().__init__(title='Toolbox Editor',
                         ui_path=ui_path,
                         version=self.VERSION,
                         parent=parent)

        toolbox_data.ToolboxRegistry().reload()

        global TOOLBOX_PREFS
        
        self._temporary_toolbox_dict = {}
        self.setup_signals()

        self.copied_ref = None
        self.active_edit = {}

        self.v_layout = None
        self.setup_preview_toolbox()
        self.refresh_combo_box()
        self.build_toolbox_preview()

    def setup_preview_toolbox(self):
        """
        Setup framework for the dynamically built UI previews. We'll attach everything to this scroll area and v_layout

        """
        scroll_area = MainCategoryScrollArea(self)
        scroll_area.setObjectName(f'MainScrollFrame')
        scroll_area.setFrameStyle(qtwidgets.QFrame.WinPanel | qtwidgets.QFrame.Sunken)
        scroll_area.setContentsMargins(0, 0, 4, 0)
        # self.scroll_area.setMinimumHeight(735)
        scroll_area.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
        scroll_area.setVerticalScrollBarPolicy(qtcore.Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(qtcore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        self.ui.toolbox_preview_verticalLayout.addWidget(scroll_area)

        scrollAreaWidgetContents = qtwidgets.QWidget(scroll_area)
        scrollAreaWidgetContents.setMinimumWidth(250)
        scrollAreaWidgetContents.setMinimumHeight(1700)
        scroll_area.setWidget(scrollAreaWidgetContents)

        # Create the layout that has all of the toolbar buttons and actions.
        self.v_layout = qtwidgets.QVBoxLayout(scrollAreaWidgetContents)
        self.v_layout.setObjectName(f'CategoryVerticalLayout')
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        scrollAreaWidgetContents.setLayout(self.v_layout)

    def setup_signals(self):
        """
        Connect our non dynamic UI elements.

        """
        self.ui.new_toolbox_pushButton.clicked.connect(self.add_new_toolbox)
        self.ui.delete_toolbox_pushButton.clicked.connect(self.delete_toolbox)
        self.ui.toolbox_list_comboBox.currentTextChanged.connect(self.build_toolbox_preview)

        self.ui.color_picker_pushButton.clicked.connect(self.pick_color)

        self.ui.save_pushButton.clicked.connect(self.save_changes)
        self.ui.save_toolboxes_pushButton.clicked.connect(self.save_all_toolboxes)
        self.ui.test_pushButton.clicked.connect(self.test_action)

        self.ui.color_r_lineEdit.editingFinished.connect(lambda: self._color_set(self.ui.color_r_lineEdit))
        self.ui.color_g_lineEdit.editingFinished.connect(lambda: self._color_set(self.ui.color_g_lineEdit))
        self.ui.color_b_lineEdit.editingFinished.connect(lambda: self._color_set(self.ui.color_b_lineEdit))

        syntax_highlighter.PythonHighlighter(self.ui.action_code_textEdit.document())

    def closeEvent(self, event):
        reply = messages.question_message('Exiting Editor', 'Would you like to save all toolboxes', tri_option=True)

        if reply == 'Yes':
            self.save_all_toolboxes()

        if reply != 'Cancel':
            event.accept()
        else:
            event.ignore()

    def add_new_toolbox(self):
        """
        Prompt for the name of a new toolbox and if it's local or shared. Then add it if there is no name conflict.
        This toolbox will be held in memory until it's saved.

        """
        new_toolbox_path = new_toolbox_prompt()
        if not new_toolbox_path:
            return
        toolbox_name = os.path.basename(new_toolbox_path).split('.')[0]
        if toolbox_data.get_toolbox_by_name(toolbox_name):
            logger.warning(f'{toolbox_name}, There is already a toolbox by this name please choose a different name.')
        toolbox_name_list = list(toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.keys())
        new_toolbox = toolbox_data.Toolbox(new_toolbox_path, True)
        main_category = toolbox_data.ToolboxCategory('Main', {})
        new_toolbox.set_entry(main_category)
        self._temporary_toolbox_dict[toolbox_name] = new_toolbox
        self._refresh_combo_box(toolbox_name_list+[toolbox_name])

        self.ui.toolbox_list_comboBox.setCurrentText(toolbox_name)
        self.build_toolbox_preview()

    def delete_toolbox(self):
        """
        Delete the current toolbox and remove it from disk, or remove it from memory if it has not been saved.

        """
        toolbox_name = self.ui.toolbox_list_comboBox.currentText()
        if not toolbox_name:
            return

        if messages.question_message('Deleting Toolbox', f'Are you sure you want to remove toolbox: {toolbox_name}?') != 'Yes':
            return

        found_toolbox = toolbox_data.get_toolbox_by_name(toolbox_name)
        if found_toolbox:
            if os.path.exists(found_toolbox.path):
                fileio.touch_path(found_toolbox.path, True)
                toolbox_data.ToolboxRegistry().reload()
        else:
            self._temporary_toolbox_dict.pop(toolbox_name)
        self.ui.toolbox_list_comboBox.removeItem(self.ui.toolbox_list_comboBox.currentIndex())
        self.refresh_menu_cmd()

    def refresh_combo_box(self):
        """
        Refill the combo box for potential toolbox options.

        """
        self._refresh_combo_box(list(toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.keys()))

    def _refresh_combo_box(self, toolbox_name_list):
        """
        Under the hood options for reloading the combo box, this lets us also add any temporary combo boxes to the ui.

        :param list[str] toolbox_name_list: A list of all toolbox names.
        :return:
        """
        self.ui.toolbox_list_comboBox.blockSignals(True)
        self.ui.toolbox_list_comboBox.clear()
        self.ui.toolbox_list_comboBox.addItems(list(sorted(toolbox_name_list)))
        self.ui.toolbox_list_comboBox.blockSignals(False)

    def _add_vertical_spacer(self):
        """
        This removes and then adds the vertical spacer to the end of the main v_layout.

        """
        try:
            if self.vertical_spacer:
                self.v_layout.removeWidget(self.vertical_spacer.widget())
        except:
            pass

        self.vertical_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Minimum, qtwidgets.QSizePolicy.Expanding)
        self.v_layout.addItem(self.vertical_spacer)

    def _get_active_toolbox(self):
        """
        From the active toolbox name in the combobox look up the corrisponding toolbox class.

        :return: The toolbox by name lookup.
        :rtype: Toolbox
        """
        toolbox_name = self.ui.toolbox_list_comboBox.currentText()
        found_toolbox = toolbox_data.get_toolbox_by_name(toolbox_name)
        if not found_toolbox:
            found_toolbox = self._temporary_toolbox_dict.get(toolbox_name)

        if found_toolbox:
            return found_toolbox

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

    def build_toolbox_preview(self):
        """
        From the active toolbox build out a visualization of the UI. This will not skip empty categories, but will skip
        empty layouts.

        """
        active_toolbox = self._get_active_toolbox()
        if not active_toolbox:
            return

        self.remove_all_categories()

        toolbox_name = active_toolbox.toolbox_name
        logger.debug(f'Building toolbox preview for: {toolbox_name}')
        build_order_dict = active_toolbox.get_build_order()

        global TOOLBOX_PREFS
        dcc_app = dcc_util.application()
        TOOLBOX_PREFS = toolbox_prefs.ToolBoxPreferences(toolbox=toolbox_name, dcc=dcc_app)

        for child_entry in build_order_dict.get('children'):
            # From the root entry find all childen and add them to the main layout.
            self._build_preview(child_entry, self.v_layout)

        self.vertical_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Minimum, qtwidgets.QSizePolicy.Expanding)
        self.v_layout.addItem(self.vertical_spacer)

    def _build_preview(self, partial_build_dict, parent, ref=REF.NO_REF):
        """
        Under the hood build class, this recursively checks through the build order to generate the preview UI.

        :param dict partial_build_dict: A formatted build dictionary containing toolbox data classes, and their children.
        :param QUiClass parent: A Q ui element the build objects should be parented to.
        :param int ref: The reference status of this ui element.
        """
        toolbox_data_class = partial_build_dict.get('toolbox_class')
        active_toolbox = self._get_active_toolbox()
        # Type check here since Categories are an child inheritance of Layouts.
        if type(toolbox_data_class) is toolbox_data.ToolboxLayout and not partial_build_dict.get('children'):
            # If we have a layout and it has no children. Skip this build as
            # the category or layout will be empty.
            logger.warning(f'layout has no children and will not be built.')
            active_toolbox.remove_entry(toolbox_data_class.id, clean_parent=True)
            return

        if not parent:
            logger.warning(f'Parent UI element is missing.')
            return

        if not toolbox_data_class:
            logger.warning('Unable to establish toolbox data class.')
            return

        if ref in [REF.IS_REF, REF.PARENT_REF]:
            ref = REF.PARENT_REF
        elif ref == REF.NO_REF and toolbox_data_class.id not in active_toolbox.GUID_DICT:
            ref = REF.IS_REF

        parent_ui = None
        if isinstance(toolbox_data_class, toolbox_data.ToolboxCategory):
            # If we have a category
            # Adds a category. This is a qtwidgets.QToolButton to the Toolbox
            new_category = PreviewCategoryButton(toolbox_data_class.display_name,
                                                 tb_id=toolbox_data_class.id,
                                                 icon=toolbox_data_class.icon,
                                                 parent=self,
                                                 parent_layout=parent,
                                                 ref=ref)
            parent_ui = self.get_category_layout(toolbox_data_class.id)
            parent.addWidget(new_category)
        elif isinstance(toolbox_data_class, toolbox_data.ToolboxLayout):
            # If we have a layout
            # Adds a Layout. This is a qtwidgets.QFrame that groups actions together under a category.
            new_layout = PreviewLayout(frame_id=toolbox_data_class.id, parent=self, parent_layout=parent)
            parent_ui = self.get_layout(toolbox_data_class.id)
            parent.addWidget(new_layout)
        elif isinstance(toolbox_data_class, toolbox_data.ToolboxAction):
            # If we have an action
            # Adds an action to the toolbox.
            action_ui = None
            if toolbox_data_class.action_type == 'QPushButton':
                # If we have a simple push button
                action_ui = PreviewButton(title=toolbox_data_class.display_name,
                                          button_id=toolbox_data_class.id,
                                          command=toolbox_data_class.command,
                                          tooltip=toolbox_data_class.tooltip,
                                          icon=toolbox_data_class.icon,
                                          color=toolbox_data_class.color,
                                          parent=self,
                                          parent_layout=parent,
                                          ref=ref)
            elif toolbox_data_class.action_type == 'QWidget':
                # If we have an embeded UI
                action_ui = PreviewUI(title=toolbox_data_class.display_name,
                                      button_id=toolbox_data_class.id,
                                      command=toolbox_data_class.command,
                                      tooltip=toolbox_data_class.tooltip,
                                      parent=self,
                                      parent_layout=parent,
                                      ref=ref)
            if action_ui:
                parent.addWidget(action_ui)

        if parent_ui:
            for child_entry in partial_build_dict.get('children'):
                # From this entry repeat this process for all children.
                self._build_preview(child_entry, parent_ui, ref)

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

    def save_changes(self):
        """
        This saves the data in the edit portion of the UI to the current button.

        """
        if self.active_edit:
            action_id, toolbox_name, parent_id = self.active_edit
            edited_toolbox = toolbox_data.get_toolbox_by_name(toolbox_name)
            if not edited_toolbox:
                edited_toolbox = self._temporary_toolbox_dict.get(toolbox_name)
            if not edited_toolbox:
                logger.warning('Unable to recover the specified toolbox, it may have been deleted.')
                return
            toolbox_action = edited_toolbox.GUID_DICT[action_id]

            if toolbox_action.action_type == 'QWidget' and not any(True if x in self.ui.action_code_textEdit.toPlainText() else False for x in ['win =', 'win=']):
                logger.warning('When using an embed UI, set the ui to a var using the formatting: "win ="')
                return

            toolbox_action.display_name = self.ui.title_lineEdit.text()
            toolbox_action.tooltip = self.ui.tooltip_lineEdit.text()
            #toolbox_action.icon = # Icon lookup uses just the name inside our resoruces folder.
            toolbox_action.command = self.ui.action_code_textEdit.toPlainText()

            color_value = self.get_color()
            if any(color_value):
                toolbox_action.color = color_value

            edited_toolbox.set_entry(toolbox_action)
            parent_entry = edited_toolbox.GUID_DICT[parent_id]
            if action_id not in parent_entry.children:
                parent_entry.children.append(action_id)
                edited_toolbox.set_entry(parent_entry)

        global TOOLBOX_PREFS
        TOOLBOX_PREFS.write_file()

        self.remove_all_categories()
        self.build_toolbox_preview()

    def save_all_toolboxes(self):
        """
        This commits all changes to all toolboxes to disk.

        """
        for toolbox_name, toolbox_entry in toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.items():
            toolbox_entry.commit()
        for toolbox_name, toolbox_entry in self._temporary_toolbox_dict.items():
            toolbox_entry.commit()

        self._temporary_toolbox_dict = {}
        toolbox_data.ToolboxRegistry().reload()

        self.remove_all_categories()
        self.build_toolbox_preview()
        self.refresh_menu_cmd()

    def refresh_menu_cmd(self):
        pass

    def test_action(self):
        """
        This executes the code in the current code window.

        """
        if self.active_edit:
            action_id, toolbox_name, parent_id = self.active_edit
            edited_toolbox = toolbox_data.get_toolbox_by_name(toolbox_name)
            if not edited_toolbox:
                edited_toolbox = self._temporary_toolbox_dict.get(toolbox_name)
            if not edited_toolbox:
                logger.warning('Unable to recover the specified toolbox, it may have been deleted.')
                return
            toolbox_action = edited_toolbox.GUID_DICT[action_id]

            if toolbox_action.action_type == 'QWidget' and not any(True if x in self.ui.action_code_textEdit.toPlainText() else False for x in ['win =', 'win=']):
                logger.warning('When using an embed UI, set the ui to a var using the formatting: "win ="')
                return

            exec(self.ui.action_code_textEdit.toPlainText())
        else:
            logger.warning('Mark for edit, or add a new action.')

    def pick_color(self):
        """
        This opens the color picker and sends the current color to it if able.

        """
        color_value = self.get_color()
        if color_value and '' not in color_value:
            color = qtwidgets.QColorDialog.getColor(initial=qtgui.QColor(*[int(x) for x in color_value]))
        else:
            color = qtwidgets.QColorDialog.getColor()
        if color.isValid():
            self.set_color(color.getRgb()[:-1])

    def set_color(self, rgb_color):
        """
        Applies the color sent to the UI elements. Used after the picker and when loading button data.

        """
        if not rgb_color:
            return

        r, g, b = rgb_color

        for color_value, ui_element in zip([r, g, b], [self.ui.color_r_lineEdit, self.ui.color_g_lineEdit, self.ui.color_b_lineEdit]):
            ui_element.blockSignals(True)
            ui_element.setText(str(color_value))
            ui_element.blockSignals(False)

    def get_color(self):
        """
        This returns the current color RGB values as a list of strings.

        :return: A list of the RGB values present in the UI as strings.
        :rtype: list(str, str , str)
        """
        return [self.ui.color_r_lineEdit.text(), self.ui.color_g_lineEdit.text(), self.ui.color_b_lineEdit.text()]

    def _color_set(self, ui_element):
        """
        When a color value is set this forces it to be ints only within the range of 0-255 inclusively.

        :param QlineEdit ui_element: The RGB QlineEdit that gets modified after the value is set.
        """
        current_text = ui_element.text()
        clean_color = re.sub('[^0-9]', '', current_text)
        if clean_color != '':
            color_value = int(clean_color)
            if color_value < 0:
                color_value = 0
            elif color_value > 255:
                color_value = 255
            clean_color = str(color_value)
        ui_element.blockSignals(True)
        ui_element.setText(clean_color)
        ui_element.blockSignals(False)

    @classmethod
    def _reorder_entry(cls, ui_element, parent_layout, positive_move, main_ui, is_button=False):
        """
        Call from the dynamic ui which reorders the position of a UI element.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param bool positive_move: If the move is positive or negative.
        :param ToolboxEditor main_ui: The main UI instance.
        :param bool is_button: If this is being called from a button.
        """
        if is_button:
            # Buttons live inside a horizonal layout so we need to go find the parent category that horizonal layout is actually in to reorder our shit.
            layout_id = parent_layout.objectName().split('_')[0]

            # This should get us our PreviewLayout
            parent_widget = parent_layout.parentWidget()

            # Reset the parent layout to the one we're actually impacting.
            parent_layout = parent_widget.parent_layout
            parent_id = parent_layout.objectName().split('_')[0]

            main_ui.clear_layout(parent_layout)

            main_ui.reorder_entry(parent_id, layout_id, positive_move)
        else:
            # Purge the current parent layout's children
            main_ui.clear_layout(parent_layout)

            # Update the toolbox data
            if parent_layout is main_ui.v_layout:
                parent_id = 'Main'
            else:
                parent_id = parent_layout.objectName().split('_')[0]
            main_ui.reorder_entry(parent_id, ui_element.id, positive_move)
        active_toolbox = main_ui._get_active_toolbox()

        # Get the build dict and rebuild the preview UI based on the changes.
        partial_build_dict = active_toolbox._get_build_order_from_entry(active_toolbox.GUID_DICT[parent_id])
        for child_entry in partial_build_dict['children']:
            main_ui._build_preview(child_entry, parent_layout)

        main_ui._add_vertical_spacer()

    def reorder_entry(self, parent_guid, guid, positive_move=True):
        """
        Local call to modify the main ui.

        :param str parent_guid: The guid that represents the parent object.
        :param str guid: The guid of the object being moved.
        :param bool positive_move: If the object is being moved ahead or behind.
        """
        active_toolbox = self._get_active_toolbox()
        parent_entry = active_toolbox.GUID_DICT.get(parent_guid)
        current_index = None
        if guid in parent_entry.children:
            current_index = parent_entry.children.index(guid)
        else:
            # likely have a reference.
            for current_index, child_guid in enumerate(parent_entry.children):
                child_entry = active_toolbox.GUID_DICT.get(child_guid)
                if isinstance(child_entry, toolbox_data.ToolboxReference):
                    if child_entry.reference_id == guid:
                        # Overwrite the original guid we were searching for with the ref entry guid.
                        guid = child_entry.id
                        break
                    current_index = None

        if current_index is not None:
            new_index = current_index - 1 if positive_move else current_index + 1
            if new_index >= 0 and new_index < len(parent_entry.children):
                parent_entry.children.remove(guid)
                parent_entry.children.insert(new_index, guid)
                active_toolbox.set_entry(parent_entry)

    @classmethod
    def _add_category(cls, ui_element, parent_layout, main_ui):
        """
        Call from the dynamic ui to add a new category under the passed element.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param ToolboxEditor main_ui: The main UI instance.
        """
        category_name = messages.text_prompt_message('Choose Category Name', 'Select a name for this new category')

        if not category_name:
            return

        category_name = ' '.join([x.title() for x in category_name.split(' ')])

        guid = string_utils.generate_guid()
        new_category = PreviewCategoryButton(category_name, guid, parent=main_ui, parent_layout=parent_layout)
        parent_layout.addWidget(new_category)
        new_category.open_button()
        main_ui._add_vertical_spacer()

        parent_id = ui_element.id

        new_category = toolbox_data.ToolboxCategory(guid, {'display_name': category_name})
        main_ui.set_category(new_category, parent_id)

    def set_category(self, toolbox_category, parent_id):
        """
        This sets the new category in the toolbox data, and builds out the dynamic UI.

        :param ToolboxCategory toolbox_category: A ToolboxCategory data class.
        :param str parent_id: The guid that represents the parent of this category in the toolbox data.
        """
        active_toolbox = self._get_active_toolbox()
        active_toolbox.set_entry(toolbox_category)
        parent_entry = active_toolbox.GUID_DICT[parent_id]
        parent_entry.children.append(toolbox_category.id)
        active_toolbox.set_entry(parent_entry)

    @classmethod
    def _copy_reference(cls, ui_element, main_ui):
        """
        Call from the dynamic ui to add a copied reference to the pass ui_element.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param ToolboxEditor main_ui: The main UI instance.
        """
        guid = ui_element.id
        active_toolbox = main_ui._get_active_toolbox()
        toolbox_name = active_toolbox.toolbox_name
        main_ui.copy_reference(guid, toolbox_name)

    def copy_reference(self, guid, toolbox_name):
        """
        Loads the data of the selected UI element into a property on the main UI class.

        :param str guid: The guid that represents the element in the toolbox.
        :param str toolbox_name: The name that represents the toolbox.
        """
        self.copied_ref = [guid, toolbox_name]

    @classmethod
    def _add_reference(cls, ui_element, parent_layout, main_ui, is_button=False):
        """
        Call from the dynamic ui to add a new category under the passed element.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param ToolboxEditor main_ui: The main UI instance.
        :param bool is_button: If this is being called from a button.
        """
        if is_button:
            parent_layout = ui_element.parent_layout
        if parent_layout is main_ui.v_layout:
            parent_id = 'Main'
        else:
            parent_id = parent_layout.objectName().split('_')[0]

        main_ui.add_reference(parent_id, parent_layout, is_button)

    def add_reference(self, parent_id, parent_layout, is_button=False):
        """
        If a reference has been saved to the main UI, add it as a reference to the toolbox data and refresh the UI.

        :param str parent_id: The guid that represents the parent of this category in the toolbox data.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param bool is_button: If this is being called from a button.
        """
        if not self.copied_ref:
            logger.warning('Copy a reference before adding a reference.')
            return

        active_toolbox = self._get_active_toolbox()
        if active_toolbox.toolbox_name == self.copied_ref[-1]:
            logger.warning('You cannot add a reference to elements from the same toolbox.')
            return

        new_reference = toolbox_data.ToolboxReference(None, dict(zip(['reference_id', 'reference_toolbox'], self.copied_ref)))
        if is_button:
            if isinstance(toolbox_data.get_entry_by_reference(new_reference), toolbox_data.ToolboxCategory):
                logger.warning('You cannot add a category reference to a button group.')
                return

        active_toolbox.set_entry(new_reference)

        parent_entry = active_toolbox.GUID_DICT[parent_id]
        parent_entry.children.append(new_reference.id)
        active_toolbox.set_entry(parent_entry)

        self.clear_layout(parent_layout)
        partial_build_dict = active_toolbox._get_build_order_from_entry(active_toolbox.GUID_DICT[parent_id])
        for child_entry in partial_build_dict['children']:
            self._build_preview(child_entry, parent_layout)

        self._add_vertical_spacer()

    @classmethod
    def _add_action(cls, ui_element, parent_layout, main_ui, is_button=False, new_layout=False):
        """
        Call from the dynamic ui to add a new action under the passed element.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param ToolboxEditor main_ui: The main UI instance.
        :param bool is_button: If the new UI element is a button or an embedded UI.
        :param bool new_layout: If this is being called from a category we'll need to prepare a new horizontal layout to hold it.
        """
        # If we're adding a new layout, we're coming from a category, else we're coming from a button
        parent_id = parent_layout.objectName().split('_')[0] if not new_layout else ui_element.id

        main_ui.add_action(parent_id, parent_layout, is_button, new_layout)

    def add_action(self, parent_id, parent_layout, is_button, new_layout):
        """
        Add a new action and then refreshes the ui.

        :param str parent_id: The guid that represents the parent of this category in the toolbox data.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param bool is_button: If the new UI element is a button or an embedded UI.
        :param bool new_layout: If this is being called from a category we'll need to prepare a new horizontal layout to hold it.
        """
        data_dict = {'action_type': 'QPushButton'}if is_button else {'action_type': 'QWidget'}
        data_dict['display_name'] = 'new button' if is_button else 'new embedded ui'
        active_toolbox = self._get_active_toolbox()
        new_action = toolbox_data.ToolboxAction(None, data_dict)
        active_toolbox.set_entry(new_action)

        original_parent_id = parent_id
        if new_layout:
            # If we require a new layout like if we add a button below a category.
            new_layout = toolbox_data.ToolboxLayout(None, {})
            active_toolbox.set_entry(new_layout)

            # Add the new layout as a child of the category.
            parent_entry = active_toolbox.GUID_DICT[parent_id]
            parent_entry.children.append(new_layout.id)
            active_toolbox.set_entry(parent_entry)

            # New parent id becomes the layout.
            parent_id = new_layout.id

        # Add the new action to the parent layout.
        parent_entry = active_toolbox.GUID_DICT[parent_id]
        parent_entry.children.append(new_action.id)
        active_toolbox.set_entry(parent_entry)

        # Prime the edit for the new button.
        self.edit_action(new_action.id, parent_id)

        self.clear_layout(parent_layout)
        partial_build_dict = active_toolbox._get_build_order_from_entry(active_toolbox.GUID_DICT[original_parent_id])
        for child_entry in partial_build_dict['children']:
            self._build_preview(child_entry, parent_layout)

        self._add_vertical_spacer()

    @classmethod
    def _edit_action(cls, ui_element, parent_layout, main_ui):
        """
        Call from the dynamic ui to edit the toolbox data for this ui element.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param QverticalLayout | QhorizontalLayout parent_layout: The layout this UI element is part of.
        :param ToolboxEditor main_ui: The main UI instance.
        """
        action_id = ui_element.id
        parent_id = parent_layout.objectName().split('_')[0] if parent_layout != main_ui.v_layout else 'Main'
        main_ui.edit_action(action_id, parent_id)

    def edit_action(self, action_id, parent_id):
        """
        Sends the toolbox data for a given element to the edit portion of the main UI.

        :param str action_id: The guid that represents the toolbox element that will be edited.
        :param str parent_id: The guid that represents the parent of this category in the toolbox data.
        :return:
        """
        active_toolbox = self._get_active_toolbox()
        toolbox_data_class = active_toolbox.GUID_DICT.get(action_id)
        if not toolbox_data_class:
            logger.warning(f'{action_id}, unable to find action entry.')
        self.active_edit = [action_id, active_toolbox.toolbox_name, parent_id]
        self.load_action_data(toolbox_data_class)

    def lock_edit(self, lock=True):
        """
        Locks or unlocks the edit panel of the main UI.

        :param bool lock: If the edit tab of the UI should be locked or unlocked.
        """
        self.ui.title_lineEdit.setEnabled(not lock)
        self.ui.tooltip_lineEdit.setEnabled(not lock)
        self.ui.action_code_textEdit.setEnabled(not lock)

        self.ui.color_r_lineEdit.setEnabled(not lock)
        self.ui.color_g_lineEdit.setEnabled(not lock)
        self.ui.color_b_lineEdit.setEnabled(not lock)

    def load_action_data(self, toolbox_data_class):
        """
        Loads the data present in a ToolboxAction class to the edit panel.

        :param ToolboxAction toolbox_data_class: ToolboxAction data class that will be represented in the edit panel.
        """
        self.lock_edit(False)
        self.ui.title_lineEdit.setText(toolbox_data_class.display_name)
        self.ui.tooltip_lineEdit.setText(toolbox_data_class.tooltip)
        self.ui.action_code_textEdit.setText(toolbox_data_class.command)

        self.set_color(toolbox_data_class.color if toolbox_data_class.color else ['' for x in range(3)])

    @classmethod
    def _remove_entry(cls, ui_element, main_ui):
        """
        Call from the dynamic ui to remove an entry from the active toolbox.

        :param Qframe | QpushButton ui_element: A Qframe or QpushButton that is calling this command.
        :param ToolboxEditor main_ui: The main UI instance.
        """
        parent_layout = ui_element.parent_layout
        parent_layout.removeWidget(ui_element)
        # Remove orphaned layouts here.

        guid = ui_element.id

        parent_id = parent_layout.objectName().split('_')[0] if parent_layout != main_ui.v_layout else 'Main'

        active_toolbox = main_ui._get_active_toolbox()
        if guid not in active_toolbox.GUID_DICT:
            # likely have a reference.
            for child_guid in active_toolbox.GUID_DICT[parent_id].children:
                child_entry = active_toolbox.GUID_DICT.get(child_guid)
                if isinstance(child_entry, toolbox_data.ToolboxReference):
                    if child_entry.reference_id == guid:
                        # Overwrite the original guid we were searching for with the ref entry guid.
                        guid = child_entry.id
                        break

        main_ui.remove_entry(guid)
        ui_element.deleteLater()

    def remove_entry(self, guid):
        """
        Removes an entry from the toolbox entry, then refreshes the UI preview.

        :param str guid: The guid that represents the toolbox element that will be removed.
        :return:
        """
        active_toolbox = self._get_active_toolbox()
        active_toolbox.remove_entry(guid, clean_parent=True)


class MainCategoryScrollArea(qtwidgets.QScrollArea):
    def __init__(self, main_ui):
        super().__init__()
        self.setContextMenuPolicy(qtcore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_click_menu)

        self.id = 'Main'
        self.main_ui = main_ui

    def right_click_menu(self, pos):
        menu = qtwidgets.QMenu()

        # Add menu options
        t = menu.addAction(f'<Main Category>')
        t.setDisabled(True)
        menu.addSeparator()
        add_category = menu.addAction('Add Category')
        add_reference = menu.addAction('Add Reference')

        parent_ui = self.main_ui.v_layout

        # Menu option events
        add_category.triggered.connect(lambda: ToolboxEditor._add_category(self, parent_ui, self.main_ui))
        add_reference.triggered.connect(lambda: ToolboxEditor._add_reference(self, parent_ui, self.main_ui))

        # Position
        menu.exec_(self.mapToGlobal(pos))


class PreviewCategoryButton(qtwidgets.QFrame):
    def __init__(self, title, tb_id, icon=None, parent=None, parent_layout=None, ref=REF.NO_REF):
        super().__init__(parent=parent)
        self.main_ui = parent
        self.ref = ref

        self.id = tb_id
        self.title = title
        self.icon = icon

        self.parent_layout = parent_layout

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
        #     qicon = resources.icon(self.icon)
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
        global TOOLBOX_PREFS
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
        if self.ref != REF.PARENT_REF:
            self.setContextMenuPolicy(qtcore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.right_click_menu)

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

    def right_click_menu(self, pos):
        menu = qtwidgets.QMenu()

        # Add menu options
        t = menu.addAction(f'<{self.title} Category>')
        t.setDisabled(True)
        menu.addSeparator()
        if self.ref == REF.NO_REF:
            add_category = menu.addAction('Add Category')
            delete_category = menu.addAction('Delete Category')
            menu.addSeparator()
            add_action = menu.addAction('Add New Button')
            add_ui = menu.addAction('Add New Embedded UI')
        else:
            delete_category = menu.addAction('Remove Reference')
        menu.addSeparator()
        if self.ref == REF.NO_REF:
            copy_reference = menu.addAction('Copy as Reference')
            add_reference = menu.addAction('Add Reference')
            menu.addSeparator()
        move_category_up = menu.addAction('Move Element Up')
        move_category_down = menu.addAction('Move Element Down')

        parent_ui = self.tool_v2_layout

        # Menu option events
        if self.ref == REF.NO_REF:
            add_category.triggered.connect(lambda: ToolboxEditor._add_category(self, parent_ui, self.main_ui))
        delete_category.triggered.connect(lambda: ToolboxEditor._remove_entry(self, self.main_ui))

        if self.ref == REF.NO_REF:
            add_action.triggered.connect(lambda: ToolboxEditor._add_action(self, parent_ui, self.main_ui, True, True))
            add_ui.triggered.connect(lambda: ToolboxEditor._add_action(self, parent_ui, self.main_ui, False, True))
            copy_reference.triggered.connect(lambda: ToolboxEditor._copy_reference(self, self.main_ui))
            add_reference.triggered.connect(lambda: ToolboxEditor._add_reference(self, parent_ui, self.main_ui))

        move_category_up.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, True, self.main_ui))
        move_category_down.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, False, self.main_ui))

        # Position
        menu.exec_(self.mapToGlobal(pos))


class PreviewLayout(qtwidgets.QFrame):
    def __init__(self, frame_id, parent=None, parent_layout=None):
        super().__init__(parent=parent)
        self.main_ui = parent
        self.parent_layout = parent_layout

        self.setObjectName(frame_id)
        self.id = frame_id
        self.setMinimumHeight(25)

        self.tool_h_layout = qtwidgets.QHBoxLayout(self)
        self.tool_h_layout.setContentsMargins(2, 0, 2, 0)
        self.tool_h_layout.setObjectName(f'{self.id}_layout')


class PreviewButton(qtwidgets.QPushButton):
    def __init__(self, title,
                 button_id,
                 command="print('Button Test!')",
                 tooltip=None,
                 icon=None,
                 color=None,
                 parent=None,
                 parent_layout=None,
                 ref=REF.NO_REF):
        super().__init__(parent=parent)
        self.main_ui = parent
        self.ref = ref

        self.title = title
        self.command = command
        self.tooltip = tooltip
        self.id = button_id
        self.icon = icon
        self.color = color

        self.parent_layout = parent_layout

        if self.ref == REF.NO_REF:
            self.clicked.connect(lambda sacrifice=False, ui_element=self, parent_ui=self.parent_layout, main_ui=self.main_ui: ToolboxEditor._edit_action(ui_element, parent_ui, main_ui))

        # if self.icon:
        #     qicon = resources.icon(self.icon)
        #     self.setIcon(qicon)

        self.setToolTip(self.tooltip)
        self.setMinimumHeight(25)
        self.setMaximumHeight(25)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)
        self.setText(title)
        if self.color:
            self.setStyleSheet(f'background-color: rgb{tuple([int(x) for x in self.color])}')
        self.setObjectName(self.id)
        if self.ref != REF.PARENT_REF:
            self.setContextMenuPolicy(qtcore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.right_click_menu)

    def right_click_menu(self, pos):
        menu = qtwidgets.QMenu()

        # Add menu options
        t = menu.addAction(f'<{self.title} Button>')
        t.setDisabled(True)
        menu.addSeparator()
        if self.ref == REF.NO_REF:
            add_action = menu.addAction('Add New Button')
            edit_action = menu.addAction('Edit Button')
            delete_button = menu.addAction('Remove Button')
        else:
            delete_button = menu.addAction('Remove Reference')
        menu.addSeparator()
        if self.ref == REF.NO_REF:
            copy_reference = menu.addAction('Copy as Reference')
        add_reference = menu.addAction('Add Reference')
        menu.addSeparator()
        move_up = menu.addAction('Move Element Up')
        move_down = menu.addAction('Move Element Down')
        move_left = menu.addAction('Move Element Left')
        move_right = menu.addAction('Move Element Right')

        parent_ui = self.parent_layout

        # Menu option events
        if self.ref == REF.NO_REF:
            add_action.triggered.connect(lambda: ToolboxEditor._add_action(self, parent_ui, self.main_ui, True))
            edit_action.triggered.connect(lambda: ToolboxEditor._edit_action(self, parent_ui, self.main_ui))
        delete_button.triggered.connect(lambda: ToolboxEditor._remove_entry(self, self.main_ui))

        if self.ref == REF.NO_REF:
            copy_reference.triggered.connect(lambda: ToolboxEditor._copy_reference(self, self.main_ui))
            add_reference.triggered.connect(lambda: ToolboxEditor._add_reference(self, parent_ui, self.main_ui))

        move_up.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, True, self.main_ui, True))
        move_down.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, False, self.main_ui, True))
        move_left.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, True, self.main_ui))
        move_right.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, False, self.main_ui))

        # Position
        menu.exec_(self.mapToGlobal(pos))


class PreviewUI(qtwidgets.QPushButton):
    def __init__(self, title,
                 button_id,
                 command="print('Button Test!')",
                 tooltip=None,
                 parent=None,
                 parent_layout=None,
                 ref=REF.NO_REF):
        super().__init__(parent=parent)
        self.main_ui = parent
        self.ref = ref

        self.title = title
        self.command = command
        self.tooltip = tooltip
        self.id = button_id

        self.parent_layout = parent_layout

        if self.ref == REF.NO_REF:
            self.clicked.connect(lambda sacrifice=False, ui_element=self, parent_ui=self.parent_layout, main_ui=self.main_ui: ToolboxEditor._edit_action(ui_element, parent_ui, main_ui))

        self.setToolTip(self.tooltip)
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)
        self.setText(title)
        self.setObjectName(self.id)
        if self.ref != REF.PARENT_REF:
            self.setContextMenuPolicy(qtcore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.right_click_menu)

    def right_click_menu(self, pos):
        menu = qtwidgets.QMenu()

        # Add menu options
        t = menu.addAction(f'<{self.title} Embeded Ui>')
        t.setDisabled(True)
        menu.addSeparator()
        if self.ref == REF.NO_REF:
            edit_action = menu.addAction('Edit Ui')
            delete_button = menu.addAction('Remove Ui')
        else:
            delete_button = menu.addAction('Remove Reference')
        menu.addSeparator()
        if self.ref == REF.NO_REF:
            copy_reference = menu.addAction('Copy as Reference')
        menu.addSeparator()
        move_up = menu.addAction('Move Element Up')
        move_down = menu.addAction('Move Element Down')

        parent_ui = self.parent_layout

        # Menu option events
        delete_button.triggered.connect(lambda: ToolboxEditor._remove_entry(self, self.main_ui))

        if self.ref == REF.NO_REF:
            edit_action.triggered.connect(lambda: ToolboxEditor._edit_action(self, parent_ui, self.main_ui))
            copy_reference.triggered.connect(lambda: ToolboxEditor._copy_reference(self, self.main_ui))

        move_up.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, True, self.main_ui, True))
        move_down.triggered.connect(lambda: ToolboxEditor._reorder_entry(self, self.parent_layout, False, self.main_ui, True))

        # Position
        menu.exec_(self.mapToGlobal(pos))
