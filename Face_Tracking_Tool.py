bl_info = {
    "name" : "Face Tracking Tool",
    "author" : "Adjerry91",
    "version" : (2,0,1),
    "blender" : (3,1,2),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Shape Keys",
}

import bpy
import math

from bpy.types import (Scene, Menu, Operator, Panel, PropertyGroup)
from bpy.props import (BoolProperty, IntProperty, FloatProperty, StringProperty, BoolVectorProperty, EnumProperty, PointerProperty)

blender_version = bool(bpy.app.version >= (2, 80, 0))

if blender_version:
    user_preferences = bpy.context.preferences
else:
    bl_info['blender'] = (2, 79, 0)
    user_preferences = bpy.context.user_preferences

# -------------------------------------------------------------------
# SRanipal Facetracking Shapekey List
# -------------------------------------------------------------------

SRanipal_Labels = [
            "Eye_Left_squeeze",
            "Eye_Right_squeeze",
            "Eye_Left_Blink",
            "Eye_Left_Right",
            "Eye_Left_Left",
            "Eye_Left_Down",
            "Eye_Left_Up",
            "Eye_Right_Blink",
            "Eye_Right_Right",
            "Eye_Right_Left",
            "Eye_Right_Down",
            "Eye_Right_Up",
            "Eye_Left_Wide",
            "Eye_Right_Wide",
            "Eye_Left_Dilation",
            "Eye_Left_Constrict",
            "Eye_Right_Dilation",
            "Eye_Right_Constrict",
            "Jaw_Right",
            "Jaw_Left",
            "Jaw_Forward",
            "Jaw_Open",
            "Mouth_Ape_Shape",
            "Mouth_Left",
            "Mouth_Right",
            "Mouth_Upper_Right",
            "Mouth_Upper_Left",
            "Mouth_Lower_Right",
            "Mouth_Lower_Left",
            "Mouth_Smile_Right",
            "Mouth_Smile_Left",
            "Mouth_Sad_Right",
            "Mouth_Sad_Left",
            "Mouth_Pout",
            "Cheek_Puff_Right",
            "Cheek_Puff_Left",
            "Cheek_Suck",
            "Mouth_Upper_Up",
            "Mouth_Lower_Down",
            "Mouth_Upper_UpRight",
            "Mouth_Upper_UpLeft",
            "Mouth_Lower_DownRight",
            "Mouth_Lower_DownLeft",
            "Mouth_O_Shape",
            "Mouth_Upper_Overturn",
            "Mouth_Lower_Overturn",
            "Mouth_Upper_Inside",
            "Mouth_Lower_Inside",
            "Mouth_Lower_Overlay",
            "Tongue_LongStep1",
            "Tongue_LongStep2",
            "Tongue_Down",
            "Tongue_Up",
            "Tongue_Right",
            "Tongue_Left",
            "Tongue_Roll",
            "Tongue_UpRight_Morph",
            "Tongue_UpLeft_Morph",
            "Tongue_DownRight_Morph",
            "Tongue_DownLeft_Morph",
        ]

FT_Visemes = [
            "FT_SIL",
            "FT_PP",
            "FT_FF",
            "FT_TH",
            "FT_DD",
            "FT_KK",
            "FT_CH",
            "FT_SS",
            "FT_NN",
            "FT_RR",
            "FT_AA",
            "FT_EE",
            "FT_IH",
            "FT_OH",
            "FT_OU",
        ]

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------

def duplicate_shapekey(string):
    active_object = bpy.context.active_object

    #Check shape keys if duplicate
    if active_object.data.shape_keys.key_blocks.find(string) >= 0:
        #print("Duplicate shape key found!")
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

def get_shapekeys_ft(self, context):
    return get_shapekeys(context, [], False, False, False)

def get_shapekeys(context, names, no_basis, decimation, return_list):
    choices = []
    choices_simple = []
    meshes_list = get_meshes_objects(check=False)

    if decimation:
        meshes = meshes_list
    elif meshes_list:
        meshes = [get_objects().get(context.scene.ft_mesh)]
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

