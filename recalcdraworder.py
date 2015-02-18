import bpy

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
    
    use_empty = bpy.props.BoolProperty(name="use empty")
    
    
    ##### POLL METHOD #####
    ### Defines When operator can be used ###
    # If there is a camera, and more than two objects #
    # (not including the camera) are selected, it can be run #
    @classmethod
    def poll(cls, context):
        if bpy.context.scene.camera != False:
            if bpy.context.selected_objects != False:
                if len(bpy.context.selected_objects) > 1:
                    if bpy.context.camera.select == True:
                        return
                else:
                    return

    def execute(self, context):
        ### Convinience Vars ###
        scene = bpy.context.scene
        selected = bpy.context.selected_objects
        object = bpy.ops.object
        draworderaxis = bpy.context.window_manager.order_axis
        
        
        ### Deselect Camera ###
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
        
        ### Sort by Axis specified by custom draworderaxis enum prop ###
        if draworderaxis == '+X':
            sortedobjects = sorted(objects, key=lambda object: object.x_axis)
        elif draworderaxis == '+Y':
            sortedobjects = sorted(objects, key=lambda object: object.y_axis)
        elif draworderaxis == '+Z':
            sortedobjects = sorted(objects, key=lambda object: object.z_axis)
        elif draworderaxis == '-X':
            sortedobjects = sorted(objects, key=lambda object: object.x_axis, reverse=True)
        elif draworderaxis == '-Y':
            sortedobjects = sorted(objects, key=lambda object: object.y_axis, reverse=True)
        elif draworderaxis == '-Z':
            sortedobjects = sorted(objects, key=lambda object: object.z_axis, reverse=True)
        
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
        
        if self.use_empty == True:
            for i in sortedobjects:
                bpy.context.scene.objects[i.name].select=True
            
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            
            bpy.ops.object.select_all(action='DESELECT')
            
            scene.objects.active = bpy.context.scene.objects[tmpempty]
            bpy.context.scene.objects[tmpempty].select=True
        else:
            #select empty and delete it
            scene.objects.active = bpy.context.scene.objects[tmpempty]
            bpy.context.scene.objects[tmpempty].select=True
            bpy.ops.object.delete()
            
            ### Select Camera ###
            #bpy.ops.object.select_all(action='SELECT')
            bpy.ops.select.camera()
        
        
        return {'FINISHED'}
