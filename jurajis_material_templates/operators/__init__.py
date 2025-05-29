from .auto_match import AutoMatchOperator
from .template_import import TemplateImportOperator

def register():
    from bpy.utils import register_class

    register_class(AutoMatchOperator)
    register_class(TemplateImportOperator)

def unregister():
    from bpy.utils import unregister_class

    unregister_class(TemplateImportOperator)
    unregister_class(AutoMatchOperator)