# Returns [delta_v in 3 parts, by vert idx], and a bounding box (-x, +x, -y, +y, -z, +z)
def get_shapekey_delta(mesh, shapekey_name):
    deltas = []
    bounding_box = [math.inf, -math.inf, math.inf, -math.inf, math.inf, -math.inf]

    basis_key = mesh.data.shape_keys.key_blocks["Basis"]
    active_key = mesh.data.shape_keys.key_blocks[shapekey_name]
    for idx, vert in enumerate(basis_key.data):
        delta = (active_key.data[idx].co[0] - vert.co[0],
                active_key.data[idx].co[1] - vert.co[1],
                active_key.data[idx].co[2] - vert.co[2])

        deltas.append(delta)
        # If this vertex moved any, adjust our bounding box
        if (math.fabs(delta[0]) + math.fabs(delta[1]) + math.fabs(delta[2])) > 0.001:
            bounding_box[0] = min(bounding_box[0], vert.co[0])
            bounding_box[1] = max(bounding_box[1], vert.co[0])
            bounding_box[2] = min(bounding_box[2], vert.co[1])
            bounding_box[3] = max(bounding_box[3], vert.co[1])
            bounding_box[4] = min(bounding_box[4], vert.co[2])
            bounding_box[5] = max(bounding_box[5], vert.co[2])

    return deltas, bounding_box

# Map a range 0-1 where the middle e.g. 0.2x is linearly interpolated
def crossfade(val, min_x, max_x, middle_percent):
    val_norm = (val - min_x) / (max_x - min_x)
    if val_norm < (.5 - (middle_percent / 2)):
        # full
        return 1
    if val_norm > (.5 + (middle_percent / 2)):
        # other side
        return 0
    else:
        # middle, linear falloff
        return 1 - ((val_norm - (.5 - (middle_percent / 2))) / middle_percent)

# -------------------------------------------------------------------
# Shape Key Operators
# -------------------------------------------------------------------

