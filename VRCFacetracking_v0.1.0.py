bl_info = {
    "name" : "VRC Facetracking Shapekeys",
    "author" : "Adjerry91",
    "version" : (0,1,0),
    "blender" : (3,0,0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Shape Keys",
}

import bpy

VRCFT_Labels = [
            "~~ VRCFacetracking ~~",
            "LeftEyeLid",
            "RightEyeLid",
            "CombinedEyeLid",
            "EyesWiden",
            "EyesDilation",
            "EyesSqueeze",
            "LeftEyeX",
            "RightEyeX",
            "LeftEyeY",
            "RightEyeY",
            "LeftEyeWiden",
            "RightEyeWiden",
            "LeftEyeSqueeze",
            "RightEyeSqueeze",
            "JawRight",
            "JawLeft",
            "JawForward",
            "JawOpen",
            "MouthApeShape",
            "MouthUpperRight",
            "MouthUpperLeft",
            "MouthLowerRight",
            "MouthLowerLeft",
            "MouthUpperOverturn",
            "MouthLowerOverturn",
            "MouthPout",
            "MouthSmileRight",
            "MouthSmileLeft",
            "MouthSadRight",
            "MouthSadLeft",
            "CheekPuffRight",
            "CheekPuffLeft",
            "CheekSuck",
            "MouthUpperUpRight",
            "MouthUpperUpLeft",
            "MouthLowerDownRight",
            "MouthLowerDownLeft",
            "MouthUpperInside",
            "MouthLowerInside",
            "MouthLowerOverlay",
            "TongueLongStep1",
            "TongueLongStep2",
            "TongueDown",
            "TongueUp",
            "TongueRight",
            "TongueLeft",
            "TongueRoll",
            "TongueUpLeftMorph",
            "TongueUpRightMorph",
            "TongueDownLeftMorph",
            "TongueDownRightMorph",
            "~~ END OF VRCFacetracking ~~"
        ]



class VRCFT_UI(bpy.types.Panel):   
    bl_label = "VRChat Facetracking"
    bl_idname = "VRCFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRCFT"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        
        #Select Mesh
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.label(text = "Mesh:")
#        row.label(text = "Object")
#        row.prop(context.scene, 'mesh_name_viseme', icon='MESH_DATA')
#        col.separator()
        
        
        #Start List of Shapekeys
        for x in range(1,len(VRCFT_Labels)-1,1): 
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text = VRCFT_Labels[x] + ":")
#            Insert prop selection of other shapekey to mix to
#            row.prop(context.scene, 'LeftEyeLid', icon='SHAPEKEY_DATA')
            row.label(text = "Shapekey Selection")
                      
             
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(context.scene, 'LeftEyeLid', icon='SHAPEKEY_DATA')
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(context.scene, 'RightEyeLid', icon='SHAPEKEY_DATA')
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(context.scene, 'CombinedEyeLid', icon='SHAPEKEY_DATA')
        
        
        
        row = layout.row()
        row.operator("vrcft.create_shapekeys", icon='MESH_MONKEY')
        
            
class VRCFT_CreateShapeKeys(bpy.types.Operator):
    """Creates VRChat Facetracking Shapekeys"""    
    bl_label = "Create VRChat Facetracking Shape Keys"
    bl_idname = "vrcft.create_shapekeys"
    
    def execute(self, context):
        object = bpy.context.object

#        Check if basis exists
#        bpy.context.active_object.data.shape_keys.key_blocks[0] = False

        
#        Code to find and warn of existing shapekeys           
#        bpy.context.active_object.data.shape_keys.key_blocks.find("Basis")
#        for x in range(len(VRCFT_Labels)):

        
        for x in range(len(VRCFT_Labels)): 
            
#            Create shape key
            object.shape_key_add(name=VRCFT_Labels[x],from_mix=False)
 
       
        return{'FINISHED'}


classes = (
    VRCFT_UI,
    VRCFT_CreateShapeKeys
)
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
 
if __name__ == "__main__":
    register()