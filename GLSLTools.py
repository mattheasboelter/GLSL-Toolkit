bl_info = {
    "name": "GLSL Tools",
    "description": "Adds a tab to the toolbar with some custom tools",
    "author": "TARDIS Maker",
    "version": (0, 0, 0),
    "blender": (2, 72, 2),
    "location": "Tool Shelf > Custom Tools",
    "warning": "",
    "category": "Custom"}

import bpy
from bpy.types import Menu, Panel, UIList     
    
####################
# Custom Operators #
####################
class DrawOrderObjects ():

    def __init__(self, x, y, z, name):
        self.x_axis = x
        self.y_axis = y
        self.z_axis = z

        self.name = name

def main(context):
    scene = bpy.context.scene
    selected = bpy.context.selected_objects
    object = bpy.ops.object

    objects = []

    for obj in selected:
        scene.objects.active = obj

        objects.append(DrawOrderObjects(obj.location.x, obj.location.y, obj.location.z, obj.name))

    for i in objects: #print name and y axis location of each of the objects for debugging
        print(i.y_axis) #y axis
        print(i.name) #name

    sortedobjects = sorted(objects, key=lambda object: object.y_axis) #sort through list

    print ("sorted") 
    for i in sortedobjects: #print name and y axis location of each of the objects for debugging
        print(i.y_axis) #y axis
        print(i.name) #name

    bpy.ops.object.empty_add(type='PLAIN_AXES')
    
    for i in sortedobjects:
        bpy.context.scene.objects[i.name].select=True
    
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    tmpempty = scene.objects.active.name
    
    
    bpy.ops.object.select_all(action='DESELECT')
    
    for i in sortedobjects:
        bpy.context.scene.objects[i.name].select=True
        bpy.ops.object.parent_clear(type='CLEAR')
    
    bpy.ops.object.select_all(action='DESELECT')
    
    #select empty and delete it
    scene.objects.active = bpy.context.scene.objects[tmpempty]
    bpy.context.scene.objects[tmpempty].select=True
    bpy.ops.object.delete()


class RecalculateDrawOrder(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "recalculate.draw_order"
    bl_label = "Recalculate Draw Order"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}



########### TOOLSHELF TAB ##############
class GLSLTools_ImportImages_Panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "GLSL Tools"
    bl_context = "objectmode"
    bl_label = "Import Images"
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("import_image.to_plane")


class GLSLTools_DrawOrder_Panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "GLSL Tools"
    bl_context = "objectmode"
    bl_label = "Draw Order"
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("recalculate.draw_order")
        



def register():
    bpy.utils.register_class(GLSLTools_ImportImages_Panel)
    bpy.utils.register_class(GLSLTools_DrawOrder_Panel)
    bpy.utils.register_class(RecalculateDrawOrder)


def unregister():
    bpy.utils.unregister_class(GLSLTools)
    bpy.utils.unregister_class(GLSLTools_DrawOrder)
    bpy.utils.unregister_class(RecalculateDrawOrder)


if __name__ == "__main__":
    register()

