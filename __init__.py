# Used code from https://blender.stackexchange.com/questions/272501/how-to-insert-keyframe-data-with-python
import json

import bpy
from bpy.types import Object, Operator, Panel
from bpy.utils import register_class, unregister_class
from mathutils import Vector
import math

bl_info = {
    'name': 'Animation creator',
    'author': 'Evgeny Podjachev',
    "version": (1, 0, 0),
    'blender': (3, 5, 0),
    'description': 'Encodes particle color in Rand value',
    'warning': '',
    'doc_url': "",
}

def create_animation_data(target, name):
    if target.animation_data == None:
        target.animation_data_create()
        target.animation_data.action = bpy.data.actions.new(name=name)    
    
def create_fcurve(target, data_path, id):
     fcurve = target.animation_data.action.fcurves.find(data_path=data_path, index=id)
    
     if fcurve == None:
          fcurve = target.animation_data.action.fcurves.new(data_path=data_path, index=id)
        
     return fcurve

class AnimationCreator(Panel):
    bl_label = "Object Properties"
    bl_idname = "OBJECT_PT_animation_creator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ACreator"

    @classmethod
    def poll(cls, context):    
        return True

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(ACREATOR_PT_Apply_animation.bl_idname)

class ACREATOR_PT_Apply_animation(Operator):
    bl_idname = "acreator.apply_animation" 
    bl_label = "Apply animation"
    bl_description = "Apply animation"

    def execute(self, context):
        with open(bpy.data.filepath + '.json', 'rt') as f:
            data = json.load(f)
        
        for d in data:
            frame = d['frame']
            objs = d['objects']
            for name, keys in objs.items():
                obj = context.scene.objects.get(name, None)
                if not obj:
                    continue

                create_animation_data(obj, 'moving_data')
                fcu_x = create_fcurve(obj, 'location', 1)
                fcu_y = create_fcurve(obj, 'location', 2)

                #insert the keyframe
                key_x = fcu_x.keyframe_points.insert(frame=frame,value=keys[0])
                key_y = fcu_y.keyframe_points.insert(frame=frame,value=keys[1])
    
                #set interpolation and easing
                #key.interpolation = interpolation
                #key.easing = easing
            pass

        return {'FINISHED'}

classes = (
    AnimationCreator,
    ACREATOR_PT_Apply_animation,
)

def find_object():
    pass

def register():
    for cls in classes:
        register_class(cls)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()