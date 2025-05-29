from bpy.props import StringProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup

from .template_mapping_item import TemplateMappingItem


class TemplateImportProperties(PropertyGroup):
    template_file: StringProperty(
        name="Template File",
        description="Path to the template .blend file",
        subtype='FILE_PATH'
    )

    source_collection_name: StringProperty(
        name="Source Collection Name",
        default="TEMPLATE",
    )

    mapping_items: CollectionProperty(
        type=TemplateMappingItem,
    )
    mapping_index: IntProperty()

    def is_template_file_set(self):
        return self.template_file is not None and self.template_file.endswith(".blend")
