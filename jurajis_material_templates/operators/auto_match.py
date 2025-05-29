from os import path

import bpy
from bpy.path import abspath
from bpy.types import Operator, Context

from ..properties import props_from_ctx, TemplateMappingItem
from ..utils.str import strip_suffix


class AutoMatchOperator(Operator):
    bl_idname = "template_import.auto_match"
    bl_label = "Run Auto-Match"
    bl_description = "Matches objects from a source file to objects in the current file."

    @classmethod
    def poll(cls, context):
        props = props_from_ctx(context)
        return props.is_template_file_set()

    def execute(self, context: Context):
        props = props_from_ctx(context)

        filepath = abspath(props.template_file)

        if not (filepath and path.isfile(filepath) and filepath.lower().endswith(".blend")):
            self.report({'ERROR'}, "Invalid or missing .blend file.")
            return {"CANCELLED"}

        self.report({'INFO'}, f"Loading mappings from {path.basename(filepath)}...")
        props.cleanup()

        try:
            c_name = props.source_collection_name
            if not c_name in bpy.data.collections:
                with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                    if c_name in data_from.collections:
                        data_to.collections.append(c_name)
                    else:
                        self.report({'ERROR'}, "No 'TEMPLATE' collection found in source file.")
                        return {"CANCELLED"}

            linked_collection = bpy.data.collections.get(c_name)
            if not linked_collection:
                self.report({'ERROR'}, f"Linked collection '{c_name}' not found after loading.")
                return {'CANCELLED'}

            for src_obj in linked_collection.objects:
                src_obj_name = strip_suffix(src_obj.name)

                # 1. Exact match by obj name
                target_obj = context.scene.objects.get(src_obj_name)

                if not target_obj and src_obj.data:
                    src_mesh_name = strip_suffix(src_obj.data.name)

                    # 2. Exact match by mesh data name
                    target_obj = next(
                        (o for o in context.scene.objects
                         if o.data and strip_suffix(o.data.name) == src_mesh_name),
                        None
                    )

                    # 3. Starts-with match by mesh data name
                    if not target_obj:
                        target_obj = next(
                            (o for o in context.scene.objects
                             if o.data and strip_suffix(o.data.name).startswith(src_mesh_name)),
                            None
                        )

                item: TemplateMappingItem = props.mapping_items.add()
                item.source_object_name = src_obj_name
                item.source_object = src_obj
                item.target_object = target_obj

            self.report({'INFO'}, f"{len(props.mapping_items)} matches generated.")
        except Exception as e:
            self.report({'ERROR'}, f"Auto-match failed: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}
