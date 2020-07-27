import c4d
from c4d import gui

def DefaultMaterial(material_name, texture_path, material_type):

    #Material
    material = c4d.Material(c4d.Mbase)

    if (material_type == 0):
        material.SetName(material_name + "_Dielectric_Material")

    if (material_type == 1):
        material.SetName(material_name + "_Conductor_Material")

    if (material_type == 2):
        material.SetName(material_name + "_Transparent_Material")

    doc.InsertMaterial(material)
    doc.AddUndo(c4d.UNDOTYPE_NEW, material)

    #Local Texture Path
    if (texture_path == doc.GetDocumentPath()):
        texture_path = ''
    else:
        texture_path = texture_path + '\\'

    #Diffuse
    material[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(1)
    diffuse_shader = c4d.BaseList2D (c4d.Xbitmap)
    diffuse_shader[c4d.BITMAPSHADER_FILENAME] = texture_path + material_name + '_Diffuse.png'
    diffuse_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
    diffuse_shader [c4d.BITMAPSHADER_COLORPROFILE] = 2
    material.InsertShader(diffuse_shader)
    material[c4d.MATERIAL_COLOR_SHADER] = diffuse_shader

    #Normal
    material[c4d.MATERIAL_USE_NORMAL] = 1
    material[c4d.MATERIAL_NORMAL_REVERSEY] = 1
    normal_shader = c4d.BaseList2D (c4d.Xbitmap)
    normal_shader [c4d.BITMAPSHADER_FILENAME] = texture_path + material_name + '_Normal.png'
    normal_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
    normal_shader [c4d.BITMAPSHADER_COLORPROFILE] = 1
    material.InsertShader(normal_shader)
    material[c4d.MATERIAL_NORMAL_SHADER] = normal_shader

    #Glossiness & Specular
    material.RemoveReflectionLayerIndex(0)

    #Reflection Layer
    material.AddReflectionLayer()
    reflection_layer = material.GetReflectionLayerIndex(0).GetDataID()

    #Reflection Settings
    material[c4d.REFLECTION_LAYER_MAIN_DISTRIBUTION + reflection_layer] = 3
    material[c4d.REFLECTION_LAYER_MAIN_ADDITIVE + reflection_layer] = 2
    material[c4d.REFLECTION_LAYER_MAIN_VALUE_SPECULAR + reflection_layer] = 0
    material[c4d.REFLECTION_LAYER_MAIN_VALUE_ROUGHNESS + reflection_layer] = 1

    #Specular Shader
    specular_shader = c4d.BaseList2D (c4d.Xbitmap)
    specular_shader [c4d.BITMAPSHADER_FILENAME] = texture_path + material_name + '_Specular.png'
    specular_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
    specular_shader [c4d.BITMAPSHADER_COLORPROFILE] = 2
    material.InsertShader (specular_shader)
    material[c4d.REFLECTION_LAYER_COLOR_TEXTURE + reflection_layer] = specular_shader

    #Roughness Shader
    roughness_shader = c4d.BaseList2D (c4d.Xbitmap)
    roughness_shader [c4d.BITMAPSHADER_FILENAME] = texture_path + material_name + '_Glossiness.png'
    roughness_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
    roughness_shader [c4d.BITMAPSHADER_COLORPROFILE] = 1
    roughness_shader [c4d.BITMAPSHADER_BLACKPOINT] = 1
    roughness_shader [c4d.BITMAPSHADER_WHITEPOINT] = 0
    material.InsertShader (roughness_shader)
    material[c4d.REFLECTION_LAYER_MAIN_SHADER_ROUGHNESS + reflection_layer] = roughness_shader
    
    #Alpha
    if (material_type == 1):
        material[c4d.MATERIAL_USE_ALPHA] = 1
        alpha_shader = c4d.BaseList2D (c4d.Xbitmap)
        alpha_shader [c4d.BITMAPSHADER_FILENAME] = texture_path + material_name + '_Metallic.png'
        alpha_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
        alpha_shader [c4d.BITMAPSHADER_COLORPROFILE] = 2
        material[c4d.MATERIAL_ALPHA_SHADER] = alpha_shader
        material.InsertShader (alpha_shader)

    return material

def DielectricIOR(material, ior):

    #IOR
    reflection_layer = material.GetReflectionLayerIndex(0).GetDataID()

    material[c4d.REFLECTION_LAYER_FRESNEL_MODE + reflection_layer] = 1
    material[c4d.REFLECTION_LAYER_FRESNEL_VALUE_IOR + reflection_layer] = ior

    return material

def ConductorIOR(material, ior):

    #IOR
    reflection_layer = material.GetReflectionLayerIndex(0).GetDataID()

    material[c4d.REFLECTION_LAYER_FRESNEL_MODE + reflection_layer] = 2
    material[c4d.REFLECTION_LAYER_FRESNEL_VALUE_ETA + reflection_layer] = ior

    return material

def Transparency(material, material_name, texture_path, refraction):

    #Local Texture Path
    if (texture_path == doc.GetDocumentPath()):
        texture_path = ''
    else:
        texture_path = texture_path + '\\'

    #Transparency
    material[c4d.MATERIAL_USE_TRANSPARENCY] = 1
    material[c4d.MATERIAL_TRANSPARENCY_REFRACTION] = refraction

    #Transparency Shader
    transparency_shader = c4d.BaseList2D (c4d.Xbitmap)
    transparency_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
    transparency_shader [c4d.BITMAPSHADER_COLORPROFILE] = 1
    material.InsertShader (transparency_shader)

    #Reflection Layer
    material.RemoveReflectionLayerIndex(0)
    reflection_layer = material.GetReflectionLayerTrans().GetDataID()

    #Reflection Settings
    material[c4d.REFLECTION_LAYER_MAIN_DISTRIBUTION + reflection_layer] = 3
    material[c4d.REFLECTION_LAYER_MAIN_ADDITIVE + reflection_layer] = 2
    material[c4d.REFLECTION_LAYER_MAIN_VALUE_SPECULAR + reflection_layer] = 0
    material[c4d.REFLECTION_LAYER_MAIN_VALUE_ROUGHNESS + reflection_layer] = 1

    #Roughness Shader
    roughness_shader = c4d.BaseList2D (c4d.Xbitmap)
    roughness_shader [c4d.BITMAPSHADER_FILENAME] = texture_path + material_name + '_Glossiness.png'
    roughness_shader [c4d.BITMAPSHADER_INTERPOLATION] = 0
    roughness_shader [c4d.BITMAPSHADER_COLORPROFILE] = 1
    roughness_shader [c4d.BITMAPSHADER_BLACKPOINT] = 1
    roughness_shader [c4d.BITMAPSHADER_WHITEPOINT] = 0
    material.InsertShader (roughness_shader)
    material[c4d.REFLECTION_LAYER_MAIN_SHADER_ROUGHNESS + reflection_layer] = roughness_shader

    return material

def AddTag(material):

    tag = doc.GetActiveObject().MakeTag(c4d.Ttexture)
    doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
    tag[c4d.TEXTURETAG_PROJECTION] = 6
    tag.SetMaterial(material)

def EdtTextureSetName(bool01, bool02, bool03):

        object_name = doc.GetActiveObject().GetName()

        if (bool02 == True):
            object_name = object_name.title()

        if (bool03 == True):
            object_name = object_name.replace(' ', '_')

        if (bool01 == True):
            object_name = object_name.replace(' ', '')

        return object_name

#Dialog window
class DialogWindow(gui.GeDialog):

    #Layout
    def CreateLayout(self):

        #Window Title
        self.SetTitle("StemCell Material")

        #Texture Set Name
        self.GroupBegin(0, c4d.BFH_LEFT, cols = 2)
        self.AddStaticText(0, c4d.BFH_LEFT, name = "Texture Set Name")
        self.AddEditText(1, c4d.BFH_LEFT, initw = 360)
        self.GroupEnd()

        #Edt Texture Set Name
        self.AddCheckbox(20, c4d.BFH_LEFT, 0, 0, name = " Remove Spaces")
        self.AddCheckbox(21, c4d.BFH_LEFT, 0, 0, name = " Title")
        self.AddCheckbox(22, c4d.BFH_LEFT, 0, 0, name = " Spaces to Underscores")

        self.AddSeparatorH(c4d.BFH_FIT)

        #Texture Path
        self.GroupBegin(0, c4d.BFH_LEFT, cols = 3)
        self.AddStaticText(0, c4d.BFH_LEFT, name = "Texture Path")
        self.AddEditText(2, c4d.BFH_LEFT, initw = 350)
        self.AddButton(3, c4d.BFH_LEFT, initw = 6, name = "...")
        self.GroupEnd()

        self.AddSeparatorH(c4d.BFH_FIT)

        #Dielectric
        self.AddCheckbox(4, c4d.BFH_LEFT, 0, 0, name = " Dielectric")
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols = 2)
        self.AddCheckbox(5, c4d.BFH_LEFT, 0, 0, name = " IOR")
        self.AddEditSlider(6, c4d.BFH_SCALEFIT)
        self.GroupEnd()
        self.AddSeparatorH(c4d.BFH_FIT)

        #Conductor
        self.AddCheckbox(7, c4d.BFH_LEFT, 0, 0, " Conductor")
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols = 2)
        self.AddCheckbox(8, c4d.BFH_LEFT, 0, 0, name = " IOR")
        self.AddEditSlider(9, c4d.BFH_SCALEFIT, 0, 0)
        self.GroupEnd()
        self.AddSeparatorH(c4d.BFH_FIT)

        #Transparent
        self.AddCheckbox(10, c4d.BFH_LEFT, 0, 0, " Transparent")
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols = 2)
        self.AddStaticText(0, c4d.BFH_LEFT, 0, 0, "Refraction", 0)
        self.AddEditSlider(11, c4d.BFH_SCALEFIT, 0, 0)
        self.GroupEnd()

        self.AddSeparatorH(c4d.BFH_FIT)

        #Apply
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols = 2)
        self.AddCheckbox(23, c4d.BFH_SCALEFIT, 0, 0, " Apply Material to Object")
        self.AddButton(12, c4d.BFH_RIGHT, name = "Apply")
        self.GroupEnd()

        return True

    #Default values
    def InitValues(self):

        #Texture Set Name
        if doc.GetActiveObject() != None:
            self.SetString(1, EdtTextureSetName(True, True, False))

        #Checkboxes
        self.SetBool(20, True)
        self.SetBool(21, True)
        self.SetBool(23, True)

        #Texture Path
        self.SetString(2, doc.GetDocumentPath())

        #"Dielectric" Checkbox
        self.SetBool(4, True)

        #Sliders
        self.SetFloat(6, 8, min = 1, max = 10, max2 = 25, step = 0.01)    #Dielectric
        self.SetFloat(9, 8, min = 1, max = 10, max2 = 25, step = 0.01)    #Conductor
        self.SetFloat(11, 1.517, min = 0.25, max = 4, step = 0.001)       #Transparent

        return True

    def Command(self, id, msg):

        #Edt Texture Set Name
        if (id == 20) or (id == 21) or (id == 22):
            self.SetString(1, EdtTextureSetName(self.GetBool(20), self.GetBool(21), self.GetBool(22)))

        #Texture Path Input
        if (id == 3):
            texture_path = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_IMAGES, "Texture Path", c4d.FILESELECT_DIRECTORY, def_path = doc.GetDocumentPath())
            self.SetString(2, texture_path)

        #Apply
        if (id == 12):
            #Conductor Material
            if (self.GetBool(7) == True):
                conductor_material = DefaultMaterial(self.GetString(1), self.GetString(2), 1)
                if (self.GetBool(8) == True):
                    ConductorIOR(conductor_material, self.GetFloat(9))
                if (self.GetBool(23) == True) and (doc.GetActiveObject() != None):
                    AddTag(conductor_material)
            
            #Dielectric Material
            if (self.GetBool(4) == True):
                dielectric_material = DefaultMaterial(self.GetString(1), self.GetString(2), 0)
                if (self.GetBool(5) == True):
                    DielectricIOR(dielectric_material, self.GetFloat(6))
                if (self.GetBool(23) == True) and (doc.GetActiveObject() != None):
                    AddTag(dielectric_material)

            #Transparent Material
            if (self.GetBool(10) == True):
                transparent_material = DefaultMaterial(self.GetString(1), self.GetString(2), 2)
                Transparency(transparent_material, self.GetString(1), self.GetString(2), self.GetFloat(11))

            c4d.EventAdd()
            self.Close()

        return True

#Open Dialog
dialog_window = DialogWindow()
dialog_window.Open(c4d.DLG_TYPE_MODAL, xpos = -2, ypos = -2)
