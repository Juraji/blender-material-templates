from .auto_match import AutoMatchOperator
from .invoke_template_import import InvokeTemplateImportOperator

def register():
    from bpy.utils import register_class

    register_class(AutoMatchOperator)
    register_class(InvokeTemplateImportOperator)

def unregister():
    from bpy.utils import unregister_class

    unregister_class(InvokeTemplateImportOperator)
    unregister_class(AutoMatchOperator)