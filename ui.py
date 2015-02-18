import bpy
from bpy.types import Menu, Panel, UIList

################## 
# TOOLSHELF TABS #
##################

### Recalculate Draw Order ###
class GLSLTools_DrawOrder_Panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "GLSL Tools"
    bl_context = "objectmode"
    bl_label = "Draw Order"
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
          
        col = layout.column(align=True)
        col.operator("recalculate.draw_order").use_empty=False
        col.operator("recalculate.draw_order", text="Recalculate Draw Order to Empty").use_empty=True
        
        col = layout.column(align=False)
        col.prop(wm, "order_axis")
        
        

### Select Camera ###    
class GLSLTools_Select_Camera(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "GLSL Tools"
    bl_context = "objectmode"
    bl_label = "Select Camera"
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("select.camera")
