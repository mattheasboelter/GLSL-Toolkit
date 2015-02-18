bl_info = {
    "name": "GLSL Tools",
    "description": "Adds a tab to the toolbar with some custom tools",
    "author": "TARDIS Maker",
    "version": (0, 0, 0),
    "blender": (2, 72, 2),
    "location": "Tool Shelf > Custom Tools",
    "warning": "Still a WIP",
    "category": "Custom"}

if "bpy" in locals():
  import imp
  imp.reload(recalcdraworder)
  imp.reload(selectcamera)
  imp.reload(ui)
  print("Reloaded multifiles")
else:
  from . import recalcdraworder, selectcamera, ui
  print("Imported multifiles")

import bpy
from bpy.props import *



#######################
# Register/Unregister #
#######################
def register():
    bpy.utils.register_module(__name__)
    
    ### CUSTOM PROPERTIES ###
    bpy.types.WindowManager.order_axis = bpy.props.EnumProperty(
        name="Draw Order Axis",
        items=(
            ('+X', '+X', 'Positive X Axis'),
            ('+Y', '+Y', 'Positive Y Axis'),
            ('+Z', '+Z', 'Positive Z Axis'),
            ('-X', '-X', 'Negative X Axis'),
            ('-Y', '-Y', 'Negative Y Axis'),
            ('-Z', '-Z', 'Negative Z Axis'),
        ),
        default='+Y'
    )

def unregister():
    bpy.utils.register_module(__name__)
       
    del bpy.types.WindowManager.order_axis


if __name__ == "__main__":
    register()

