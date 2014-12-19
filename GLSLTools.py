bl_info = {
    "name": "GLSL Tools",
    "description": "Adds a tab to the toolbar with some custom tools",
    "author": "TARDIS Maker",
    "version": (0, 0, 0),
    "blender": (2, 72, 2),
    "location": "Tool Shelf > Custom Tools",
    "warning": "Still a WIP",
    "category": "Custom"}

import bpy
from bpy.types import Menu, Panel, UIList     
    
####################
# Custom Operators #
####################

### Select Camera ###
class SelectCamera(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "select.camera"
    bl_label = "Select Active Camera"

    #@classmethod
    #def poll(cls, context):
        
    
    def execute(self, context):
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.scene.objects.active = bpy.context.scene.camera
        bpy.context.scene.camera.select = True   

        return {'FINISHED'}

### Recalculate Draw Order ###
class DrawOrderObjects ():

    def __init__(self, x, y, z, name):
        self.x_axis = x
        self.y_axis = y
        self.z_axis = z

        self.name = name

class RecalculateDrawOrder(bpy.types.Operator):
    """Recalculate the GLSL Draw Order of the selected objects"""
    bl_idname = "recalculate.draw_order"
    bl_label = "Recalculate Draw Order"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ### Convinience Vars ###
        scene = bpy.context.scene
        selected = bpy.context.selected_objects
        object = bpy.ops.object
        
        bpy.context.scene.camera.select = False
        
        
        ### A list to contain the selected objects
        objects = []        
        
        ### Loop through selected objets and add them to the list
        for obj in selected:
            scene.objects.active = obj

            objects.append(DrawOrderObjects(obj.location.x, obj.location.y, obj.location.z, obj.name))
        
        ### Debugging info ###
        for i in objects: #print name and y axis location of each of the objects for debugging
            print(i.y_axis) #y axis
            print(i.name) #name
        
        ### Sort list to put objects in proper order based on Y axis location
        sortedobjects = sorted(objects, key=lambda object: object.y_axis) #sort through list
        
        ### Debugging info ###
        print ("sorted") 
        for i in sortedobjects: #print name and y axis location of each of the objects for debugging
            print(i.y_axis) #y axis
            print(i.name) #name
        
        ### Add empty and add parent selected objects to it
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        tmpempty = scene.objects.active.name
        
        for i in sortedobjects:
            bpy.context.scene.objects[i.name].select=True
        
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        
        
        ### Deselct Everything ###
        bpy.ops.object.select_all(action='DESELECT')
        
        ### Unparent Objects for the empty ###
        for i in sortedobjects:
            bpy.context.scene.objects[i.name].select=True
            bpy.ops.object.parent_clear(type='CLEAR')
        
        ### Deselct Everything ###
        bpy.ops.object.select_all(action='DESELECT')
        
        #select empty and delete it
        scene.objects.active = bpy.context.scene.objects[tmpempty]
        bpy.context.scene.objects[tmpempty].select=True
        bpy.ops.object.delete()
        
        ### Select Camera ###
        #bpy.ops.object.select_all(action='SELECT')
        bpy.ops.select.camera()
        
        return {'FINISHED'}


### Recalculate Draw Order and Parent to an Empty ###
class RecalculateDrawOrderEmpty(bpy.types.Operator):
    """Recalculate the GLSL Draw Order of the selected objects and Parent to an Empty"""
    bl_idname = "recalculate.draw_order_empty"
    bl_label = "Recalculate Draw Order to Empty"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ### Convinience Vars ###
        scene = bpy.context.scene
        selected = bpy.context.selected_objects
        object = bpy.ops.object
        
        
        ### A list to contain the selected objects
        objects = []        
        
        ### Loop through selected objets and add them to the list
        for obj in selected:
            scene.objects.active = obj

            objects.append(DrawOrderObjects(obj.location.x, obj.location.y, obj.location.z, obj.name))
        
        ### Debugging info ###
        for i in objects: #print name and y axis location of each of the objects for debugging
            print(i.y_axis) #y axis
            print(i.name) #name
        
        ### Sort list to put objects in proper order based on Y axis location
        sortedobjects = sorted(objects, key=lambda object: object.y_axis) #sort through list
        
        ### Debugging info ###
        print ("sorted") 
        for i in sortedobjects: #print name and y axis location of each of the objects for debugging
            print(i.y_axis) #y axis
            print(i.name) #name
        
        ### Add empty and add parent selected objects to it
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        tmpempty = scene.objects.active.name
        
        for i in sortedobjects:
            bpy.context.scene.objects[i.name].select=True
        
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        
        
        ### Deselct Everything ###
        bpy.ops.object.select_all(action='DESELECT')
        
        ### Unparent Objects for the empty ###
        for i in sortedobjects:
            bpy.context.scene.objects[i.name].select=True
            bpy.ops.object.parent_clear(type='CLEAR')
        
        ### Deselct Everything ###
        bpy.ops.object.select_all(action='DESELECT')
        
        #select empty and delete it
        scene.objects.active = bpy.context.scene.objects[tmpempty]
        bpy.context.scene.objects[tmpempty].select=True
        bpy.ops.object.delete()
        
        
        ### Add empty and add parent selected objects to it
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        tmpempty = scene.objects.active.name
        
        for i in sortedobjects:
            bpy.context.scene.objects[i.name].select=True
        
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        
        
        ### Deselct Everything ###
        bpy.ops.object.select_all(action='DESELECT')
        
        ### Select Empty ###
        scene.objects.active = bpy.context.scene.objects[tmpempty]
        bpy.context.scene.objects[tmpempty].select=True
        
        return {'FINISHED'}


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
        
        col = layout.column(align=True)
        col.operator("recalculate.draw_order")
        col.operator("recalculate.draw_order_empty")

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
        #col.operator("select.cameras")
        


#######################
# Register/Unregister #
#######################
def register():
    
    bpy.utils.register_class(GLSLTools_DrawOrder_Panel)
    bpy.utils.register_class(RecalculateDrawOrder)
    bpy.utils.register_class(SelectCamera)
    bpy.utils.register_class(GLSLTools_Select_Camera)
    bpy.utils.register_class(RecalculateDrawOrderEmpty)
    
    
    
    

def unregister():
    bpy.utils.unregister_class(GLSLTools)
    bpy.utils.unregister_class(GLSLTools_DrawOrder)
    bpy.utils.unregister_class(RecalculateDrawOrder)
    bpy.utils.unregister_class(SelectCamera)
    bpy.utils.unregister_class(GLSLTools_Select_Camera)
    bpy.utils.unregister_class(RecalculateDrawOrderEmpty)

if __name__ == "__main__":
    register()

