from .auto_match import AutoMatchOperator
from .clear_matches import ClearMatchesOperator
from .template_import import TemplateImportOperator

def register():
    from bpy.utils import register_class

    register_class(AutoMatchOperator)
    register_class(TemplateImportOperator)
    register_class(ClearMatchesOperator)

def unregister():
    from bpy.utils import unregister_class

    unregister_class(ClearMatchesOperator)
    unregister_class(TemplateImportOperator)
    unregister_class(AutoMatchOperator)