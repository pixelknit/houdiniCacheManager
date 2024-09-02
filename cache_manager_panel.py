import hou
from PySide2 import QtWidgets, QtCore
import os
import re

# Mapping of node types to their cache file parameter names
CACHE_PARAM_MAP = {
    'filecache': 'file',
    'alembic': 'fileName',
    'rop_alembic': 'filename',
}

def get_cache_nodes():
    cache_nodes = []
    for node in hou.node('/').allSubChildren():
        if node.type().name() in CACHE_PARAM_MAP.keys():
            cache_nodes.append(node)
    return cache_nodes

def list_cache_versions(node):
    """
    Given a cache node, find all version subdirectories in the cache output path.
    """
    versions = []
    try:
        param_name = CACHE_PARAM_MAP.get(node.type().name())
        if param_name:
            cache_path = node.evalParm(param_name)
            if cache_path:
                base_dir = os.path.dirname(cache_path)
                parent_dir = "/".join(base_dir.split("/")[:-1])
                
                if os.path.isdir(parent_dir):
                    for item in os.listdir(parent_dir):
                        if os.path.isdir(os.path.join(parent_dir, item)) and item.startswith('v'):
                            versions.append(item)
    except Exception as e:
        print(f"Error finding versions for node {node.name()}: {e}")
    return versions

class CacheListWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CacheListWidget, self).__init__()
        self.setWindowTitle("Cache Node List")
        self.setGeometry(100, 100, 400, 400)
    
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
    
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Node Name", "Node Type", "Current Cache Version", "Unused Caches"])
        layout.addWidget(self.tree)
    
        self.populate_tree()
    
        self.tree.itemClicked.connect(self.on_item_clicked)
        
        # Add delete button
        self.delete_button = QtWidgets.QPushButton("Delete Unused Caches")
        self.delete_button.clicked.connect(self.delete_and_update)
        layout.addWidget(self.delete_button)
    
    def populate_tree(self):
        cache_nodes = get_cache_nodes()
        for node in cache_nodes:
            item = QtWidgets.QTreeWidgetItem(self.tree)
            item.setText(0, node.name())
            item.setText(1, node.type().name())
            item.setData(0, QtCore.Qt.UserRole, node)
            
            param_name = CACHE_PARAM_MAP.get(node.type().name())
            current_version = node.evalParm(param_name).split("/")[-2]

            # Create a ComboBox for versions
            combo = QtWidgets.QComboBox()
            versions = list_cache_versions(node)
            combo.addItems(versions)
            
            # Create a ComboBox for unused versions
            un_combo = QtWidgets.QComboBox()
            unused_versions = versions.copy()
            unused_versions.remove(current_version)
            un_combo.addItems(unused_versions)

            if current_version in versions:
                combo.setCurrentText(current_version)
            
            self.tree.setItemWidget(item, 2, combo)
            self.tree.setItemWidget(item, 3, un_combo)
            
            combo.currentIndexChanged.connect(lambda index, n=node, c=combo: self.on_version_changed(n, c))

    def on_item_clicked(self, item, column):
        node = item.data(0, QtCore.Qt.UserRole)
        if node:
            node.setCurrent(True, clear_all_selected=True)
    
    def on_version_changed(self, node, combo):
        """
        Called when the version selection changes in the combo box.
        """
        new_version = combo.currentText()
        print(f"Node: {node.name()} changed to version {new_version}")
        
        try:
            param_name = CACHE_PARAM_MAP.get(node.type().name())
            if param_name:
                base_path = node.evalParm(param_name)
                print(base_path)
                pattern = r"v\d{3}"
                new_cache_path = re.sub(pattern, new_version, base_path)

                node.setParms({param_name: new_cache_path})
                print(f"Updated node {node.name()} to new cache path: {new_cache_path}")
                
                # Update the unused caches list
                item = self.tree.findItems(node.name(), QtCore.Qt.MatchExactly, 0)[0]
                un_combo = self.tree.itemWidget(item, 3)
                unused_versions = list_cache_versions(node)
                unused_versions.remove(new_version)
                un_combo.clear()
                un_combo.addItems(unused_versions)
        except Exception as e:
            print(f"Error updating node {node.name()}: {e}")
    
    def delete_unused_caches(self):
        """
        Deletes all unused caches that are versions less than the current version.
        """
        nodes_with_deleted_caches = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            node = item.data(0, QtCore.Qt.UserRole)
            param_name = CACHE_PARAM_MAP.get(node.type().name())
            if param_name:
                current_version = node.evalParm(param_name).split("/")[-2]
                current_version_num = int(re.search(r'\d+', current_version).group())
                base_path = os.path.dirname(node.evalParm(param_name))
                parent_dir = "/".join(base_path.split("/")[:-1])
                
                deleted_any = False
                for version in list_cache_versions(node):
                    version_num = int(re.search(r'\d+', version).group())
                    if version_num < current_version_num:
                        version_path = os.path.join(parent_dir, version)
                        print(f"Deleting unused cache: {version_path}")
                        try:
                            # Delete all files in the directory
                            for root, dirs, files in os.walk(version_path, topdown=False):
                                for file in files:
                                    os.remove(os.path.join(root, file))
                                for dir in dirs:
                                    os.rmdir(os.path.join(root, dir))
                            # Delete the directory itself
                            os.rmdir(version_path)
                            deleted_any = True
                        except Exception as e:
                            print(f"Error deleting {version_path}: {e}")
                
                if deleted_any:
                    nodes_with_deleted_caches.append(node)
    
        return nodes_with_deleted_caches
        
    def update_ui_after_delete(self, node):
        """
        Updates the UI for a specific node after deleting unused caches.
        """
        item = self.tree.findItems(node.name(), QtCore.Qt.MatchExactly, 0)[0]
        un_combo = self.tree.itemWidget(item, 3)
        unused_versions = list_cache_versions(node)
        current_version = node.evalParm(CACHE_PARAM_MAP.get(node.type().name())).split("/")[-2]
        unused_versions.remove(current_version)
        un_combo.clear()
        un_combo.addItems(unused_versions)
    
    def delete_and_update(self):
        nodes_with_deleted_caches = self.delete_unused_caches()
        for node in nodes_with_deleted_caches:
            self.update_ui_after_delete(node)

def show_cache_list_ui():
    widget = CacheListWidget()
    widget.show()

def onCreateInterface():
    widget = CacheListWidget()
    return widget