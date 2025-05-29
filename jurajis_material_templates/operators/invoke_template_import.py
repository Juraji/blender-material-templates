import bpy
from bpy.types import Operator, Context

from ..properties import props_from_ctx


class InvokeTemplateImportOperator(Operator):
    bl_idname = "template_import.template_import_ui"
    bl_label = "Import Template"
    bl_description = "Import template data from another .blend file."

    def invoke(self, context: Context, event):
        self.cleanup_template_data(context)
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context: Context):
        layout = self.layout
        props = props_from_ctx(context)

        layout.label(text="Step 1: Select Template")
        layout.prop(props, "template_file")

        layout.separator()
        layout.operator("template_import.auto_match")

        layout.template_list(
            "TemplateImportMappingList", "",
            props, "mapping_items",
            props, "mapping_index")

        layout.operator("template_import.apply_template_data", text="Apply")

    def execute(self, context):
        # TODO: Oh god, gotta copy all the things
        return {"FINISHED"}

    def cancel(self, context: Context):
        self.cleanup_template_data(context)

    @staticmethod
    def cleanup_template_data(context: Context):
        props = props_from_ctx(context)

        template_name = props.source_collection_name
        linked_coll = bpy.data.collections.get(template_name)
        if linked_coll:
            bpy.data.collections.remove(linked_coll, do_unlink=True)

        props.mapping_items.clear()
        props.template_file = ""
