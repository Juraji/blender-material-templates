from bpy.types import Panel

from ..operators import TemplateImportOperator


class TemplateImportPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_context = "objectmode"
    bl_idname = "VIEW3D_PT_template_import_panel"
    bl_category = "Juraji's Tools"
    bl_region_type = "UI"
    bl_label = "Template Import"

    def draw(self, context):
        layout = self.layout
        layout.operator(TemplateImportOperator.bl_idname)
