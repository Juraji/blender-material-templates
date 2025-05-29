from bpy.types import Context as _Context

from .template_import_properties import TemplateImportProperties
from .template_mapping_item import TemplateMappingItem


def register():
    from bpy.types import Scene
    from bpy.utils import register_class
    from bpy.props import PointerProperty

    register_class(TemplateMappingItem)
    register_class(TemplateImportProperties)

    Scene.template_import__import_properties = PointerProperty(type=TemplateImportProperties)


def unregister():
    from bpy.types import Scene
    from bpy.utils import unregister_class

    unregister_class(TemplateImportProperties)
    unregister_class(TemplateMappingItem)

    # noinspection PyUnresolvedReferences
    del Scene.template_import__import_properties


def props_from_ctx(context: _Context) -> TemplateImportProperties:
    # noinspection PyUnresolvedReferences
    return context.scene.template_import__import_properties
