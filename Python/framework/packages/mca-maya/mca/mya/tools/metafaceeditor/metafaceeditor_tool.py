"""
Module that contains Test tool implementation.
"""

# System global imports
import os
# Software specific imports
import pymel.core as pm
# PySide2 imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets
# mca python imports
from mca.common import log
from mca.common.project import project_paths

from mca.mya.pyqt import mayawindows
from mca.mya.thirdpartytools.MetaHumanDNACalibrationmain import dna_viewer
from mca.mya.thirdpartytools.MetaHumanDNACalibrationmain.lib.Maya2022.windows import dna, dnacalib
from mca.mya.modeling import vert_utils

from mca.mya.tools.metafaceeditor import metafaceeditor_utils

logger = log.MCA_LOGGER


class MetaFaceEditor(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'metafaceeditor_ui.ui')
        super().__init__(title='Meta Face Editor',
                         ui_path=ui_path,
                         version=MetaFaceEditor.VERSION)

        self.calibrated_data = None
        self.dna_object = None
        self.dna_path = None
        self.reader = None
        self.temp_dna_path = self._get_temp_dna_path()
        self.ui.dna_status_lineEdit.setText('No data')
        self.ui.dna_status_lineEdit.setReadOnly(1)
        # ==============================
        # Signals
        # ==============================

        self.ui.browse_pushButton.clicked.connect(self._on_browse_button_clicked)
        self.ui.load_dna_build_rig_pushButton.clicked.connect(self._on_load_dna_build_rig_button_clicked)
        self.ui.update_base_mesh_pushButton.clicked.connect(self._on_update_base_mesh_button_clicked)
        self.ui.update_dna_file_pushButton.clicked.connect(self._on_update_dna_file_button_clicked)
        self.ui.save_as_new_dna_pushButton.clicked.connect(self._on_save_as_new_dna_button_clicked)
        self.ui.edit_expression_pushButton.clicked.connect(self._on_edit_expression_button_clicked)
        self.ui.joint_lod_comboBox.currentIndexChanged.connect(self._populate_joint_tree)
        self.ui.mesh_blendshape_comboBox.currentIndexChanged.connect(self._populate_blendshape_list)
        self.ui.save_expression_pushButton.clicked.connect(self._on_save_expression_button_clicked)
        self.ui.edit_blendshape_pushButton.clicked.connect(self._on_edit_blendshape_button_clicked)
        self.ui.clear_blendshape_pushButton.clicked.connect(self._on_clear_blendshape_button_clicked)
        self.ui.remove_joint_pushButton.clicked.connect(self._on_remove_joint_button_clicked)
        self.ui.mimic_joint_selection_pushButton.clicked.connect(self._on_mimic_joint_selection_button_clicked)
        self.ui.mimic_ui_joint_selection_pushButton.clicked.connect(self.mimic_ui_selection_in_maya)
        self.ui.show_skinned_joints_only_checkBox.clicked.connect(self._populate_joint_tree)


    # ==============================
    # Slots
    # ==============================

    ############# BASE #############

    def _on_browse_button_clicked(self):

        sel_dna = pm.fileDialog2(fileFilter='*.dna',
                                 dialogStyle=2,
                                 fm=1,
                                 dir=project_paths.MCA_PROJECT_ROOT)
        if not sel_dna:
            return
        self.ui.dna_path_lineEdit.setText(sel_dna[0])

    def _get_lod_list(self):
        lods = []
        for x in range(8):
            lod_checkbox = eval(f'self.ui.lod_{x}_checkBox')

            if lod_checkbox.isChecked():
                lod = lod_checkbox.text()
                print(lod)
                lods.append(lod)
        return [int(x) for x in lods]

    def _on_load_dna_build_rig_button_clicked(self):
        self.dna_path = os.path.normpath(self.ui.dna_path_lineEdit.text())
        if not os.path.exists(self.dna_path):
            logger.warning('DNA path does not exist')
            return
        lods_to_build = self._get_lod_list()
        if not lods_to_build:
            return
        if not self.ui.load_dna_only_checkBox.isChecked():
            metafaceeditor_utils.assemble_mh_head_rig(self.dna_path, lods_to_build)

        self.reader = metafaceeditor_utils.load_dna_reader(self.dna_path)
        self.calibrated_data = dnacalib.DNACalibDNAReader(self.reader)
        self.dna_object = dna_viewer.DNA(self.dna_path)
        self._populate_expression_list()
        self._populate_lod_comboboxes()
        self._populate_joint_tree()
        self._populate_meshes_combobox()
        self._populate_blendshape_list()
        self._set_dna_status('Clean')

    def _on_update_neutral_joints_button_clicked(self):
        old_head_mesh = pm.PyNode('head_lod0_mesh')
        new_head_mesh = pm.selected()[0]

        jnt_vert_dict = {}
        for jnt in reversed(pm.listRelatives('FACIAL_C_FacialRoot', ad=True, type=pm.nt.Joint)):
            if any(pm.listRelatives(jnt, ad=True, type=pm.nt.Joint)):
                continue
            closest_vert = vert_utils.get_closest_vertex_to_object(old_head_mesh, jnt)
            jnt_vert_dict[jnt.name()] = closest_vert
        remove_connection_list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
        for jnt_name, vert_num in jnt_vert_dict.items():
            connections = pm.listConnections(jnt_name, source=True, destination=False, plugs=True)
            for connection in connections:
                connection_dest = pm.listConnections(connection, source=False, destination=True, plugs=True)
                if connection_dest:
                    connection_dest = connection_dest[0]
                    if connection_dest.name().split('.')[-1] in remove_connection_list:
                        connection // connection_dest

            pos = pm.xform(f'{new_head_mesh.name()}.vtx[{vert_num}]', q=True, t=True, ws=True)
            jnt = pm.PyNode(jnt_name)
            jnt_par = jnt.getParent()
            jnt.setParent(w=True)
            jnt.tx.set(pos[0])
            jnt.ty.set(pos[1])
            jnt.tz.set(pos[2])
            jnt.setParent(jnt_par)
        metafaceeditor_utils.run_joints_command(self.reader, self.calibrated_data)
        metafaceeditor_utils.save_dna(self.calibrated_data, self.dna_path)

    def _on_update_base_mesh_button_clicked(self):
        #TODO: use CalculateMeshLowerLODsCommand to automatically set up lower LOD meshes
        if not self.dna_object:
            logger.warning('No DNA loaded.')
            return

        mesh_list = metafaceeditor_utils.get_all_meshes_from_calibrated(self.calibrated_data)
        selected_lod = self.ui.basemesh_update_lod_comboBox.currentIndex()
        head_meshes = [x for x in mesh_list if 'head' in x]
        old_head_mesh = head_meshes[selected_lod]

        new_head_mesh = pm.selected()
        if not new_head_mesh:
            logger.warning('No new head mesh selected')
            return

        new_head_mesh = new_head_mesh[0]

        current_vertices_positions = {}
        meshes = []
        for mesh_index, name in enumerate(self.dna_object.meshes.names):
            meshes.append(name)
            current_vertices_positions[name] = {
                "mesh_index": mesh_index,
                "positions": metafaceeditor_utils.get_mesh_vertex_positions_from_scene(name),
            }

        channel_name = new_head_mesh.name()

        blendnode = pm.blendShape(new_head_mesh, old_head_mesh, n=f'TEMP_DELETE_ME_blendshape')[0]
        pm.setAttr(f'{blendnode}.{channel_name}', 1)

        for name, item in current_vertices_positions.items():
            new_vertices_positions = metafaceeditor_utils.get_mesh_vertex_positions_from_scene(name)
            if new_vertices_positions:
                metafaceeditor_utils.run_vertices_command(
                    self.calibrated_data, item["positions"], new_vertices_positions, item["mesh_index"]
                )
        temp_dna_path = self._get_temp_dna_path()

        # note: updating vertex and joints positions at same time doesn't work but
        # saving before updating joints does

        metafaceeditor_utils.save_dna(self.calibrated_data, temp_dna_path)

        pm.delete(blendnode)

        if self.ui.auto_position_neutral_joints_checkBox.isChecked():
            if not selected_lod == 0:
                logger.warning('Please update LOD 0 to update joint positions.')
            else:
                metafaceeditor_utils.set_new_mh_face_joint_positions(old_head_mesh,
                                                                     new_head_mesh,
                                                                     self.reader,
                                                                     self.calibrated_data)

        metafaceeditor_utils.save_dna(self.calibrated_data, temp_dna_path)
        self.reader = metafaceeditor_utils.load_dna_reader(temp_dna_path)
        self.calibrated_data = dnacalib.DNACalibDNAReader(self.reader)
        self.dna_object = dna_viewer.DNA(temp_dna_path)

        self._set_dna_status('dirty')

    ############# BLENDSHAPES #############

    def _populate_meshes_combobox(self):
        self.ui.mesh_blendshape_comboBox.clear()
        if not self.calibrated_data:
            logger.warning('No calibrated data.')
            return
        mesh_list = metafaceeditor_utils.get_all_meshes_from_calibrated(self.calibrated_data)
        self.ui.mesh_blendshape_comboBox.addItems(mesh_list)
        self.ui.mesh_blendshape_comboBox.setCurrentIndex(0)

    def _populate_blendshape_list(self):
        self.ui.blendshape_listWidget.clear()
        current_mesh_index = self.ui.mesh_blendshape_comboBox.currentIndex()
        current_mesh_name = self.ui.mesh_blendshape_comboBox.currentText()
        blendshape_list = metafaceeditor_utils.get_blendshape_list_for_mesh(current_mesh_index,
                                                                            self.dna_object,
                                                                            self.calibrated_data,
                                                                            current_mesh_name)
        self.ui.blendshape_listWidget.addItems(sorted(blendshape_list))

    def _on_clear_blendshape_button_clicked(self):
        mesh_to_edit = self.ui.mesh_blendshape_comboBox.currentText()
        blendshape_item = self.ui.blendshape_listWidget.currentItem()
        if not blendshape_item:
            logger.warning('No blendshape selected to update')
            return
        blendshape_name = blendshape_item.text()

        metafaceeditor_utils.clear_mh_face_blendshape_by_name(self.dna_object,
                                                       self.calibrated_data,
                                                       mesh_to_edit,
                                                       blendshape_name,
                                                       self.temp_dna_path)
        self.reader = metafaceeditor_utils.load_dna_reader(self.temp_dna_path)
        self.calibrated_data = dnacalib.DNACalibDNAReader(self.reader)
        self.dna_object = dna_viewer.DNA(self.temp_dna_path)
        self._set_dna_status('dirty')


    def _on_edit_blendshape_button_clicked(self):
        self._update_selected_blendshape()
        self._set_dna_status('dirty')

    def _update_selected_blendshape(self):
        new_blendshape = pm.selected()
        if not new_blendshape:
            logger.warning('Please select a new blendshape to add')
            return
        new_blendshape = new_blendshape[0]
        mesh_to_edit = self.ui.mesh_blendshape_comboBox.currentText()
        blendshape_item = self.ui.blendshape_listWidget.currentItem()
        if not blendshape_item:
            logger.warning('No blendshape selected to update')
            return
        blendshape_name = blendshape_item.text()

        metafaceeditor_utils.update_mh_face_blendshape(self.dna_object,
                                                       self.calibrated_data,
                                                       new_blendshape,
                                                       mesh_to_edit,
                                                       blendshape_name,
                                                       self.temp_dna_path,
                                                       self.reader)
        self.reader = metafaceeditor_utils.load_dna_reader(self.temp_dna_path)
        self.calibrated_data = dnacalib.DNACalibDNAReader(self.reader)
        self.dna_object = dna_viewer.DNA(self.temp_dna_path)
        self._set_dna_status('dirty')

    ############# EXPRESSIONS #############

    def _populate_expression_list(self):
        expression_list = []
        for i in range(self.calibrated_data.getRawControlCount()):
            raw_control_name = self.calibrated_data.getRawControlName(i)
            expression_list.append(raw_control_name)
        expression_list_display = [x.split('.')[-1] for x in expression_list]
        self.ui.expression_listWidget.addItems(sorted(expression_list_display))

    def _on_save_expression_button_clicked(self):
        if not self.connection_dict:
            return
        self._update_selected_expression()
        for connection, connection_dest in self.connection_dict.items():
            connection >> connection_dest


    def _on_edit_expression_button_clicked(self):
        if not self.joint_list:
            logger.warning('No joint list')
            return
        selected_item = self.ui.expression_listWidget.currentItem()
        if not selected_item:
            return

        remove_connection_list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX',
                                  'scaleY', 'scaleZ']
        self.connection_dict = {}
        for jnt_name in self.joint_list:
            connections = pm.listConnections(jnt_name, source=True, destination=False, plugs=True)
            for connection in connections:
                connection_dest = pm.listConnections(connection, source=False, destination=True, plugs=True)
                if connection_dest:
                    connection_dest = connection_dest[0]
                    if connection_dest.name().split('.')[-1] in remove_connection_list:
                        connection // connection_dest
                        self.connection_dict[connection] = connection_dest


    def _update_selected_expression(self):
        # TODO: ADD EDIT MODE
        selected_item = self.ui.expression_listWidget.currentItem()
        if not selected_item:
            return
        selected_expression = selected_item.text()
        full_expression_name = f'CTRL_expressions.{selected_expression}'

        metafaceeditor_utils.update_expression_by_name(self.dna_path,
                                                       full_expression_name)


    ############# JOINTS #############

    def _populate_lod_comboboxes(self):
        self.ui.joint_lod_comboBox.clear()
        self.ui.joint_lod_comboBox.addItem('all')
        for x in range(self.calibrated_data.getLODCount()):
            self.ui.joint_lod_comboBox.addItem(str(x))
            self.ui.basemesh_update_lod_comboBox.addItem(str(x))
        self.ui.joint_lod_comboBox.setCurrentIndex(0)
        self.ui.basemesh_update_lod_comboBox.setCurrentIndex(0)

    def _populate_joint_tree(self):
        self.ui.joint_treeWidget.clear()
        selected_lod = self.ui.joint_lod_comboBox.currentText()
        joint_lod_list = None
        joint_id_list = []
        joint_count = self.calibrated_data.getJointCount()
        for x in range(joint_count):
            joint_name = self.calibrated_data.getJointName(x)
            joint_id_list.append(joint_name)

        if selected_lod == '':
            return

        if selected_lod != 'all':
            selected_lod = int(selected_lod)
            joint_indices = self.calibrated_data.getJointIndicesForLOD(selected_lod)
            joint_lod_list = []
            for x in joint_indices:
                joint_name = self.calibrated_data.getJointName(x)
                joint_lod_list.append(joint_name)

        use_joint_list = joint_id_list if not joint_lod_list else joint_lod_list
        self.joint_list = joint_id_list

        if self.ui.show_skinned_joints_only_checkBox.isChecked():
            skinned_joints = metafaceeditor_utils.get_mh_face_skinned_joints(joint_id_list, self.calibrated_data)
            skinned_usable_joints = [x for x in use_joint_list if x in skinned_joints]
            use_joint_list = skinned_usable_joints


        self.item_name_dict = {}

        for index, joint_name in enumerate(joint_id_list):
            if joint_name not in use_joint_list:
                continue
            parent_name = None
            if index:
                x = joint_id_list.index(joint_name)
                parent_index = self.calibrated_data.getJointParentIndex(x)
                parent_name = self.calibrated_data.getJointName(parent_index)

            tree_item = qtwidgets.QTreeWidgetItem([joint_name])
            if parent_name:
                if self.item_name_dict.get(parent_name):
                    self.item_name_dict[parent_name][0].addChild(tree_item)
                else:
                    self.ui.joint_treeWidget.insertTopLevelItem(0, tree_item)
            else:
                self.ui.joint_treeWidget.insertTopLevelItem(0, tree_item)

            if joint_name not in self.item_name_dict:
                self.item_name_dict[joint_name] = [tree_item, joint_name]
            else:
                logger.warning(f'rename {joint_name} a joint has already been registered with this name.')
                return

        self.ui.joint_treeWidget.expandAll()

    def _select_recursive(self, selected_item):
        for row in range(selected_item.childCount()):
            child_item = selected_item.child(row)
            child_item.setSelected(True)
            self._select_recursive(child_item)

    def _on_remove_joint_button_clicked(self):
        selected_items = self.ui.joint_treeWidget.selectedItems()
        if not selected_items:
            logger.warning('Please select a joint to remove')
            return

        for selected_item in selected_items:
            self._select_recursive(selected_item)

        selected_items = self.ui.joint_treeWidget.selectedItems()
        for selected_item in selected_items:
            selected_joint = selected_item.text(0)
            joint_list = []

            for x in range(self.calibrated_data.getJointCount()):
                joint_list.append(self.calibrated_data.getJointName(x))
            joint_index = joint_list.index(selected_joint)
            command_seq = dnacalib.CommandSequence()
            command = dnacalib.RemoveJointCommand(joint_index)
            command_seq.add(command)
            command_seq.run(self.calibrated_data)

        root = self.ui.joint_treeWidget.invisibleRootItem()
        for item in selected_items:
            (item.parent() or root).removeChild(item)

        metafaceeditor_utils.save_dna(self.calibrated_data, self.temp_dna_path)
        self.reader = metafaceeditor_utils.load_dna_reader(self.temp_dna_path)
        self.calibrated_data = dnacalib.DNACalibDNAReader(self.reader)
        self.dna_object = dna_viewer.DNA(self.temp_dna_path)
        self._set_dna_status('dirty')

    def _on_mimic_joint_selection_button_clicked(self):
        maya_sel = pm.selected()
        if not maya_sel:
            return
        maya_sel_names = [x.name() for x in maya_sel]
        all_items = self.get_all_items(self.ui.joint_treeWidget)
        for item in all_items:
            item_text = item.text(0)
            if item_text in maya_sel_names:
                item.setSelected(True)



    def get_all_items(self, tree_widget):
        items = []
        for index in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(index)
            items.append(top_item)
            items.extend(self.get_all_child_items(top_item))
        return items

    def get_all_child_items(self, parent_item):
        items = []
        for index in range(parent_item.childCount()):
            child_item = parent_item.child(index)
            items.append(child_item)
            items.extend(self.get_all_child_items(child_item))
        return items


    def mimic_ui_selection_in_maya(self):
        selected_items = self.ui.joint_treeWidget.selectedItems()
        sel_joint_names = []
        for selected_item in selected_items:
            selected_joint = selected_item.text(0)
            sel_joint_names.append(selected_joint)
        real_joints = [x for x in sel_joint_names if pm.objExists(x)]
        pm.select(real_joints, r=True)

    ############# CONTROLS #############


    ############# SKINNING #############

    ############# OTHER #############

    def _on_update_dna_file_button_clicked(self):
        if not self.reader:
            logger.warning('No reader found.')
            return

        metafaceeditor_utils.save_dna(self.reader, self.dna_path)
        self._set_dna_status('clean')

    def _on_save_as_new_dna_button_clicked(self):
        if not self.reader:
            logger.warning('No reader found.')
            return
        new_dna_path = pm.fileDialog2(fileFilter='*.dna',
                                      dialogStyle=2,
                                      fm=0,
                                      dir=project_paths.MCA_PROJECT_ROOT)

        if not new_dna_path:
            return
        new_dna_path = os.path.normpath(new_dna_path[0])
        if not new_dna_path.endswith('.dna'):
            new_dna_path = new_dna_path + '.dna'
        metafaceeditor_utils.save_dna(self.reader, new_dna_path)
        self._set_dna_status('clean')

    def _set_dna_status(self, status):

        if status == 'dirty':
            self.ui.dna_status_lineEdit.setStyleSheet('{background-color: rgb(255, 0, 0)}')
            self.ui.dna_status_lineEdit.setText('Dirty')
        else:
            self.ui.dna_status_lineEdit.setStyleSheet('{background-color: rgb(0, 255, 0)}')
            self.ui.dna_status_lineEdit.setText('Clean')

    def _get_temp_dna_path(self):
        version = pm.about(version=True)
        prefs_dir = os.path.join(os.path.expanduser('~'), 'maya', version)
        temp_dna_dir = os.path.normpath(os.path.join(prefs_dir, 'temp_dna'))
        if not os.path.exists(temp_dna_dir):
            os.makedirs(temp_dna_dir)
        temp_dna_path = os.path.join(temp_dna_dir, 'temp_dna.dna')

        return temp_dna_path


