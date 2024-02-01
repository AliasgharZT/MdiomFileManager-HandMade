from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.anchorlayout import MDAnchorLayout 
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidgetWithoutTouch
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty
import os
import time  
import psutil
from kivymd.toast import toast 
# --------------Builder------------------------
Builder.load_file('style.kv')
# ------------------STYLE & Calculator------------------------
class FileManagerZ(MDScrollView): 
    register=ObjectProperty()
    global_ld=[]
    global_address=''
    t_address={'address':''}
    t_ld={'disk':[]} 
    def __init__(self,*args,**kwargs):
        super(FileManagerZ,self).__init__(*args,**kwargs)
    
    def find_disks(self):
        partitions=psutil.disk_partitions()
        for partition in partitions:
            self.global_ld.append(partition[0])
        self.t_ld['disk']=self.global_ld
    def create_disks(self):
        try:
            self.register.clear_widgets()
            self.find_disks()
            for ld in self.global_ld:
                name=ld 
                address=ld 
                list_file=os.listdir(address)
                items=str(len(list_file))
                td=os.path.getmtime(address)
                td=time.ctime(td)
                date=td
                t=ThreeLineIconListItem(
                    IconLeftWidgetWithoutTouch(icon='folder-home'),
                    text=name,
                    secondary_text=items,
                    tertiary_text=date,
                    on_press=self.goto_address  
                    )
                self.register.add_widget(t)
                # self.goto_items(list_file,address)
                # l.append(t)
                # print(list_file)
        except:pass
    
    def goto_address(self,instace):
        # print(instace.text)
        # print(self.global_ld)
        self.global_address=instace.text 
        self.t_address['address']+=instace.text 
        # print(self.global_address)
        self.register.clear_widgets()
        lf=os.listdir(self.global_address)
        # print(lf,'\n==================') 
        self.goto_items(lf,self.global_address)
    
    def goto_items(self,list_file,address):
        try:
            # print(address) 
            app=MDApp.get_running_app()
            tb=app.root.ids.tb 
            tb.title=address 
            for file_name in list_file:
                if file_name[-3]=='.' or file_name[-4]=='.' or file_name[-5]=='.':
                    at=address
                    at+=file_name
                    tt=os.path.getmtime(at)
                    tt=time.ctime(tt)
                    s=os.path.getsize(at)
                    z=self.return_size(s)
                    self.register.add_widget(ThreeLineIconListItem(
                        IconLeftWidgetWithoutTouch(icon='file'),
                        text=file_name,
                        secondary_text=str(z[0])+z[1],
                        tertiary_text=tt, 
                        on_press=self.run_file,
                    ))
                else:
                    at=address
                    at+=file_name
                    # print(at) 
                    lt=os.listdir(at)
                    tt=os.path.getmtime(at)
                    tt=time.ctime(tt)
                    self.register.add_widget(ThreeLineIconListItem(
                        IconLeftWidgetWithoutTouch(icon='folder'),
                        text=file_name,
                        secondary_text=str(len(lt)),
                        tertiary_text=tt,
                        on_press=self.goto_address_file
                    ))
        except:pass
    def run_file(self,instance):
        try:
            address=self.global_address
            address+=instance.text 
            os.system(fr'{address}')
        except:
            None
    def goto_address_file(self,instace):
        # print(instace.text)
        # print(self.global_ld)
        self.global_address+=instace.text+'\\'
        self.t_address['address']+=instace.text +'\\'
        # print(self.global_address)
        self.register.clear_widgets()
        lf=os.listdir(self.global_address)
        # print(lf,'\n==================') 
        self.goto_items(lf,self.global_address)
    def return_size(self,size):
        s=size
        if len(str(s))<=3:
            return([s,'B'])
        elif len(str(s))<=6:
            s=float(s/1024)
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'KB'])
        elif len(str(s))<=9:
            s=float(s/(1024*1024))
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'MB'])
        elif len(str(s))<=12:
            s=float(s/(1024*1024*1024))
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'GB'])
        elif len(str(s))<=15:
            s=float(s/(1024*1024*1024*1024))
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'TB'])
        else:pass       