class FT_OT_CreateShapeKeys(Operator):
    """Creates SRanipal Facetracking Shape Keys"""
    bl_label = "Create SRanipal Face Tracking Shape Keys"
    bl_idname = "ft.create_shapekeys"

    def execute(self, context):

        object = bpy.context.object
        scene = context.scene
        ft_mesh = scene.ft_mesh
        active_object = bpy.context.active_object
        mesh = bpy.ops.mesh
        ops = bpy.ops

        #Set the selected mesh to active object
        mesh = get_objects()[ft_mesh]
        self.report({'INFO'}, "Selected mesh is: " + str(ft_mesh))
        set_active(mesh)

        #Check if there is shape keys on the mesh
        if object.data.shape_keys:

            #Create beginning seperation marker for VRCFT Shape Keys
            if duplicate_shapekey("~~ SRanipal Face Tracking ~~") == False :
                object.shape_key_add(name="~~ SRanipal Face Tracking ~~", from_mix=False)

            #Clear all existing values for shape keys
            ops.object.shape_key_clear()

            for x in range(len(SRanipal_Labels)):
                curr_key = eval("scene.ft_shapekey_" + str(x))
                curr_key_enable = eval("scene.ft_shapekey_enable_" + str(x))
                #Skip key if shape is disabled
                if not curr_key_enable:
                    continue
                # determine if we're going to be working with visemes
                label = SRanipal_Labels[x]
                basis_key = get_shapekeys_ft(self, context)[0][0]
                generate_eyes = (any(string in label for string in ['Blink', 'squeeze', 'Wide']) and
                    context.scene.ft_blink != basis_key )
                generate_jaw = (any(string in label for string in ['Jaw']) and context.scene.ft_aa != basis_key)
                generate_mouth = (any(string in label for string in ['Upper_Up', 'Lower_Down', 'Upper_Left', 'Lower_Right', 'Upper_Right', 'Lower_Left', 'Inside', 'Pout', 'Mouth_Left', 'Mouth_Right']) and context.scene.ft_ch != basis_key and context.scene.ft_oh != basis_key)
                generate_smile = (any(string in label for string in ['Smile']) and context.scene.ft_smile != basis_key)
                generate_frown = (any(string in label for string in ['Sad']) and context.scene.ft_frown != basis_key)

                #Check if blend with 'Basis' shape key
                if curr_key == "Basis" and not (generate_eyes or generate_jaw or generate_frown or generate_mouth or generate_smile):
                    #Check for duplicates
                    if not duplicate_shapekey(SRanipal_Labels[x]):
                        object.shape_key_add(name=SRanipal_Labels[x], from_mix=False)
                    #Do not overwrite if the shape key exists and is on 'Basis'

                else:
                    #Check for duplicates
                    if not duplicate_shapekey(SRanipal_Labels[x]):
                        # Special handling for visemes
                        if generate_eyes:
                            object.shape_key_add(name=SRanipal_Labels[x], from_mix=False)
                            deltas, _ = get_shapekey_delta(object, context.scene.ft_blink)
                            factor = 1
                            if 'squeeze' in label:
                                factor = 1.1
                            elif 'Wide' in label:
                                factor = -0.15
                            for idx, vert in enumerate(object.data.shape_keys.key_blocks[label].data):
                                # No cross-fading for eyes
                                if 'Left' in label and vert.co[0] < 0:
                                    continue
                                if 'Right' in label and vert.co[0] > 0:
                                    continue
                                object.data.shape_keys.key_blocks[label].data[idx].co[0] += (deltas[idx][0] * factor)
                                object.data.shape_keys.key_blocks[label].data[idx].co[1] += (deltas[idx][1] * factor)
                                object.data.shape_keys.key_blocks[label].data[idx].co[2] += (deltas[idx][2] * factor)
                        elif generate_mouth:
                            object.shape_key_add(name=SRanipal_Labels[x], from_mix=False)
                            ch_deltas, bounding_box = get_shapekey_delta(object, context.scene.ft_ch)
                            oh_deltas, _ = get_shapekey_delta(object, context.scene.ft_oh)
                            # consider vertices where delta(v_ch) > delta(v_oh) upper lip, and vice versa
                            ch_should_be_greater = 'Upper' in label
                            both_lips = any(string in label for string in ['Pout', 'Mouth_Left', 'Mouth_Right'])

                            for idx, vert in enumerate(object.data.shape_keys.key_blocks[label].data):
                                ch_greater = (math.hypot(ch_deltas[idx][0], ch_deltas[idx][1], ch_deltas[idx][2])
                                        > math.hypot(oh_deltas[idx][0], oh_deltas[idx][1], oh_deltas[idx][2]))
                                if not both_lips:
                                    if ch_greater and not ch_should_be_greater:
                                        continue
                                    elif not ch_greater and ch_should_be_greater:
                                        continue
                                if any(string in label for string in ['Upper_Left', 'Lower_Right', 'Upper_Right', 'Lower_Left', 'Mouth_Left', 'Mouth_Right']):
                                    # instead of blending, we take the magnitude of movement * .1 and direct it to the left/right
                                    multiplier = 1
                                    if 'Right' in label:
                                        multiplier = -1
                                    object.data.shape_keys.key_blocks[label].data[idx].co[0] -= (math.hypot(ch_deltas[idx][0], ch_deltas[idx][1], ch_deltas[idx][2]) * 0.75 * multiplier)
                                elif any(string in label for string in ['Inside']):
                                    object.data.shape_keys.key_blocks[label].data[idx].co[1] += (math.hypot(ch_deltas[idx][0], ch_deltas[idx][1], ch_deltas[idx][1]) * 0.75 )
                                elif any(string in label for string in ['Pout']):
                                    object.data.shape_keys.key_blocks[label].data[idx].co[1] -= (math.hypot(ch_deltas[idx][0], ch_deltas[idx][1], ch_deltas[idx][1]) * 0.75 )
                                else:
                                    crossfade_factor = crossfade(vert.co[0], bounding_box[0], bounding_box[1], 0.2)
                                    if 'Left' in label:
                                        crossfade_factor = 1 - crossfade_factor
                                    object.data.shape_keys.key_blocks[label].data[idx].co[0] += (ch_deltas[idx][0] * crossfade_factor)
                                    object.data.shape_keys.key_blocks[label].data[idx].co[1] += (ch_deltas[idx][1] * crossfade_factor)
                                    object.data.shape_keys.key_blocks[label].data[idx].co[2] += (ch_deltas[idx][2] * crossfade_factor)
                        elif generate_smile:
                            object.shape_key_add(name=SRanipal_Labels[x], from_mix=False)
                            smile_deltas, _ = get_shapekey_delta(object, context.scene.ft_smile)

                            for idx, vert in enumerate(object.data.shape_keys.key_blocks[label].data):
                                crossfade_factor = crossfade(vert.co[0], bounding_box[0], bounding_box[1], 0.2)
                                if 'Left' in label:
                                    crossfade_factor = 1 - crossfade_factor
                                object.data.shape_keys.key_blocks[label].data[idx].co[0] += (smile_deltas[idx][0] * crossfade_factor)
                                object.data.shape_keys.key_blocks[label].data[idx].co[1] += (smile_deltas[idx][1] * crossfade_factor)
                                object.data.shape_keys.key_blocks[label].data[idx].co[2] += (smile_deltas[idx][2] * crossfade_factor)
                        elif generate_frown:
                            object.shape_key_add(name=SRanipal_Labels[x], from_mix=False)
                            frown_deltas, _ = get_shapekey_delta(object, context.scene.ft_frown)

                            for idx, vert in enumerate(object.data.shape_keys.key_blocks[label].data):
                                crossfade_factor = crossfade(vert.co[0], bounding_box[0], bounding_box[1], 0.2)
                                if 'Left' in label:
                                    crossfade_factor = 1 - crossfade_factor
                                object.data.shape_keys.key_blocks[label].data[idx].co[0] += (frown_deltas[idx][0] * crossfade_factor)
                                object.data.shape_keys.key_blocks[label].data[idx].co[1] += (frown_deltas[idx][1] * crossfade_factor)
                                object.data.shape_keys.key_blocks[label].data[idx].co[2] += (frown_deltas[idx][2] * crossfade_factor)
                        elif generate_jaw:
                            object.shape_key_add(name=SRanipal_Labels[x], from_mix=False)
                            aa_deltas, _ = get_shapekey_delta(object, context.scene.ft_aa)

                            for idx, vert in enumerate(object.data.shape_keys.key_blocks[label].data):
                                if any(string in label for string in ['Left', 'Right']):
                                    # instead of blending, we take the magnitude of movement * .1 and direct it to the left/right
                                    multiplier = 1
                                    if 'Right' in label:
                                        multiplier = -1
                                    object.data.shape_keys.key_blocks[label].data[idx].co[0] += (math.hypot(aa_deltas[idx][0], aa_deltas[idx][1], aa_deltas[idx][2]) * 0.75 * multiplier)
                                elif any(string in label for string in ['Forward']):
                                    object.data.shape_keys.key_blocks[label].data[idx].co[1] -= (math.hypot(aa_deltas[idx][0], aa_deltas[idx][1], aa_deltas[idx][2]) * 0.5 )
                                else:
                                    object.data.shape_keys.key_blocks[label].data[idx].co[0] += aa_deltas[idx][0] * 2.0
                                    object.data.shape_keys.key_blocks[label].data[idx].co[1] += aa_deltas[idx][1] * 2.0
                                    object.data.shape_keys.key_blocks[label].data[idx].co[2] += aa_deltas[idx][2] * 2.0
                        else:
                            # Find shapekey enterred and mix to create new shapekey
                            object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(curr_key)
                            object.data.shape_keys.key_blocks[curr_key].value = 1
                            object.shape_key_add(name=SRanipal_Labels[x], from_mix=True)
                    else:
                        #Mix to existing shape key duplicate
                        object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(SRanipal_Labels[x])
                        object.data.shape_keys.key_blocks[curr_key].value = 1
                        ops.object.mode_set(mode='EDIT', toggle=False)
                        bpy.ops.mesh.select_mode(type="VERT")
                        ops.mesh.select_all(action='SELECT')
                        ops.mesh.blend_from_shape(shape=curr_key, blend=1.0, add=False)
                        self.report({'INFO'}, "Existing SRanipal face tracking shape key: " + SRanipal_Labels[x] + " has been overwritten with: " + curr_key)
                    #Clear shape key weights
                    ops.object.shape_key_clear()

            self.report({'INFO'}, "SRanipal face tracking shapekeys have been created on mesh")


            #Cleanup mode state
            ops.object.mode_set(mode='OBJECT', toggle=False)

            #Move active shape to 'Basis'
            active_object.active_shape_key_index = 0

        else:
            #Error message if basis does not exist
            self.report({'WARNING'}, "No shape keys found on mesh")
        return{'FINISHED'}

