bl_info = {
    "name" : "VRC Facetracking Shapekeys",
    "author" : "Adjerry91",
    "version" : (0,3,0),
    "blender" : (3,0,0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Shape Keys",
}

import bpy
from bpy.types import (Menu, Operator, Panel, PropertyGroup)
from bpy.props import (BoolProperty, IntProperty, StringProperty, BoolVectorProperty, EnumProperty, PointerProperty)

blender_version = bool(bpy.app.version >= (2, 80, 0))

if blender_version:
    user_preferences = bpy.context.preferences
else:
    bl_info['blender'] = (2, 79, 0)
    user_preferences = bpy.context.user_preferences

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
            "MouthLowerOverlay"
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
# Shape Key Operators    
# -------------------------------------------------------------------    
            
class VRCFT_CreateShapeKeys(bpy.types.Operator):
    """Creates VRChat Facetracking Shapekeys"""    
    bl_label = "Create VRChat Facetracking Shape Keys"
    bl_idname = "vrcft.create_shapekeys"
    
    def execute(self, context):
        object = bpy.context.object
        scene = context.scene
        vrcft_tools = scene.vrcft_tools
        active_object = bpy.context.active_object
        
        #Check if there is shape keys on the mesh
        if context.object.data.shape_keys:
                             
            #Create beginning seperation marker for VRCFT Shape Keys
            object.shape_key_add(name=VRCFT_Labels[0],from_mix=False) 
            
            #Clear all existing values for shape keys
            bpy.ops.object.shape_key_clear()
            
            
            #I am really sorry for the following code. I could not figure out how to do property list that would work with the UI
            
            if vrcft_tools.shapekey_1 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[1],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_1)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_1].value = 1
                object.shape_key_add(name=VRCFT_Labels[1],from_mix=True)
                bpy.ops.object.shape_key_clear()
            
            if vrcft_tools.shapekey_2 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[2],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_2)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_2].value = 1
                object.shape_key_add(name=VRCFT_Labels[2],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_3 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[3],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_3)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_3].value = 1
                object.shape_key_add(name=VRCFT_Labels[3],from_mix=True)
                bpy.ops.object.shape_key_clear()            
            
            if vrcft_tools.shapekey_4 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[4],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_4)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_4].value = 1
                object.shape_key_add(name=VRCFT_Labels[4],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_5 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[5],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_5)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_5].value = 1
                object.shape_key_add(name=VRCFT_Labels[5],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_6 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[6],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_6)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_6].value = 1
                object.shape_key_add(name=VRCFT_Labels[6],from_mix=True)
                bpy.ops.object.shape_key_clear()                

            if vrcft_tools.shapekey_7 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[7],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_7)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_7].value = 1
                object.shape_key_add(name=VRCFT_Labels[7],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_8 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[8],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_8)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_8].value = 1
                object.shape_key_add(name=VRCFT_Labels[8],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_9 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[9],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_9)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_9].value = 1
                object.shape_key_add(name=VRCFT_Labels[9],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_10 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[10],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_10)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_10].value = 1
                object.shape_key_add(name=VRCFT_Labels[10],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_11 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[11],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_11)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_11].value = 1
                object.shape_key_add(name=VRCFT_Labels[11],from_mix=True)
                bpy.ops.object.shape_key_clear()   
            
            if vrcft_tools.shapekey_12 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[12],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_12)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_12].value = 1
                object.shape_key_add(name=VRCFT_Labels[12],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_13 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[13],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_13)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_13].value = 1
                object.shape_key_add(name=VRCFT_Labels[13],from_mix=True)
                bpy.ops.object.shape_key_clear()            
            
            if vrcft_tools.shapekey_14 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[14],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_14)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_14].value = 1
                object.shape_key_add(name=VRCFT_Labels[14],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_15 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[15],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_15)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_15].value = 1
                object.shape_key_add(name=VRCFT_Labels[15],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_16 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[16],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_16)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_16].value = 1
                object.shape_key_add(name=VRCFT_Labels[16],from_mix=True)
                bpy.ops.object.shape_key_clear()                

            if vrcft_tools.shapekey_17 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[17],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_17)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_17].value = 1
                object.shape_key_add(name=VRCFT_Labels[17],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_18 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[18],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_18)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_18].value = 1
                object.shape_key_add(name=VRCFT_Labels[18],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_19 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[19],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_19)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_19].value = 1
                object.shape_key_add(name=VRCFT_Labels[19],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_20 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[20],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_20)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_20].value = 1
                object.shape_key_add(name=VRCFT_Labels[20],from_mix=True)
                bpy.ops.object.shape_key_clear()                                      
            
            if vrcft_tools.shapekey_21 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[21],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_21)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_21].value = 1
                object.shape_key_add(name=VRCFT_Labels[21],from_mix=True)
                bpy.ops.object.shape_key_clear()   
            
            if vrcft_tools.shapekey_22 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[22],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_22)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_22].value = 1
                object.shape_key_add(name=VRCFT_Labels[22],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_23 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[23],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_23)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_23].value = 1
                object.shape_key_add(name=VRCFT_Labels[23],from_mix=True)
                bpy.ops.object.shape_key_clear()            
            
            if vrcft_tools.shapekey_24 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[24],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_24)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_24].value = 1
                object.shape_key_add(name=VRCFT_Labels[24],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_25 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[25],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_25)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_25].value = 1
                object.shape_key_add(name=VRCFT_Labels[25],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_26 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[26],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_26)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_26].value = 1
                object.shape_key_add(name=VRCFT_Labels[26],from_mix=True)
                bpy.ops.object.shape_key_clear()                

            if vrcft_tools.shapekey_27 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[27],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_27)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_27].value = 1
                object.shape_key_add(name=VRCFT_Labels[27],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_28 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[28],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_28)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_28].value = 1
                object.shape_key_add(name=VRCFT_Labels[28],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_29 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[29],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_29)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_29].value = 1
                object.shape_key_add(name=VRCFT_Labels[29],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_30 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[30],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_30)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_30].value = 1
                object.shape_key_add(name=VRCFT_Labels[30],from_mix=True)
                bpy.ops.object.shape_key_clear()                                      
            
            if vrcft_tools.shapekey_31 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[31],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_31)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_31].value = 1
                object.shape_key_add(name=VRCFT_Labels[31],from_mix=True)
                bpy.ops.object.shape_key_clear()   
            
            if vrcft_tools.shapekey_32 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[32],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_32)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_32].value = 1
                object.shape_key_add(name=VRCFT_Labels[32],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_33 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[33],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_33)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_33].value = 1
                object.shape_key_add(name=VRCFT_Labels[33],from_mix=True)
                bpy.ops.object.shape_key_clear()            
            
            if vrcft_tools.shapekey_34 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[34],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_34)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_34].value = 1
                object.shape_key_add(name=VRCFT_Labels[34],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_35 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[35],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_35)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_35].value = 1
                object.shape_key_add(name=VRCFT_Labels[35],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_36 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[36],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_36)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_36].value = 1
                object.shape_key_add(name=VRCFT_Labels[36],from_mix=True)
                bpy.ops.object.shape_key_clear()                

            if vrcft_tools.shapekey_37 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[37],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_37)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_37].value = 1
                object.shape_key_add(name=VRCFT_Labels[37],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_38 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[38],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_38)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_38].value = 1
                object.shape_key_add(name=VRCFT_Labels[38],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_39 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[39],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_39)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_39].value = 1
                object.shape_key_add(name=VRCFT_Labels[39],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_40 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[40],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_40)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_40].value = 1
                object.shape_key_add(name=VRCFT_Labels[40],from_mix=True)
                bpy.ops.object.shape_key_clear()                                      
            
            if vrcft_tools.shapekey_41 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[41],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_41)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_41].value = 1
                object.shape_key_add(name=VRCFT_Labels[41],from_mix=True)
                bpy.ops.object.shape_key_clear()   
            
            if vrcft_tools.shapekey_42 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[42],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_42)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_42].value = 1
                object.shape_key_add(name=VRCFT_Labels[42],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_43 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[43],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_43)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_43].value = 1
                object.shape_key_add(name=VRCFT_Labels[43],from_mix=True)
                bpy.ops.object.shape_key_clear()            
            
            if vrcft_tools.shapekey_44 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[44],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_44)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_44].value = 1
                object.shape_key_add(name=VRCFT_Labels[44],from_mix=True)
                bpy.ops.object.shape_key_clear()
                
            if vrcft_tools.shapekey_45 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[45],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_45)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_45].value = 1
                object.shape_key_add(name=VRCFT_Labels[45],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_46 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[46],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_46)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_46].value = 1
                object.shape_key_add(name=VRCFT_Labels[46],from_mix=True)
                bpy.ops.object.shape_key_clear()                

            if vrcft_tools.shapekey_47 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[47],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_47)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_47].value = 1
                object.shape_key_add(name=VRCFT_Labels[47],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_48 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[48],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_48)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_48].value = 1
                object.shape_key_add(name=VRCFT_Labels[48],from_mix=True)
                bpy.ops.object.shape_key_clear()

            if vrcft_tools.shapekey_49 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[49],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_49)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_49].value = 1
                object.shape_key_add(name=VRCFT_Labels[49],from_mix=True)
                bpy.ops.object.shape_key_clear()                

            if vrcft_tools.shapekey_50 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[50],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_50)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_50].value = 1
                object.shape_key_add(name=VRCFT_Labels[50],from_mix=True)
                bpy.ops.object.shape_key_clear() 

            if vrcft_tools.shapekey_51 == 'Basis':
                object.shape_key_add(name=VRCFT_Labels[51],from_mix=False)
            else:
                #Find shapekey enterred and mix to create new shapekey              
                active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(vrcft_tools.shapekey_51)
                object.data.shape_keys.key_blocks[vrcft_tools.shapekey_51].value = 1
                object.shape_key_add(name=VRCFT_Labels[51],from_mix=True)
                bpy.ops.object.shape_key_clear() 


            #Create end seperation marker for VRCFT Shape Keys    
            object.shape_key_add(name=VRCFT_Labels[len(VRCFT_Labels)-1],from_mix=False)
                     

            
            
            self.report({'INFO'}, "VRC Facetracking Shapekeys have been created")                
        else:
            #Error message if basis does not exist
            self.report({'WARNING'}, "No shape keys found on mesh")
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
        wm = context.window_manager
        object = bpy.context.object
        

        
        box = layout.box()
        col = box.column(align=True)
        
        #Start List of Shapekeys from VRCFT labels list
        for i in range(1,len(VRCFT_Labels)-1,1): 
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text = VRCFT_Labels[i] + ":")
            row.prop(vrcft_tools, 'shapekey_' + str(i), icon='SHAPEKEY_DATA') 
               
        row = layout.row()
        row.operator("vrcft.create_shapekeys", icon='MESH_MONKEY')

