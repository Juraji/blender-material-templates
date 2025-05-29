from .template_import_mapping_list import TemplateImportMappingList
from .template_import_panel import TemplateImportPanel


def register():
    from bpy.utils import register_class

    register_class(TemplateImportMappingList)
    register_class(TemplateImportPanel)


def unregister():
    from bpy.utils import unregister_class

    unregister_class(TemplateImportPanel)
    unregister_class(TemplateImportMappingList)