class FT_OT_CreateVisemes(Operator):
    """Creates Face Tracking Visemes"""
    bl_label = "Create Remapped Face Tracking Visemes"
    bl_idname = "ft.create_visemes"

    def execute(self, context):

        object = bpy.context.object
        scene = context.scene
        ft_mesh = scene.ft_mesh
        active_object = bpy.context.active_object
        mesh = bpy.ops.mesh
        ops = bpy.ops

        #Set the selected mesh to active object
        mesh = get_objects()[ft_mesh]
        self.report({'INFO'}, "Selected mesh is: " + str(ft_mesh))
        set_active(mesh)


        #Check if there is shape keys on the mesh
        if object.data.shape_keys:

            #Create beginning seperation marker for Viseme Shape Keys
            if duplicate_shapekey("~~ Face Tracking Visemes ~~") == False :
                object.shape_key_add(name="~~ Face Tracking Visemes ~~", from_mix=False)

            #Clear all existing values for shape keys
            ops.object.shape_key_clear()

            for x in range(len(FT_Visemes)):
                curr_key = eval("scene.ft_viseme_" + str(x))
                #Check if blend with 'Basis' shape key
                if curr_key == "Basis":
                    #Check for duplicates
                    if duplicate_shapekey(FT_Visemes[x]) == False :
                        object.shape_key_add(name=FT_Visemes[x], from_mix=False)
                    #Do not overwrite if the shape key exists and is on 'Basis'

                else:
                    #Check for duplicates
                    if duplicate_shapekey(FT_Visemes[x]) == False :
                        # Find shapekey enterred and mix to create new shapekey
                        object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(curr_key)
                        object.data.shape_keys.key_blocks[curr_key].value = eval('scene.ft_viseme_int_' + str(x))
                        object.shape_key_add(name=FT_Visemes[x], from_mix=True)
                    else:
                        #Mix to existing shape key duplicate
                        object.active_shape_key_index = active_object.data.shape_keys.key_blocks.find(FT_Visemes[x])
                        object.data.shape_keys.key_blocks[curr_key].value = eval('scene.ft_viseme_int_' + str(x))
                        ops.object.mode_set(mode='EDIT', toggle=False)
                        bpy.ops.mesh.select_mode(type="VERT")
                        ops.mesh.select_all(action='SELECT')
                        ops.mesh.blend_from_shape(shape=curr_key, blend=1, add=False)
                        self.report({'INFO'}, "Existing SRanipal Viseme shape key: " + FT_Visemes[x] + " has been overwritten with: " + curr_key)
                    #Clear shape key weights
                    ops.object.shape_key_clear()

            self.report({'INFO'}, "SRanipal face tracking shapekeys have been created on mesh")


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