# -------------------------------------------------------------------
# Properties    
# -------------------------------------------------------------------

class VRCFT_Properties(PropertyGroup):
            
    #List of VRCFT Shapes variables to be used by UI
    #Must equal the VRCFT labels
    shapekey_1 : StringProperty(name = "", default = "Basis")       
    shapekey_2 : StringProperty(name = "", default = "Basis")    
    shapekey_3 : StringProperty(name = "", default = "Basis")
    shapekey_4 : StringProperty(name = "", default = "Basis")
    shapekey_5 : StringProperty(name = "", default = "Basis")
    shapekey_6 : StringProperty(name = "", default = "Basis")
    shapekey_7 : StringProperty(name = "", default = "Basis")
    shapekey_8 : StringProperty(name = "", default = "Basis")
    shapekey_9 : StringProperty(name = "", default = "Basis")
    shapekey_10 : StringProperty(name = "", default = "Basis")
    shapekey_11 : StringProperty(name = "", default = "Basis")
    shapekey_12 : StringProperty(name = "", default = "Basis")
    shapekey_13 : StringProperty(name = "", default = "Basis")
    shapekey_14 : StringProperty(name = "", default = "Basis")
    shapekey_15 : StringProperty(name = "", default = "Basis")
    shapekey_16 : StringProperty(name = "", default = "Basis")
    shapekey_17 : StringProperty(name = "", default = "Basis")
    shapekey_18 : StringProperty(name = "", default = "Basis")
    shapekey_19 : StringProperty(name = "", default = "Basis")
    shapekey_20 : StringProperty(name = "", default = "Basis")
    shapekey_21 : StringProperty(name = "", default = "Basis")
    shapekey_22 : StringProperty(name = "", default = "Basis")
    shapekey_23 : StringProperty(name = "", default = "Basis")
    shapekey_24 : StringProperty(name = "", default = "Basis")
    shapekey_25 : StringProperty(name = "", default = "Basis")
    shapekey_26 : StringProperty(name = "", default = "Basis")
    shapekey_27 : StringProperty(name = "", default = "Basis")
    shapekey_28 : StringProperty(name = "", default = "Basis")
    shapekey_29 : StringProperty(name = "", default = "Basis")
    shapekey_30 : StringProperty(name = "", default = "Basis")
    shapekey_31 : StringProperty(name = "", default = "Basis")
    shapekey_32 : StringProperty(name = "", default = "Basis")
    shapekey_33 : StringProperty(name = "", default = "Basis")
    shapekey_34 : StringProperty(name = "", default = "Basis")
    shapekey_35 : StringProperty(name = "", default = "Basis")
    shapekey_36 : StringProperty(name = "", default = "Basis")
    shapekey_37 : StringProperty(name = "", default = "Basis")
    shapekey_38 : StringProperty(name = "", default = "Basis")
    shapekey_39 : StringProperty(name = "", default = "Basis")
    shapekey_40 : StringProperty(name = "", default = "Basis")
    shapekey_41 : StringProperty(name = "", default = "Basis")
    shapekey_42 : StringProperty(name = "", default = "Basis")
    shapekey_43 : StringProperty(name = "", default = "Basis")
    shapekey_44 : StringProperty(name = "", default = "Basis")
    shapekey_45 : StringProperty(name = "", default = "Basis")
    shapekey_46 : StringProperty(name = "", default = "Basis")
    shapekey_47 : StringProperty(name = "", default = "Basis")
    shapekey_48 : StringProperty(name = "", default = "Basis")
    shapekey_49 : StringProperty(name = "", default = "Basis")
    shapekey_50 : StringProperty(name = "", default = "Basis")
    shapekey_51 : StringProperty(name = "", default = "Basis")

    shapekeys : StringProperty()


# -------------------------------------------------------------------
# Register
# -------------------------------------------------------------------

classes = (
    VRCFT_Properties,
    VRCFT_CreateShapeKeys,
    VRCFT_UI
#    SearchEnumOperatorone
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