# -------------------------------------------------
class Style(MDAnchorLayout): 
    mn=ObjectProperty() 
    tb=ObjectProperty() 
    t=True
    def __init__(self,*args,**kwargs):
        super(Style,self).__init__(*args,**kwargs) 
        self.fmz=FileManagerZ()
    
    def back_file(self): 
        if self.t==True:
            self.ad=self.fmz.t_address['address']
            # self.t=False
        # print(self.ad) 
        # print(self.fmz.t_address) 
        if self.ad=='':pass 
        else:
            self.t=False
            if len(self.ad)==3:
                # self.ids.tb.title='<<< disks >>>'
                self.tb.title='<<< disks >>>'
                self.create_disks() 
            else:
                # print(self.ad)
                a=self.ad 
                a=a.split('\\')
                # print(a) 
                s=''
                for w in range(len(a)-2):
                    s+=a[w]+'\\'
                # print(s)
                self.ad=s
                lf=os.listdir(self.ad)
                self.ids.fm.ids.register.clear_widgets()
                self.goto_items(lf,self.ad) 

    def create_disks(self):
        try:
            self.ids.fm.ids.register.clear_widgets()
            self.ld=self.fmz.t_ld['disk']
            # print(self.ld) 
            for ld in self.ld:
                name=ld 
                address=ld 
                list_file=os.listdir(address)
                items=str(len(list_file))
                td=os.path.getmtime(address)
                td=time.ctime(td)
                date=td
                t=ThreeLineIconListItem(
                    IconLeftWidgetWithoutTouch(icon='folder-home'),
                    text=name,
                    secondary_text=items,
                    tertiary_text=date,
                    on_press=self.goto_address  
                    )
                self.ids.fm.ids.register.add_widget(t)
        except:pass
    def goto_address(self,instace):
        self.ad=instace.text 
        # self.t_address['address']+=instace.text 
        self.ids.fm.ids.register.clear_widgets()
        lf=os.listdir(self.ad)       
        self.goto_items(lf,self.ad) 
    
    def goto_items(self,list_file,address):
        try:
            # self.ids.tb.title=address 
            self.tb.title=address 
            for file_name in list_file:
                if file_name[-3]=='.' or file_name[-4]=='.' or file_name[-5]=='.':
                    at=address
                    at+=file_name
                    tt=os.path.getmtime(at)
                    tt=time.ctime(tt)
                    s=os.path.getsize(at)
                    z=self.return_size(s)
                    self.ids.fm.ids.register.add_widget(ThreeLineIconListItem(
                        IconLeftWidgetWithoutTouch(icon='file'),
                        text=file_name,
                        secondary_text=str(z[0])+z[1],
                        tertiary_text=tt, 
                        on_press=self.run_file,
                    ))
                else:
                    at=address
                    at+=file_name
                    # print(at) 
                    lt=os.listdir(at)
                    tt=os.path.getmtime(at)
                    tt=time.ctime(tt)
                    self.ids.fm.ids.register.add_widget(ThreeLineIconListItem(
                        IconLeftWidgetWithoutTouch(icon='folder'),
                        text=file_name,
                        secondary_text=str(len(lt)),
                        tertiary_text=tt,
                        on_press=self.goto_address_file
                    ))
        except:pass
    def run_file(self,instance):
        try:
            address=self.ad 
            address+=instance.text 
            os.system(fr'{address}')
        except:
            None
    def goto_address_file(self,instace):
        self.ad+=instace.text+'\\'
        # print(self.ad) 
        self.ids.fm.ids.register.clear_widgets()
        lf=os.listdir(self.ad)
        self.goto_items(lf,self.ad) 
    def return_size(self,size):
        s=size
        if len(str(s))<=3:
            return([s,'B'])
        elif len(str(s))<=6:
            s=float(s/1024)
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'KB'])
        elif len(str(s))<=9:
            s=float(s/(1024*1024))
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'MB'])
        elif len(str(s))<=12:
            s=float(s/(1024*1024*1024))
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'GB'])
        elif len(str(s))<=15:
            s=float(s/(1024*1024*1024*1024))
            ts=str(s)
            n=ts.find('.')
            s=ts[0:n+2+1]
            return([s,'TB'])
        else:pass       

    def about(self):
        toast('This is App Make AliasgharZahdyan\n          <<<===[[[[[A.Z.T]]]]]===>>>')
#------------------APP-----------------------
class MainApp(MDApp):
    def __init__(self,*args,**kwargs):
        super(MainApp,self).__init__(*args,**kwargs)
        # self.fmz=FileManagerZ()
    def build(self):
        self.theme_cls.theme_style='Dark'
        return Style()
#     def on_start(self):
#         self.fmz.create_disks() 
# ------------------------------------------------
MainApp().run()
# self.ids.tb.title=self.ad