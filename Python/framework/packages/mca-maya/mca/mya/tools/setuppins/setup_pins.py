#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A tool for character modelling team to use to have a visual reference of joints and how they will rotate
"""

# python imports
import os
import inspect
import webbrowser
import yaml

# software specific imports
import pymel.core as pm

# mca python imports
from mca.common import log
from mca.common.utils import fileio
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.modifiers import decorators as py_decorators
from mca.common.textio import yamlio
from mca.common.resources import resources
from mca.common.assetlist import assetlist
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import skel_utils, chain_markup
from mca.mya.utils import namespace, naming, optionvars
from mca.mya.modeling import geometry
from mca.mya.modifiers import ma_decorators


logger = log.MCA_LOGGER


class MCASkeletonPinsOptionVars(optionvars.MCAOptionVars):
    """
    Option vars for the Face Staging UI
    """

    # strings
    MCASkeletonPinsAsset = {'default_value': 'player_male', 'docstring': 'Asset id for this reference.'}

    @property
    def asset_id_selection(self):
        """
        Returns asset id index in combo box.
        :rtype: Int
        """

        return self.MCASkeletonPinsAsset

    @asset_id_selection.setter
    def asset_id_selection(self, value):
        """
        Sets asset id index in combo box.
        :rtype: Int
        """

        self.MCASkeletonPinsAsset = value

class SkeletonPins(mayawindows.MCAMayaWindow):
    ID = 'mca-mya-tools-skeletonpins'
    VERSION = '1.2.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'setup_pins_ui.ui')
        super(SkeletonPins, self).__init__(title='Reference Pins',
                                           ui_path=ui_path,
                                           version=SkeletonPins.VERSION)
        self.optionvars = MCASkeletonPinsOptionVars()
        self.CREATED_NODES = {}
        tool_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.PIN_PATH = os.path.join(tool_path, 'setup_pins_dict.yml')
        self.PIN_DATA_DICT = yamlio.read_yaml_file(self.PIN_PATH)

        self.setup_signals()

    def setup_signals(self):
        asset_list = assetlist.AssetListRegistry()
        for asset_type, subtype_dict in asset_list.CATEGORY_DICT.items():
            for asset_subtype, entry_dict in subtype_dict.items():
                if asset_subtype in assetlist.NON_RIG_ASSETS:
                    continue
                for asset_id, asset_entry in entry_dict.items():
                    self.ui.assetBox.addItem(asset_entry.asset_name)

        axis_to_add = ['rotateX', 'rotateY', 'rotateZ']
        self.ui.axis_comboBox.addItems(axis_to_add)

        shapes_to_add = ['Cylinder', 'Sphere', 'Cone']
        self.ui.shape_comboBox.addItems(shapes_to_add)

        self.ui.toggleButton.clicked.connect(self._on_add_button_clicked)
        self.ui.removeButton.clicked.connect(self._on_remove_button_clicked)
        self.ui.axis_comboBox.currentTextChanged.connect(self._on_axis_changed)
        self.ui.shape_comboBox.currentTextChanged.connect(self._on_edit_shape_changed)
        self.ui.make_editable_pushButton.clicked.connect(self._on_make_pins_editable_clicked)
        self.ui.finish_and_merge_pushButton.clicked.connect(self._on_finish_merge_clicked)
        self.ui.save_data_pushButton.clicked.connect(self._on_save_data_button_clicked)
        self.ui.assetBox.editTextChanged.connect(self._on_asset_id_changed)

        save_icon = resources.icon(r'color\save.png')
        self.ui.save_data_pushButton.setIcon(save_icon)
        self.ui.save_data_pushButton.setEnabled(False)
        self.ui.finish_and_merge_pushButton.setEnabled(False)
        self.ui.axis_comboBox.setEnabled(False)
        self.ui.shape_comboBox.setEnabled(False)

        self.ui.assetBox.setCurrentText(self.optionvars.asset_id_selection)
        self._find_pins_in_scene()

    def _on_asset_id_changed(self):
        self.optionvars.asset_id_selection = self.ui.assetBox.currentText()

    @ma_decorators.not_undoable_decorator
    def _on_add_button_clicked(self, merge_pins=True):
        """
        Creates polyCylinders to serve as reference pins at location and orientation of the chosen asset skeleton. User
        can set length of pins during creation based on spinbox input. Pins are rotated to clearly represent the most
        commonly used rotation axis.
        """

        # Check if there are pins in scene already and remove if needed
        self._on_remove_button_clicked()

        asset_id = self.ui.assetBox.currentText()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(fn=self._on_add_button_clicked, data_entry=asset_id)

        # Look for a skeleton to reference, import one if not found
        jnt_list = pm.ls(type=pm.nt.Joint)
        roots = [x for x in jnt_list if chain_markup.JointMarkup(x).region == 'root']
        root_joint = next((x for x in roots if chain_markup.JointMarkup(x).chainStart), None)
        # Only want to delete skel if it was imported through the tool
        delete_joint_list = False

        if not root_joint:
            root_joint = self._import_skeleton()
            if not root_joint:
                return False
            if not merge_pins:
                # If not merging pins we assume we want to edit pins so want to keep skel in scene
                delete_joint_list = False
            else:
                delete_joint_list = True

        pins = geometry.make_pins(joint_list=chain_markup.ChainMarkup(root_joint).joints,
                         size_multiplier=self.ui.create_size_spinBox.value(),
                         data_dict=self.PIN_DATA_DICT,
                         delete_joint_list=delete_joint_list,
                         merge_pins=merge_pins)

        self.CREATED_NODES['pins'] = [pins.name()] if merge_pins else [x.name() for x in pins]

        if not delete_joint_list:
            self.CREATED_NODES['skel'] = [root_joint]
        else:
            self.CREATED_NODES['skel'] = []
        return True

    @ma_decorators.not_undoable_decorator
    @py_decorators.track_fnc
    def _on_remove_button_clicked(self):
        """
        Removes all created objects
        """

        pins = self.CREATED_NODES.get('pins')
        if pins:
            if not isinstance(pins, list):
                pins = [pins]
            existing_pins = [x for x in pins if pm.objExists(x)]
            pm.delete(existing_pins)
        skel = self.CREATED_NODES.get('skel')
        if skel:
            if pm.objExists(skel[0]):
                pm.delete(skel[0])

        if pm.namespace(exists='skel_ref'):
            namespace.purge_namespace('skel_ref')

        if not self.ui.make_editable_pushButton.isEnabled():
            self._button_switch()

        self.CREATED_NODES['skel'] = []
        self.CREATED_NODES['pins'] = []

    def _on_save_data_button_clicked(self):
        """
        Exports current pin configuration
        """

        self.save_pin_config(self.CREATED_NODES.get('pins'))
        self.export_pin_data()
        asset_id = self.ui.assetBox.currentText()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(fn=self._on_save_data_button_clicked, data_entry=asset_id)
        

    def save_pin_config(self, pin_list):
        """
        Updates PIN_DATA_DICT with current pin configuration info
        """

        setup_info = self.PIN_DATA_DICT.get('region_rotations')
        for pin in pin_list:
            pin = pm.PyNode(pin)

            jnt = pin.matchedJoint.get()
            new_rotate = pin.rotatedAxis.get()
            new_size = pin.scaleY.get()
            new_shape = pin.objShape.get()
            setup_info.update({jnt: [new_rotate, new_size, new_shape]})

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    def _on_axis_changed(self, axis):
        """
        Changes the rotated axis of the selected pin(s)
        """

        selection = pm.selected()
        if not selection:
            return
        for each in selection:
            if each.hasAttr('ref_pin'):
                matched_joint = each.getAttr('matchedJoint')
                if pm.objExists(matched_joint):
                    dup_bone = pm.duplicate(pm.PyNode(matched_joint), po=True, n=f'skel_ref_{matched_joint}')[0]
                    pm.setAttr(f'{dup_bone}.{axis}', 90)

                    pm.delete(pm.orientConstraint(dup_bone, each, mo=False))
                    each.rotatedAxis.set(axis)

                    pm.delete(dup_bone)

    @ma_decorators.undo_decorator
    def _on_edit_shape_changed(self, new_shape):
        """
        Changes the shape of the selected reference objects per user input from shape_comboBox
        """

        selected_objects = pm.selected()
        if not selected_objects:
            return
        new_objs = []
        obj_grp = selected_objects[0].getParent()
        namespace.set_namespace('skel_ref')
        for obj in selected_objects:
            obj_name = naming.get_basename(obj)
            if obj.hasAttr('ref_pin'):
                new_obj = geometry.create_reference_obj(obj.scaleY.get(),
                                                        self.ui.create_size_spinBox.value(),
                                                        new_shape,
                                                        obj.rotatedAxis.get(),
                                                        obj.matchedJoint.get())
                pm.delete(pm.parentConstraint(obj, new_obj, mo=False))
                pm.delete(obj)
                new_obj.rename(obj_name)
                new_obj.setParent(obj_grp)
                new_obj.translate.lock()
                new_objs.append(new_obj)
        namespace.set_namespace('')
        pm.select(new_objs, r=True)

    def _on_edit_size_changed(self):
        """
        Changes the size of the selected pin(s), keeping in mind the current user size multiplier that the pins were
        imported on.
        """

        size = self.ui.edit_size_spinBox.value()
        selection = pm.selected()
        for each in selection:
            if each.hasAttr('ref_pin'):
                current_multiplier = self.ui.create_size_spinBox.value()
                each.scaleY.set(current_multiplier * size)
                each.pinSize.set(size)

    def export_pin_data(self):
        """
        Exports PIN_DATA_DICT to YAML file
        """
        fileio.touch_path(self.PIN_PATH)
        yamlio.write_to_yaml_file(self.PIN_DATA_DICT, self.PIN_PATH)

    @py_decorators.track_fnc
    def _on_import_skeleton_button_pressed(self):
        """
        Imports skeleton and updates dict
        """

        root_joint = self._import_skeleton()
        self._button_switch()
        self.CREATED_NODES['skel'] = [root_joint]
        asset_id = self.ui.assetBox.currentText()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(fn=self._on_import_skeleton_button_pressed, data_entry=asset_id)

    def _import_skeleton(self):
        """
        Imports skeleton based on user input asset ID
        """
        asset_id = self.ui.assetBox.currentText()
        mca_asset = assetlist.get_asset_by_name(asset_id)
        if not mca_asset:
            logger.warning(f'Skeleton for {asset_id} not found')
            return None
        root_chk = self.CREATED_NODES.get('skel')
        if root_chk:
            pm.delete(root_chk)

        root_joint = skel_utils.import_skeleton(mca_asset.skel_path)

        root_joint.v.set(0)
        root_joint.addAttr('ref_pins', at='bool')

        return root_joint

    def _button_switch(self):
        """
        Switches enabled status of editing buttons
        """

        self.ui.make_editable_pushButton.setEnabled(self.ui.finish_and_merge_pushButton.isEnabled())

        self.ui.finish_and_merge_pushButton.setEnabled(not self.ui.make_editable_pushButton.isEnabled())
        self.ui.axis_comboBox.setEnabled(not self.ui.make_editable_pushButton.isEnabled())
        self.ui.shape_comboBox.setEnabled(not self.ui.make_editable_pushButton.isEnabled())
        self.ui.save_data_pushButton.setEnabled(not self.ui.make_editable_pushButton.isEnabled())

    @py_decorators.track_fnc
    def _on_make_pins_editable_clicked(self):
        """
        Puts pins into editable state by recreating them without merging and keeping skel in scene
        """

        add_pins = self._on_add_button_clicked(merge_pins=False)
        if not add_pins:
            return
        self._button_switch()

    @ma_decorators.not_undoable_decorator
    def _on_finish_merge_clicked(self):
        """
        Merges pins and removes imported skel
        """
        self._button_switch()
        created_pins = self.CREATED_NODES.get('pins')
        created_skel = self.CREATED_NODES.get('skel')
        if not created_pins:
            return
        if created_skel:
            pm.delete(created_skel)
            self.CREATED_NODES['skel'] = []
        existing_pins = [x for x in created_pins if pm.objExists(x)]
        final_pins = pm.polyUnite(existing_pins, n=f'skel_ref_pins')[0]
        pm.delete(final_pins, ch=True)
        final_pins.addAttr('ref_pins', at='bool')
        self.CREATED_NODES['pins'] = final_pins

    def _find_pins_in_scene(self):
        """
        Looks for pins in scene and if any are found updates setup dict with their configuration
        """

        pins_in_scene = [x for x in pm.ls(type=pm.nt.Transform) if x.hasAttr('pinSize')]
        if pins_in_scene:
            self.save_pin_config(pins_in_scene)
            self._button_switch()
            self.CREATED_NODES['pins'] = [x.name() for x in pins_in_scene]

            roots = [x for x in pm.ls(type=pm.nt.Joint) if chain_markup.JointMarkup(x).region == 'root']
            root_joint = next((x for x in roots if chain_markup.JointMarkup(x).chainStart), None)
            if root_joint:
                if root_joint.hasAttr('ref_pins'):
                    self.CREATED_NODES['skel'] = [root_joint]

