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

#from bpy.props import (IntProperty,
#                       BoolProperty,
#                       FloatProperty,
#                       StringProperty,
#                       PointerProperty,
#                       CollectionProperty,
#                       EnumProperty
#                       )
#                       
#from bpy.types import (Operator,
#                       Panel,
#                       UIList,
#                       PropertyGroup
#                       )

# -------------------------------------------------------------------
# VRChat Facetracking Shapekey List   
# -------------------------------------------------------------------

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



# -------------------------------------------------------------------
# Helper    
# -------------------------------------------------------------------

def shape_key_selection(op, context):
    shape_key_names = []

    for shapekey in context.object.data.shape_keys.key_blocks:
        shape_key_names.append(shapekey.name) 
                
    return shape_key_names


# -------------------------------------------------------------------
# Properties    
# -------------------------------------------------------------------

class VRCFT_Properties(bpy.types.PropertyGroup):
    
#    for x in range(len(VRCFT_Labels)): 
#        shapekey_enum1 : bpy.props.EnumProperty(
#            name = "",
#            description = "Shapekey",
#            items = [('OP1', "Shapekey1",""),
#                     ('OP2', "Shapekey2",""),
#                     ('OP3', "Shapekey3","")    
#            ]
#        )
        
    shapekey_enum1 : bpy.props.EnumProperty(
        name = "",
        description = "Shapekey",
        items = [('Basis', "Basis","")  
        ]
    )
    

# -------------------------------------------------------------------
# Shape Key Operators    
# -------------------------------------------------------------------    
            
class VRCFT_CreateShapeKeys(bpy.types.Operator):
    """Creates VRChat Facetracking Shapekeys"""    
    bl_label = "Create VRChat Facetracking Shape Keys"
    bl_idname = "vrcft.create_shapekeys"
    
    def execute(self, context):
        object = bpy.context.object

        #Warn user to select mesh fist before creating shape keys

        if context.object.data.shape_keys:
            
            
            #Import existing shape keys
            
            #DEBUG Shape Key List
#            self.report({'INFO'},"List of existing shapekeys on the mesh:")
#            shape_keys = (shape_key_selection(self, context))
#            for i in shape_keys:
#                shapekey = object.data.shape_keys.key_blocks[i]
#                self.report({'INFO'},shapekey.name)
#            num_SK_blocks = len(object.data.shape_keys.key_blocks)
#            self.report({'INFO'}, "Number of existing shapekeys: " + str(num_SK_blocks))
            
            
            #Create new shape keys    
            for i in range(len(VRCFT_Labels)): 
                
                #Mix Shapekey to selections made on the UI

                #Add shape key
                object.shape_key_add(name=VRCFT_Labels[i],from_mix=False)
     
            self.report({'INFO'}, "VRC Facetracking Shapekeys have been created")    
                    
        else:
            #Error message if basis does not exist
            self.report({'INFO'}, "No shape keys found on mesh")
        return{'FINISHED'}

# -------------------------------------------------------------------
# User Interface  
# -------------------------------------------------------------------

class VRCFT_UI(bpy.types.Panel):   
    bl_label = "VRChat Facetracking"
    bl_idname = "VRCFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRCFT"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        vrcft_tools = scene.vrcft_tools
        
        object = bpy.context.object
        
        box = layout.box()
        col = box.column(align=True)
        
        #Start List of Shapekeys from VRCFT labels list
        for i in range(1,len(VRCFT_Labels)-1,1): 
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text = VRCFT_Labels[i] + ":")
            row.prop(vrcft_tools, 'shapekey_enum1', icon='SHAPEKEY_DATA')
            
            
            #Create shapekey dropdown to select existing shape keys to assign
#            shape_keys = (shape_key_selection(self, context))
#    
#            for i in shape_keys:
#                shapekey = object.data.shape_keys.key_blocks[i]
#            row.prop(self, "shape_keys", icon='SHAPEKEY_DATA')



        #TEST
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(vrcft_tools, "shapekey_test", icon='SHAPEKEY_DATA')
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(context.scene, 'mouth_a', icon='SHAPEKEY_DATA') 
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(context.scene, 'mouth_o', icon='SHAPEKEY_DATA')
#        row = col.row(align=True)
#        row.scale_y = 1.1
#        row.prop(context.scene, 'mouth_ch', icon='SHAPEKEY_DATA')
          

                       
        
        row = layout.row()
        row.operator("vrcft.create_shapekeys", icon='MESH_MONKEY')

# -------------------------------------------------------------------
# Register
# -------------------------------------------------------------------

classes = (
    VRCFT_Properties,
    VRCFT_CreateShapeKeys,
    VRCFT_UI
)
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.vrcft_tools = bpy.props.PointerProperty(type=VRCFT_Properties)
        
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.vrcft_tools
 
if __name__ == "__main__":
    register()