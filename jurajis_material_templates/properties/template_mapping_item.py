from bpy.props import StringProperty, PointerProperty
from bpy.types import PropertyGroup, Object


class TemplateMappingItem(PropertyGroup):
    source_object_name: StringProperty(name="Template Object")
    source_object: PointerProperty(
        name="Source Object",
        type=Object
    )
    target_object: PointerProperty(
        name="Target Object",
        type=Object,
        description="Object in current scene to apply template data to",
    )
