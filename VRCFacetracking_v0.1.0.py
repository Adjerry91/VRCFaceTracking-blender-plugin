bl_info = {
    "name" : "VRCFacetracking Shapekeys",
    "author" : "Adjerry91",
    "version" : (0,1,0),
    "blender" : (3,0,0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Shape Keys",
}

import bpy

class VRCFT_main_panel(bpy.types.Panel):   
    bl_label = "VRCFacetracking"
    bl_idname = "VRCFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRCFT"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="VRChat Facetracking", icon='MESH_MONKEY')
        row.operator("vrcft.create_shapekeys")
        
            
class VRCFT_CreateShapeKeys(bpy.types.Operator):
    """Creates VRChat Facetracking Shapekeys"""    
    bl_label = "Create Shape Keys"
    bl_idname = "vrcft.create_shapekeys"
    


    def execute(self, context):
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
            "EyesY",
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
        
        for x in range(len(VRCFT_Labels)): 
            bpy.context.object.shape_key_add(name=VRCFT_Labels[x],from_mix=True)
            

        
        return{'FINISHED'}


classes = [VRCFT_main_panel,VRCFT_CreateShapeKeys]
 
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
         
 
 
if __name__ == "__main__":
    register()