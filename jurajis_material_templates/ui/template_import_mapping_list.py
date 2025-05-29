import bpy
from typing import Any

from bpy.types import UIList, Context, UILayout


class TemplateImportMappingList(UIList):
    bl_idname = "TemplateImportMappingList"

    def draw_item(self,
                  context: Context,
                  layout: UILayout,
                  data: Any | None,
                  item: Any | None,
                  icon: int | None,
                  active_data: Any,
                  active_property: str | None,
                  index: int | None,
                  flt_flag: int | None):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row(align=True)
            row.label(text=item.source_object_name)
            row.prop(item, "target_object", text="")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="")


    def filter_items(self, context, data, prop):
        helper_funcs = bpy.types.UI_UL_list

        items = getattr(data, prop)
        ordered = []

        # Filter
        if self.filter_name:
            filtered = helper_funcs.filter_items_by_name(
                self.filter_name,
                self.bitflag_filter_item,
                items,
                propname="source_object_name",
                reverse=False)
        else:
            filtered = [self.bitflag_filter_item] * len(items)

        if self.use_filter_sort_alpha:
            ordered = helper_funcs.sort_items_by_name(items, "source_object_name")

        return filtered, ordered