class FT_Shapes_UL(Panel):
    bl_label = "SRanipal Shape Key Remapping"
    bl_idname = "FT Shapes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FT MAPPING"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ft_mesh = scene.ft_mesh
        object = bpy.context.object

        #Start Layout
        col = layout.column()

        #Mesh Selection
        mesh = get_objects()[ft_mesh]
        mesh_count = len(get_meshes_objects(check=False, mode=2))
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(context.scene, 'ft_mesh', icon='MESH_DATA')
        col.separator()
        row = col.row(align=True)

        #Viseme Selection
        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="Create from Visemes:", icon='SHADERFX')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, 'ft_aa', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, 'ft_ch', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, 'ft_oh', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, 'ft_blink', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, 'ft_smile', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, 'ft_frown', icon='SHAPEKEY_DATA')

        #Check mesh selections
        if ft_mesh and has_shapekeys(mesh):
            #Info

            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Select shape keys to create FT shape keys.', icon='INFO')
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Specifying above will attempt to create them for you.', icon='INFO')
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Currently requires rotation to be applied.', icon='INFO')
            col.separator()

            #Start Box
            box = layout.box()
            col = box.column(align=True)

            #Start List of Shapekeys from VRCFT labels list
            for i in range(len(SRanipal_Labels)):
                row = col.row(align=True)
                row.scale_y = 1.1
                row.label(text = SRanipal_Labels[i] + ":")
                row.prop(scene, 'ft_shapekey_' + str(i), icon='SHAPEKEY_DATA')
                row.prop(scene, 'ft_shapekey_enable_' + str(i), icon='CHECKMARK')
                # Determine whether this key is already going to be auto-populated
                label = SRanipal_Labels[i]
                basis = get_shapekeys_ft(self, context)[0][0]
                if any(string in label for string in ['Blink', 'squeeze', 'Wide']):
                    if context.scene.ft_blink != basis:
                        row.enabled = False
                if any(string in label for string in ['Jaw']):
                    if context.scene.ft_aa != basis:
                        row.enabled = False
                if any(string in label for string in ['Upper_Up', 'Lower_Down', 'Upper_Left', 'Lower_Right', 'Upper_Right', 'Lower_Left', 'Inside', 'Pout', 'Mouth_Left', 'Mouth_Right', 'Smile', 'Sad']):
                    if (context.scene.ft_ch != basis and
                        context.scene.ft_oh != basis):
                        row.enabled = False
                if any(string in label for string in ['Smile']):
                    if context.scene.ft_smile != basis:
                        row.enabled = False
                if any(string in label for string in ['Sad']):
                    if context.scene.ft_frown != basis:
                        row.enabled = False

            row = layout.row()
            row.operator("ft.create_shapekeys", icon='MESH_MONKEY')
        else:
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Select the mesh with face shape keys.', icon='INFO')
            col.separator()

