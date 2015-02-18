import bpy

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
