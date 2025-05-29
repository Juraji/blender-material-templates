from bpy.types import Operator, Context, Object, bpy_struct

from ..properties import props_from_ctx


class TemplateImportOperator(Operator):
    bl_idname = "template_import.template_import_ui"
    bl_label = "Import Template"
    bl_description = "Import template data from another .blend file."
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    def invoke(self, context: Context, event):
        props = props_from_ctx(context)
        props.cleanup()
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context: Context):
        layout = self.layout
        props = props_from_ctx(context)

        layout.prop(props, "template_file")
        layout.separator()
        layout.operator("template_import.auto_match")

        layout.template_list(
            "OBJECT_UL_mapping_list", "",
            props, "mapping_items",
            props, "mapping_index")

    def execute(self, context):
        props = props_from_ctx(context)
        mapping_items: list[TemplateMappingItem] = props.mapping_items

        source_to_target_map: dict[Object, Object | None] = {
            item.source_object: item.target_object
            for item in mapping_items
            if item.source_object and item.target_object
        }

        for source, target in source_to_target_map.items():
            if not target:
                # No mapping for this object
                continue

            self.copy_materials(source, target)
            self.copy_modifiers(source, target)
            self.copy_object_name(source, target)
            self.copy_parentage(source_to_target_map, source, target)

        props.cleanup()
        return {"FINISHED"}

    def cancel(self, context: Context):
        props = props_from_ctx(context)
        props.cleanup()

    @staticmethod
    def copy_materials(source: Object, target: Object):
        for idx, target_slot in enumerate(target.material_slots):
            name = target_slot.material.name

            # Rename source mat so it doesn't cause 001 naming of our target
            target_slot.material.name = f"{name}_REPLACED"

            source_mat = source.material_slots[idx].material
            source_mat.name = name
            target_slot.material = source_mat

    @classmethod
    def copy_modifiers(cls, source: Object, target: Object):
        for source_mod in source.modifiers:
            target_mod = target.modifiers.new(name=source_mod.name, type=source_mod.type)
            cls.copy_writable_properties(source_mod, target_mod)

    @staticmethod
    def copy_object_name(source, target):
        desired_name = source.name
        # Rename source obj so it doesn't cause 001 naming of our target
        source.name = f"{desired_name}_SOURCE"
        target.name = desired_name

    @staticmethod
    def copy_parentage(source_to_target_map, source, target):
        if not source.parent:
            # Source does not have a parent
            return

        source_parent = source.parent
        target_parent = None
        while source_parent:
            target_parent = source_to_target_map.get(source_parent)
            if target_parent:
                break
            source_parent = source_parent.parent

        if target_parent and target_parent != target:
            target_local_matrix = target_parent.matrix_world.inverted() @ target.matrix_world
            target.parent = target_parent
            target.matrix_basis = target_local_matrix
        else:
            target.parent = None

    @staticmethod
    def copy_writable_properties(source: bpy_struct, target: bpy_struct):
        properties = [p.identifier for p in source.bl_rna.properties if not p.is_readonly]

        for prop in properties:
            setattr(target, prop, getattr(source, prop))
