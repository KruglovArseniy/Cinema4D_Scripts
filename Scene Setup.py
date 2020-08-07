import c4d
from c4d import gui

default_path = "D:\\Google Drive\\3D\\!Content\\HDRI"
paths = {
    "StemCell" : default_path + "\\Studio\\StemCell.exr",
    "Tomoco Studio" : default_path + "\\Interior\\Tomoco Studio.exr",
    "Artist Workshop 4K" : default_path + "\\Interior\\Artist Workshop\\Artist Workshop 4K.hdr"}

#Dialog window
class DialogWindow(gui.GeDialog):

    def CreateLayout(self):
        self.SetTitle("Scene Setup")    #Window Title

        self.AddCheckbox(10, c4d.BFH_LEFT, 0, 0, " Sky")    #Sky Checkbox

        #Texture Path
        self.GroupBegin(0, c4d.BFH_SCALEFIT, cols = 3)
        self.AddStaticText(0, c4d.BFH_LEFT, name = "Path")
        self.AddEditText(11, c4d.BFH_SCALEFIT, initw = 350)
        self.AddButton(12, c4d.BFH_LEFT, initw = 6, name = "...")
        self.GroupEnd()

        #Presets
        self.GroupBegin(0, c4d.BFH_LEFT)
        self.AddRadioGroup(13, 3, 1, c4d.BFH_LEFT)
        for i in range (len(paths)):
            self.AddChild(13, i + 17, paths.keys()[i])
        self.AddChild(13, 14, "Custom")
        self.GroupEnd()
        
        self.AddCheckbox(15, c4d.BFH_LEFT, 0, 0, " Seen by Camera")    #Visibility Checkbox

        self.AddSeparatorH(c4d.BFH_FIT)

        self.AddCheckbox(20, c4d.BFH_LEFT, 0, 0, " Background")    #Background Checkbox
        self.AddColorChooser(21, c4d.BFH_SCALEFIT, layoutflags = c4d.DR_COLORFIELD_NO_MIXER)    #Color Chooser

        self.AddButton(1, c4d.BFH_RIGHT, name = "Apply")    #Apply

        return True

    def InitValues(self):
        self.SetBool(10, True)    #Sky Checkbox
        self.SetString(11, default_path)    #Path
        self.SetBool(14, True)    #Radio Button
        
        self.SetBool(20, True)    #Background Checkbox
        self.SetColorField(id = 21, color = c4d.Vector(247/255.), brightness = 1, maxbrightness = 1, flags = 0)    #Color Field

        return True

    def Command(self, id, msg):
        #Image Picker
        if (id == 12):
          path = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_IMAGES, "HDRI", c4d.FILESELECT_LOAD, def_path = self.GetString(1))

          if (path != None):
            self.SetString(11, path)

            for i in range (len(paths)):
                self.SetBool(i + 17, False)

            self.SetBool(14, True)

        if (id == 13):
            for i in range (len(paths)):
                if (self.GetBool(i + 17) == True):
                    self.SetString(11, paths.values()[i])

        if (id == 1):
            doc.StartUndo()

            #Sky
            if (self.GetBool(10) == True):
                sky = c4d.BaseObject(c4d.Osky)
                doc.InsertObject(sky)
                doc.AddUndo(c4d.UNDOTYPE_NEW, sky)

                #Material
                material = c4d.Material(c4d.Mbase)
                material.SetName('Sky')
                doc.InsertMaterial(material)
                doc.AddUndo(c4d.UNDOTYPE_NEW, material)
                material[c4d.MATERIAL_USE_REFLECTION] = 0
                material[c4d.MATERIAL_USE_COLOR] = 0
                material[c4d.MATERIAL_USE_LUMINANCE] = 1

                #Luminance Shader
                luminance_shader = c4d.BaseList2D (c4d.Xbitmap)
                luminance_shader[c4d.BITMAPSHADER_FILENAME] = self.GetString(11)
                material.InsertShader(luminance_shader)
                material[c4d.MATERIAL_LUMINANCE_SHADER] = luminance_shader

                #Tag
                tag = sky.MakeTag(c4d.Ttexture)
                tag[c4d.TEXTURETAG_PROJECTION] = 0
                tag.SetMaterial(material)
                
                #Visibility
                if (self.GetBool(15) == False):
                    tag = sky.MakeTag(c4d.Tcompositing)
                    tag[c4d.COMPOSITINGTAG_SEENBYCAMERA] = 0

            #Background
            if (self.GetBool(20) == True):
                #Background
                background = c4d.BaseObject(c4d.Obackground)
                doc.InsertObject(background)
                doc.AddUndo(c4d.UNDOTYPE_NEW, background)
    
                #Material
                material = c4d.Material(c4d.Mbase)
                material.SetName('Background')
                doc.InsertMaterial(material)
                doc.AddUndo(c4d.UNDOTYPE_NEW, material)
                material[c4d.MATERIAL_USE_REFLECTION] = 0
                material[c4d.MATERIAL_COLOR_COLOR] = self.GetColorField(21).values()[0]
    
                #Tag
                tag = background.MakeTag(c4d.Ttexture)
                tag[c4d.TEXTURETAG_PROJECTION] = 6
                tag.SetMaterial(material)


            doc.EndUndo()
            c4d.EventAdd()
            self.Close()

        return True

#Open Dialog
dialog_window = DialogWindow()
dialog_window.Open(c4d.DLG_TYPE_MODAL, xpos = -2, ypos = -2)