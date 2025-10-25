from bpy.types import Operator

from ..properties import props_from_ctx


class ClearMatchesOperator(Operator):
    bl_idname = "template_import.clear_matches"
    bl_label = "Clear Matches"
    bl_description = "Clear current matches."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        props = props_from_ctx(context)
        return len(props.mapping_items) > 0

    def execute(self, context):
        props = props_from_ctx(context)

        for item in props.mapping_items:
            item.target_object = None

        return {"FINISHED"}
