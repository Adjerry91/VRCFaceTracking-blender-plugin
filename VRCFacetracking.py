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
            "LeftEyeLid",
            "RightEyeLid",
            "CombinedEyeLid",
            "EyesWiden",
            "EyesDilation",
            "EyesSqueeze",
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
            self.report({'INFO'}, "VRC Facetracking Shapekeys have been created")
        else:
            #Error message if basis does not exist
            self.report({'WARNING'}, "No shape keys found on mesh")
        return{'FINISHED'}

# -------------------------------------------------------------------
# User Interface  
# -------------------------------------------------------------------

class VRCFT_UI(Panel):
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
        for i in range(len(VRCFT_Labels)):
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