class FT_Visemes_UL(Panel):
    bl_label = "Face Tracking Viseme Remapping"
    bl_idname = "FT Viseme"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FT MAPPING"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ft_mesh = scene.ft_mesh
        object = bpy.context.object

        #Start Layout
        col = layout.column()

        #Mesh Selection
        mesh = get_objects()[ft_mesh]
        mesh_count = len(get_meshes_objects(check=False, mode=2))
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(context.scene, 'ft_mesh', icon='MESH_DATA')
        col.separator()
        row = col.row(align=True)

        #Check mesh selections
        if ft_mesh and has_shapekeys(mesh):

            #Info
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Select shape keys to create visemes.', icon='INFO')
            col.separator()

            #Start Box
            box = layout.box()
            col = box.column(align=True)

            #Start List of Shapekeys from VRCFT labels list
            for i in range(len(FT_Visemes)):
                row = col.row(align=True)
                row.scale_y = 1.1
                row.label(text = FT_Visemes[i] + ":")
                row.prop(scene, 'ft_viseme_' + str(i), icon='SHAPEKEY_DATA')
                row.prop(scene, 'ft_viseme_int_' + str(i))
            row = layout.row()
            row.operator("ft.create_visemes", icon='MESH_MONKEY')
        else:
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text='Select the mesh with face shape keys.', icon='INFO')
            col.separator()

