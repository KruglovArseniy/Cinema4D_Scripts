import c4d
from c4d import gui

#Dialog window
class DialogWindow(gui.GeDialog):

    def CreateLayout(self):
        #Window Title
        self.SetTitle("Background")
        
        #Color Chooser
        self.AddColorChooser(1, c4d.BFH_SCALEFIT, layoutflags = c4d.DR_COLORFIELD_NO_MIXER)
        
        #Apply
        self.AddButton(2, c4d.BFH_RIGHT, name = "Apply")
        
        return True
        
    def InitValues(self):
        self.SetColorField(id = 1, color = c4d.Vector(247/255.), brightness = 1, maxbrightness = 1, flags = 0)
        
        return True
        
    def Command(self, id, msg):
        if (id == 2):
            doc.StartUndo()
    
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
            material[c4d.MATERIAL_COLOR_COLOR] = self.GetColorField(1).values()[0]
            
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