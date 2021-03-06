import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBeginForEachComponentLoop(Node, ScNode):
    bl_idname = "ScBeginForEachComponentLoop"
    bl_label = "Begin For-Each Component Loop"

    prop_locked: BoolProperty()
    prop_components: StringProperty()
    in_type: EnumProperty(items=[('VERT', 'Vertices', ''), ('EDGE', 'Edges', ''), ('FACE', 'Faces', '')], default='FACE', update=ScNode.update_value)
    out_index: IntProperty()

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "In")
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.outputs.new("ScNodeSocketInfo", "End For-Each Component Loop")
        self.outputs.new("ScNodeSocketObject", "Out")
        self.outputs.new("ScNodeSocketNumber", "Index")
    
    def execute(self, forced=False):
        if (self.prop_locked):
            self.outputs["Index"].default_value = self.out_index
            self.set_color()
            return True
        else:
            self.prop_locked = True
            self.out_index = 0
            return super().execute(forced)
    
    def pre_execute(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        if (self.inputs["Type"].default_value == 'VERT'):
            self.prop_components = repr([i.index for i in self.inputs["In"].default_value.data.vertices if i.select])
        elif (self.inputs["Type"].default_value == 'EDGE'):
            self.prop_components = repr([i.index for i in self.inputs["In"].default_value.data.edges if i.select])
        elif (self.inputs["Type"].default_value == 'FACE'):
            self.prop_components = repr([i.index for i in self.inputs["In"].default_value.data.polygons if i.select])
        bpy.ops.object.mode_set(mode="EDIT")
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        out["Index"] = self.out_index
        return out