class FT_VersionInfo_UL(Panel):
    bl_label = "Info"
    bl_idname = "FT Info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FT MAPPING"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        #Start Layout
        col = layout.column()

        #Version Info
        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text=bl_info['name'] + ' v' + (".".join(str(n) for n in bl_info['version'])), icon="HEART")
        col.separator()

        #Credits
        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="Created by " + bl_info['author'], icon="SOLO_ON")
        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="Create from Visemes by Feilen", icon="SHADERFX")
        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="With help from bernaclejames", icon="CHECKMARK")
        col.separator()

# -------------------------------------------------------------------
# Register
# -------------------------------------------------------------------

classes = (
    FT_OT_CreateShapeKeys,
    FT_OT_CreateVisemes,
    FT_Shapes_UL,
    FT_Visemes_UL,
    FT_VersionInfo_UL
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Mesh Select
    Scene.ft_mesh = EnumProperty(name='Mesh',description='Mesh to apply FT shape keys',items=get_meshes)

    # Viseme select
    Scene.ft_aa = EnumProperty(name='aa/Jaw Down',description='This shapekey should ideally only move the mouth down.',items=get_shapekeys_ft)
    Scene.ft_ch = EnumProperty(name='ch/Cheese',description='This shapekey should ideally only move the lips to expose the teeth.',items=get_shapekeys_ft)
    Scene.ft_oh = EnumProperty(name='oh/Shock/aa/Jaw Down',description='This shapekey should move the bottom lips more than CH but not the top lips, and may need to be created. Often AA works too.',items=get_shapekeys_ft)
    Scene.ft_blink = EnumProperty(name='blink',description='Select shapekey to use for FT',items=get_shapekeys_ft)
    Scene.ft_smile = EnumProperty(name='smile',description='Select shapekey to use for FT',items=get_shapekeys_ft)
    Scene.ft_frown = EnumProperty(name='frown',description='Select shapekey to use for FT',items=get_shapekeys_ft)

    # Shape Keys
    for i, ft_shape in enumerate(SRanipal_Labels):
        setattr(Scene, "ft_shapekey_" + str(i), EnumProperty(
            name='',
            description='Select shapekey to use for SRanipal',
            items=get_shapekeys_ft)
        )
    # Enable Shape Key Creation
    for i, ft_shape in enumerate(SRanipal_Labels):
        setattr(Scene, "ft_shapekey_enable_" + str(i), BoolProperty(
            name='',
            description='Enable SRanipal Shapekey Creation',
            default=True)
        )
    # Visemes
    for i, ft_viseme in enumerate(FT_Visemes):
        setattr(Scene, "ft_viseme_" + str(i), EnumProperty(
            name='',
            description='Select existing viseme',
            items=get_shapekeys_ft)
        )
    # Viseme Intensity
    for i, ft_viseme in enumerate(FT_Visemes):
        setattr(Scene, "ft_viseme_int_" + str(i), FloatProperty(
            name = "",
            description = "Visemes intensity reduction with face tracking shapekey controls",
            default = 0.5,
            min = 0.0,
            max = 1.0
            )
        )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for i, ft_shape in enumerate(SRanipal_Labels):
        delattr(Scene, "ft_shapekey_" + str(i))

    for i, ft_shape in enumerate(SRanipal_Lables):
        delattr(Scene, "ft_shapekey_enable_" + str(i))

    for i, ft_viseme in enumerate(FT_Visemes):
        delattr(Scene, "ft_viseme_" + str(i))

    for i, ft_viseme in enumerate(FT_Visemes):
        delattr(Scene, "ft_viseme_int" + str(i))

if __name__ == "__main__":
    register()
