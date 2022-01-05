bl_info = {
    "name" : "VRC Facetracking Shapekeys",
    "author" : "Adjerry91",
    "version" : (0,2,0),
    "blender" : (3,0,0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Shape Keys",
}

import bpy

# -------------------------------------------------------------------
# VRChat Facetracking Shapekey List   
# -------------------------------------------------------------------

VRCFT_Labels = [
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

    #List of VRCFT Shapes variables to be used by UI
    #Must equal the VRCFT labels

    # Should probably allocate these dynamically at some point, not sure how to do this at the moment
    shapekey_0 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_1 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_2 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_3 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_4 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_5 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_6 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_7 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_8 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_9 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_10 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_11 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_12 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_13 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_14 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_15 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_16 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_17 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_18 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_19 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_20 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_21 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_22 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_23 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_24 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_25 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_26 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_27 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_28 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_29 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_30 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_31 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_32 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_33 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_34 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_35 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_36 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_37 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_38 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_39 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_40 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_41 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_42 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_43 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_44 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_45 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_46 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_47 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_48 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_49 : bpy.props.StringProperty(name = "", default = "Basis")
    shapekey_50 : bpy.props.StringProperty(name = "", default = "Basis")


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
            object.shape_key_add(name="~~ VRCFacetracking ~~",from_mix=False)

            #Clear all existing values for shape keys
            bpy.ops.object.shape_key_clear()

            for x in range(len(VRCFT_Labels)):
                curr_key = eval("vrcft_tools.shapekey_" + str(x))
                if curr_key == "Basis":
                    object.shape_key_add(name=VRCFT_Labels[x], from_mix=False)
                else:
                    # Find shapekey enterred and mix to create new shapekey
                    active_object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(
                        curr_key)
                    object.data.shape_keys.key_blocks[curr_key].value = 1
                    object.shape_key_add(name=VRCFT_Labels[x], from_mix=True)
                    bpy.ops.object.shape_key_clear()

            #Create end seperation marker for VRCFT Shape Keys
            object.shape_key_add(name="~~ END OF VRCFacetracking ~~",from_mix=False)

            #DEBUG REPORT STAT OF EACH OF THE CONTROLS
#            self.report({'INFO'}, str(VRCFT_Labels[1]) + " mixed with " + str(vrcft_tools.shapekey_1))
#            self.report({'INFO'}, str(VRCFT_Labels[2]) + " mixed with " + str(vrcft_tools.shapekey_2))
#            self.report({'INFO'}, str(VRCFT_Labels[3]) + " mixed with " + str(vrcft_tools.shapekey_3))
#            self.report({'INFO'}, str(VRCFT_Labels[4]) + " mixed with " + str(vrcft_tools.shapekey_4))
#            self.report({'INFO'}, str(VRCFT_Labels[5]) + " mixed with " + str(vrcft_tools.shapekey_5))
#            self.report({'INFO'}, str(VRCFT_Labels[6]) + " mixed with " + str(vrcft_tools.shapekey_6))
#            self.report({'INFO'}, str(VRCFT_Labels[7]) + " mixed with " + str(vrcft_tools.shapekey_7))
#            self.report({'INFO'}, str(VRCFT_Labels[8]) + " mixed with " + str(vrcft_tools.shapekey_8))
#            self.report({'INFO'}, str(VRCFT_Labels[9]) + " mixed with " + str(vrcft_tools.shapekey_9))
#            self.report({'INFO'}, str(VRCFT_Labels[10]) + " mixed with " + str(vrcft_tools.shapekey_10))
#            self.report({'INFO'}, str(VRCFT_Labels[11]) + " mixed with " + str(vrcft_tools.shapekey_11))
#            self.report({'INFO'}, str(VRCFT_Labels[12]) + " mixed with " + str(vrcft_tools.shapekey_12))
#            self.report({'INFO'}, str(VRCFT_Labels[13]) + " mixed with " + str(vrcft_tools.shapekey_13))
#            self.report({'INFO'}, str(VRCFT_Labels[14]) + " mixed with " + str(vrcft_tools.shapekey_14))
#            self.report({'INFO'}, str(VRCFT_Labels[15]) + " mixed with " + str(vrcft_tools.shapekey_15))
#            self.report({'INFO'}, str(VRCFT_Labels[16]) + " mixed with " + str(vrcft_tools.shapekey_16))
#            self.report({'INFO'}, str(VRCFT_Labels[17]) + " mixed with " + str(vrcft_tools.shapekey_17))
#            self.report({'INFO'}, str(VRCFT_Labels[18]) + " mixed with " + str(vrcft_tools.shapekey_18))
#            self.report({'INFO'}, str(VRCFT_Labels[19]) + " mixed with " + str(vrcft_tools.shapekey_19))
#            self.report({'INFO'}, str(VRCFT_Labels[20]) + " mixed with " + str(vrcft_tools.shapekey_20))
#            self.report({'INFO'}, str(VRCFT_Labels[21]) + " mixed with " + str(vrcft_tools.shapekey_21))
#            self.report({'INFO'}, str(VRCFT_Labels[22]) + " mixed with " + str(vrcft_tools.shapekey_22))
#            self.report({'INFO'}, str(VRCFT_Labels[23]) + " mixed with " + str(vrcft_tools.shapekey_23))
#            self.report({'INFO'}, str(VRCFT_Labels[24]) + " mixed with " + str(vrcft_tools.shapekey_24))
#            self.report({'INFO'}, str(VRCFT_Labels[25]) + " mixed with " + str(vrcft_tools.shapekey_25))
#            self.report({'INFO'}, str(VRCFT_Labels[26]) + " mixed with " + str(vrcft_tools.shapekey_26))
#            self.report({'INFO'}, str(VRCFT_Labels[27]) + " mixed with " + str(vrcft_tools.shapekey_27))
#            self.report({'INFO'}, str(VRCFT_Labels[28]) + " mixed with " + str(vrcft_tools.shapekey_28))
#            self.report({'INFO'}, str(VRCFT_Labels[29]) + " mixed with " + str(vrcft_tools.shapekey_29))
#            self.report({'INFO'}, str(VRCFT_Labels[30]) + " mixed with " + str(vrcft_tools.shapekey_30))
#            self.report({'INFO'}, str(VRCFT_Labels[31]) + " mixed with " + str(vrcft_tools.shapekey_31))
#            self.report({'INFO'}, str(VRCFT_Labels[32]) + " mixed with " + str(vrcft_tools.shapekey_32))
#            self.report({'INFO'}, str(VRCFT_Labels[33]) + " mixed with " + str(vrcft_tools.shapekey_33))
#            self.report({'INFO'}, str(VRCFT_Labels[34]) + " mixed with " + str(vrcft_tools.shapekey_34))
#            self.report({'INFO'}, str(VRCFT_Labels[35]) + " mixed with " + str(vrcft_tools.shapekey_35))
#            self.report({'INFO'}, str(VRCFT_Labels[36]) + " mixed with " + str(vrcft_tools.shapekey_36))
#            self.report({'INFO'}, str(VRCFT_Labels[37]) + " mixed with " + str(vrcft_tools.shapekey_37))
#            self.report({'INFO'}, str(VRCFT_Labels[38]) + " mixed with " + str(vrcft_tools.shapekey_38))
#            self.report({'INFO'}, str(VRCFT_Labels[39]) + " mixed with " + str(vrcft_tools.shapekey_39))
#            self.report({'INFO'}, str(VRCFT_Labels[40]) + " mixed with " + str(vrcft_tools.shapekey_40))
#            self.report({'INFO'}, str(VRCFT_Labels[41]) + " mixed with " + str(vrcft_tools.shapekey_41))
#            self.report({'INFO'}, str(VRCFT_Labels[42]) + " mixed with " + str(vrcft_tools.shapekey_42))
#            self.report({'INFO'}, str(VRCFT_Labels[43]) + " mixed with " + str(vrcft_tools.shapekey_43))
#            self.report({'INFO'}, str(VRCFT_Labels[44]) + " mixed with " + str(vrcft_tools.shapekey_44))
#            self.report({'INFO'}, str(VRCFT_Labels[45]) + " mixed with " + str(vrcft_tools.shapekey_45))
#            self.report({'INFO'}, str(VRCFT_Labels[46]) + " mixed with " + str(vrcft_tools.shapekey_46))
#            self.report({'INFO'}, str(VRCFT_Labels[47]) + " mixed with " + str(vrcft_tools.shapekey_47))
#            self.report({'INFO'}, str(VRCFT_Labels[48]) + " mixed with " + str(vrcft_tools.shapekey_48))
#            self.report({'INFO'}, str(VRCFT_Labels[49]) + " mixed with " + str(vrcft_tools.shapekey_49))
#            self.report({'INFO'}, str(VRCFT_Labels[50]) + " mixed with " + str(vrcft_tools.shapekey_50))
#            self.report({'INFO'}, str(VRCFT_Labels[51]) + " mixed with " + str(vrcft_tools.shapekey_51))


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
        del bpy.types.Scene.vrcft_shapekeys

if __name__ == "__main__":
    register()
