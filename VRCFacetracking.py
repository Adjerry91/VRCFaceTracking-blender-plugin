bl_info = {
    "name" : "VRC Facetracking Shapekeys",
    "author" : "Adjerry91",
    "version" : (1,0,3),
    "blender" : (3,0,0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Shape Keys",
}

import bpy
import math

from bpy.types import (Scene, Menu, Operator, Panel, PropertyGroup)
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
            "EyesConstrict",
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
# Functions  
# -------------------------------------------------------------------

def duplicate_shapekey(string):
    active_object = bpy.context.active_object
    
    #Check shape keys if duplicate
    if active_object.data.shape_keys.key_blocks.find(string) >= 0:
#        print("Duplicate shape key found!")       
        return True
    else:          
        return False
    
def version_2_79_or_older():
    return bpy.app.version < (2, 80)

def unselect_all():
    for obj in get_objects():
        select(obj, False)

def get_objects():
    return bpy.context.scene.objects if version_2_79_or_older() else bpy.context.view_layer.objects

def set_active(obj, skip_sel=False):
    if not skip_sel:
        select(obj)
    if version_2_79_or_older():
        bpy.context.scene.objects.active = obj
    else:
        bpy.context.view_layer.objects.active = obj
        
def select(obj, sel=True):
    if sel:
        hide(obj, False)
    if version_2_79_or_older():
        obj.select = sel
    else:
        obj.select_set(sel)

def hide(obj, val=True):
    if hasattr(obj, 'hide'):
        obj.hide = val
    if not version_2_79_or_older():
        obj.hide_set(val)
        
def get_armature(armature_name=None):
    if not armature_name:
        armature_name = bpy.context.scene.armature
    for obj in get_objects():
        if obj.type == 'ARMATURE':
            if (armature_name and obj.name == armature_name) or not armature_name:
                return obj
    return None
    
def get_meshes_objects(armature_name=None, mode=2, check=True, visible_only=False):
    # Modes:
    # 0 = With armatures only
    # 1 = Top level only
    # 2 = All meshes
    # 3 = Selected only

    if not armature_name:
        armature = get_armature()
        if armature:
            armature_name = armature.name

    meshes = []
    for ob in get_objects():
        if ob.type == 'MESH':
            if mode == 0 or mode == 5:
                if ob.parent:
                    if ob.parent.type == 'ARMATURE' and ob.parent.name == armature_name:
                        meshes.append(ob)
                    elif ob.parent.parent and ob.parent.parent.type == 'ARMATURE' and ob.parent.parent.name == armature_name:
                        meshes.append(ob)

            elif mode == 1:
                if not ob.parent:
                    meshes.append(ob)

            elif mode == 2:
                meshes.append(ob)

            elif mode == 3:
                if is_selected(ob):
                    meshes.append(ob)

    if visible_only:
        for mesh in meshes:
            if is_hidden(mesh):
                meshes.remove(mesh)

    # Check for broken meshes and delete them
    if check:
        current_active = get_active()
        to_remove = []
        for mesh in meshes:
            selected = is_selected(mesh)
            # print(mesh.name, mesh.users)
            set_active(mesh)

            if not get_active():
                to_remove.append(mesh)

            if not selected:
                select(mesh, False)

        for mesh in to_remove:
            print('DELETED CORRUPTED MESH:', mesh.name, mesh.users)
            meshes.remove(mesh)
            delete(mesh)

        if current_active:
            set_active(current_active)

    return meshes

def get_shapekeys_vrcft(self, context):
    return get_shapekeys(context, [], False, False, False)

def get_shapekeys(context, names, no_basis, decimation, return_list):
    choices = []
    choices_simple = []
    meshes_list = get_meshes_objects(check=False)

    if decimation:
        meshes = meshes_list
    elif meshes_list:
        meshes = [get_objects().get(context.scene.vrcft_mesh)]  
    else:
        bpy.types.Object.Enum = choices
        return bpy.types.Object.Enum

    for mesh in meshes:
        if not mesh or not has_shapekeys(mesh):
            bpy.types.Object.Enum = choices
            return bpy.types.Object.Enum

        for shapekey in mesh.data.shape_keys.key_blocks:
            name = shapekey.name
            if name in choices_simple:
                continue
            if no_basis and name == 'Basis':
                continue
            if decimation and name in Decimation.ignore_shapes:
                continue
            # 1. Will be returned by context.scene
            # 2. Will be shown in lists
            # 3. will be shown in the hover description (below description)
            choices.append((name, name, ''))
            choices_simple.append(name)

#    choices.sort(key=lambda x: tuple(x[0].lower()))

    choices2 = []
    for name in names:
        if name in choices_simple and len(choices) > 1 and choices[0][0] != name:
            if decimation and name in Decimation.ignore_shapes:
                continue
            choices2.append((name, name, name))

    for choice in choices:
        choices2.append(choice)

    bpy.types.Object.Enum = choices2

    if return_list:
        shape_list = []
        for choice in choices2:
            shape_list.append(choice[0])
        return shape_list

    return bpy.types.Object.Enum

def get_meshes(self, context):
    # Modes:
    # 0 = With Armature only
    # 1 = Without armature only
    # 2 = All meshes

    choices = []

    for mesh in get_meshes_objects(mode=2, check=False):
        choices.append((mesh.name, mesh.name, mesh.name))

    bpy.types.Object.Enum = sorted(choices, key=lambda x: tuple(x[0].lower()))
    return bpy.types.Object.Enum

def has_shapekeys(mesh):
    if not hasattr(mesh.data, 'shape_keys'):
        return False
    return hasattr(mesh.data.shape_keys, 'key_blocks')


# -------------------------------------------------------------------
# Shape Key Operators    
# -------------------------------------------------------------------    

class VRCFT_OT_CreateShapeKeys(Operator):
    """Creates VRChat Facetracking Shapekeys"""
    bl_label = "Create VRChat Facetracking Shape Keys"
    bl_idname = "vrcft.create_shapekeys"

    def execute(self, context):

        object = bpy.context.object        
        scene = context.scene       
        vrcft_mesh = scene.vrcft_mesh
        active_object = bpy.context.active_object
        mesh = bpy.ops.mesh
        ops = bpy.ops

        #Set the selected mesh to active object
        mesh = get_objects()[vrcft_mesh]
        self.report({'INFO'}, "Selected mesh is: " + str(vrcft_mesh))
        set_active(mesh)


        #Check if there is shape keys on the mesh
        if object.data.shape_keys: 
            
            #Create beginning seperation marker for VRCFT Shape Keys
            if duplicate_shapekey("~~ VRCFacetracking ~~") == False :    
                object.shape_key_add(name="~~ VRCFacetracking ~~", from_mix=False)
                    
            #Clear all existing values for shape keys
            ops.object.shape_key_clear()

            for x in range(len(VRCFT_Labels)):
                curr_key = eval("scene.vrcft_shapekeys_" + str(x))
                
                #Check if blend with 'Basis' shape key
                if curr_key == "Basis":
                    #Check for duplicates
                    if duplicate_shapekey(VRCFT_Labels[x]) == False :
                        object.shape_key_add(name=VRCFT_Labels[x], from_mix=False)
                    #Do not overwrite if the shape key exists and is on 'Basis'
                        
                else:                                     
                    #Check for duplicates
                    if duplicate_shapekey(VRCFT_Labels[x]) == False :
                        # Find shapekey enterred and mix to create new shapekey
                        object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(curr_key)
                        object.data.shape_keys.key_blocks[curr_key].value = 1                      
                        object.shape_key_add(name=VRCFT_Labels[x], from_mix=True)                        
                    else:
                        #Mix to existing shape key duplicate
                        object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(VRCFT_Labels[x])
                        object.data.shape_keys.key_blocks[curr_key].value = 1
                        ops.object.mode_set(mode='EDIT', toggle=False)
                        bpy.ops.mesh.select_mode(type="VERT")
                        ops.mesh.select_all(action='SELECT')
                        ops.mesh.blend_from_shape(shape=curr_key, blend=1.0, add=False)
                        self.report({'INFO'}, "Existing VRC facetracking shape key: " + VRCFT_Labels[x] + " has been overwritten with: " + curr_key)
                    #Clear shape key weights    
                    ops.object.shape_key_clear()
                        

            #Create end seperation marker for VRCFT Shape Keys
            if duplicate_shapekey("~~ END OF VRCFacetracking ~~") == False : 
                object.shape_key_add(name="~~ END OF VRCFacetracking ~~",from_mix=False)                
            self.report({'INFO'}, "VRC facetracking shapekeys have been created on mesh")
            
                
            #Cleanup mode state
            ops.object.mode_set(mode='OBJECT', toggle=False)
            
            #Move active shape to 'Basis'
            active_object.active_shape_key_index = 0
                
        else:
            #Error message if basis does not exist
            self.report({'WARNING'}, "No shape keys found on mesh")
        return{'FINISHED'}

# -------------------------------------------------------------------
# User Interface  
# -------------------------------------------------------------------

class VRCFT_UL(Panel):
    bl_label = "VRChat Facetracking"
    bl_idname = "VRCFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRCFT"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        vrcft_mesh = scene.vrcft_mesh
        object = bpy.context.object
        
        #Start Layout
        col = layout.column()
        
        #Mesh Selection
        mesh = get_objects()[vrcft_mesh]
        mesh_count = len(get_meshes_objects(check=False, mode=2))     
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(context.scene, 'vrcft_mesh', icon='MESH_DATA')
        col.separator()                       
        row = col.row(align=True)
        
        #Check mesh selections        
        if vrcft_mesh and has_shapekeys(mesh):
            #Info
            
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Select shape keys to create VRCFT shape keys.', icon='INFO')
            col.separator()
            
            #Start Box
            box = layout.box()
            col = box.column(align=True)

            #Start List of Shapekeys from VRCFT labels list
            for i in range(len(VRCFT_Labels)):
                row = col.row(align=True)
                row.scale_y = 1.1
                row.label(text = VRCFT_Labels[i] + ":")
                row.prop(scene, 'vrcft_shapekeys_' + str(i), icon='SHAPEKEY_DATA')                 
            row = layout.row()
            row.operator("vrcft.create_shapekeys", icon='MESH_MONKEY')
        else:
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Select the mesh with face shape keys.', icon='INFO')
            col.separator()
        
# -------------------------------------------------------------------
# Register
# -------------------------------------------------------------------

classes = (
    VRCFT_OT_CreateShapeKeys,
    VRCFT_UL
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
      
    # Shape keys
    Scene.vrcft_mesh = EnumProperty(name='Mesh',description='Mesh to apply VRCFT shape keys',items=get_meshes)
    for i, vrcft_shape in enumerate(VRCFT_Labels):
        setattr(Scene, "vrcft_shapekeys_" + str(i), EnumProperty(name='',description='Select shapekey to use for VRCFT',items=get_shapekeys_vrcft))
        


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls) 
        
    # Shape keys
    del Scene.vrcft_mesh
#    for i in enumerate(VRCFT_Labels):  
          
    del Scene.vrcft_shapekeys_0
    del Scene.vrcft_shapekeys_1
    del Scene.vrcft_shapekeys_2
    del Scene.vrcft_shapekeys_3
    del Scene.vrcft_shapekeys_4
    del Scene.vrcft_shapekeys_5
    del Scene.vrcft_shapekeys_6
    del Scene.vrcft_shapekeys_7
    del Scene.vrcft_shapekeys_8
    del Scene.vrcft_shapekeys_9
    del Scene.vrcft_shapekeys_10
    del Scene.vrcft_shapekeys_11
    del Scene.vrcft_shapekeys_12
    del Scene.vrcft_shapekeys_13
    del Scene.vrcft_shapekeys_14
    del Scene.vrcft_shapekeys_15
    del Scene.vrcft_shapekeys_16
    del Scene.vrcft_shapekeys_17
    del Scene.vrcft_shapekeys_18
    del Scene.vrcft_shapekeys_19
    del Scene.vrcft_shapekeys_20
    del Scene.vrcft_shapekeys_21
    del Scene.vrcft_shapekeys_22
    del Scene.vrcft_shapekeys_23
    del Scene.vrcft_shapekeys_24
    del Scene.vrcft_shapekeys_25
    del Scene.vrcft_shapekeys_26
    del Scene.vrcft_shapekeys_27
    del Scene.vrcft_shapekeys_28
    del Scene.vrcft_shapekeys_29
    del Scene.vrcft_shapekeys_30
    del Scene.vrcft_shapekeys_31
    del Scene.vrcft_shapekeys_32
    del Scene.vrcft_shapekeys_33
    del Scene.vrcft_shapekeys_34
    del Scene.vrcft_shapekeys_35
    del Scene.vrcft_shapekeys_36
    del Scene.vrcft_shapekeys_37
    del Scene.vrcft_shapekeys_38
    del Scene.vrcft_shapekeys_39
    del Scene.vrcft_shapekeys_40
    del Scene.vrcft_shapekeys_41
    del Scene.vrcft_shapekeys_42
    del Scene.vrcft_shapekeys_43
    del Scene.vrcft_shapekeys_44
    del Scene.vrcft_shapekeys_45
    del Scene.vrcft_shapekeys_46
    del Scene.vrcft_shapekeys_47
#    del Scene.vrcft_shapekeys_48
#    del Scene.vrcft_shapekeys_49
        

if __name__ == "__main__":
    register()
