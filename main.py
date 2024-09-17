from typing import Tuple
import customtkinter as ctk 
from CTkMessagebox import CTkMessagebox
from CTkToolTip import *
from datetime import datetime 
import threading
import ctypes
import sys
import os 
import subprocess as sub
import pathlib



class AppMain(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.resizable(False,False)
        self.title('Limpa Tudo')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x = (screen_width - window_width) // 2 -100
        y = (screen_height - window_height) // 2 -100
        
        self.geometry(f"{250}x{300}+{x}+{y}")
        
        self.__display_main()
        
    def __display_main(self):
        
        self.checkbox = []
        # self.options_execute = [
        #     "Delete Recent",
        #     "Delete Temp",
        #     "Delete Prefetch",
        #     "Execute SFC",
        #     "Execute CHKDSK /SCAN",
        #     "Execute CHDDSK /r", 
        #     "Desligar PC/",
        #     "Reiniciar",        
        #                         ]
        
        self.options_execute = [
            {"Delete Recent":"Deleta os arquivos recentes"},
            {"Delete Temp":"Deleta os arquivos temporários"},
            {"Delete Prefetch": "Deleta os arquivos do prefetch"},
            {"Execute SFC": "Realiza a verificação do SFC /SCANNOW"},
            {"Execute CHKDSK /SCAN" : "Realiza scan"},
            {"Execute CHDDSK /r": "Essa opção terá que reiniciar o sistema operacional"}, 
            {"Desligar PC/": "Essa opção deslia o sistema"},
            {"Reiniciar": "Reiniciar o sistema"},        
                                ]
        
        
        self.label_title = ctk.CTkLabel(self, text="Limpa Tudo",font=("Roboto",18), text_color='Orange')
        
        # for i in self.options_execute:
        #     checkbox = ctk.CTkCheckBox(self,text=i,font=("Roboto",16), command=lambda  widget = i: self.__event_checkbox(widget) )
        #     self.checkbox.append(checkbox)
        
        # for i in self.options_dic:
        #     checkbox = ctk.CTkCheckBox(self,text=[a.replace('{','') for a in i.keys()],font=("Roboto",16), command=lambda  widget = [a for a in i.keys()]: self.__event_checkbox(widget) )
        #     print([list(a)[:-1] for a in i.keys()])
        #     tooltip = CTkToolTip(checkbox, [c.removeprefix('{') for c in i.values()])
        #     self.checkbox.append(checkbox)
        
        for i in self.options_execute:
            for a in i.keys():
                checkbox = ctk.CTkCheckBox(self, text=a,font=("Roboto",16), command=lambda  widget = a: self.__event_checkbox(widget))
                self.checkbox.append(checkbox)
            for b in i.values():
                tooltip= CTkToolTip(checkbox,b)
            
        self.button_okay = ctk.CTkButton(self,text="Run", command=self.__run_app)

        self.label_title.pack()
        
        for i in self.checkbox:
            i.pack(expand=True,fill='both',padx = 10)
        
        self.button_okay.pack(pady=10,expand=False)    
        
        for i in self.checkbox:
            a = i.cget("text")
            if "Delete" in a:
                i.select()
          
    def __event_checkbox(self,widget):
        if  "Execute CHDDSK /r" in widget:
            for i in self.checkbox:
                if "Reiniciar"in i.cget("text") :
                    i.toggle()

    def __save_log(self,options_select,info_exec_stdout, info_exec_stderr = ""):
        filename = "log_limp_tudo.txt"
        start_log = f"_______________________iniciando log - {datetime.now()}____________________"
        
        end_log = f"_______________________Finalizando log - {datetime.now()}____________________"
        
        with open(filename, 'a', encoding='utf-8') as file:
         file.write(f"{start_log}\n{options_select}\n{info_exec_stdout}\nerro:{info_exec_stderr}\n{end_log}\n")
        
        pass                    
                         
    

        # for i in options:
    def __run_command(self, i):            
            match i:
                case "Delete Recent":
                    self.label_exec.configure(text = " Recents")
                case "Delete Temp":
                    self.label_exec.configure(text = "Temp")                    
                    result = sub.run("del /f /s /q %temp%",capture_output=True, text=True,shell=True)
                    for a in result.stdout:
                        self.label_stdout.configure(text=f"{a}")
                    self.__save_log(i,result.stdout)
                        
                case "Delete Prefetch":
                    self.label_exec.configure(text = " Prefetch")
                    # os.system("del /f /s /q C:/Windows/Prefetch/")
                    result = sub.run("del /f /s /q C:/Windows/Prefetch/",capture_output=True, text=True,shell=True)
                    for a in result.stdout:
                        self.label_stdout.configure(text=f"{a}")
                    self.__save_log(i,result.stdout)
                
                case "Execute SFC":
                    self.label_exec.configure(text = "SCF /SCANNOW")
                    result = sub.run("sfc /scannow",capture_output=True, text=True,shell=True)
                    for a in result.stdout:
                        self.label_stdout.configure(text=f"{a}")
                    self.__save_log(i,result.stdout,result.stderr)
                    
                case "Execute CHKDSK /SCAN":
                    self.label_exec.configure(text = "CHKDSK /SCAN")
                    result = sub.run("chkdsk /scan",capture_output=True, text=True,shell=True)
                    for a in result.stdout:
                        self.label_stdout.configure(text=f"{a}")
                    self.__save_log(i,result.stdout,result.stderr)
                case "Execute CHDDSK /r":
                    self.label_exec.configure(text = "CHKDSK /R")
                    result = sub.run("chkdsk /r",capture_output=True, text=True,shell=True)
                    self.label_stdout.configure(text=f"{result.stdout}") 
                    self.__save_log(i,result.stdout,result.stderr)
                
                case "Desligar PC/":
                    self.label_exec.configure(text = "Desligando...")
                    msg = CTkMessagebox(title="Warning",message="Seu PC desligará em 5 minutos\nFeche tudo que precisar!!! ")
                    result = sub.run("shutdown -f -s -t 300",capture_output=True, text=True,shell=True)
                    self.label_stdout.configure(text=f"{result.stdout}") 
                    self.__save_log(i,result.stdout,result.stderr)    
                case "Reiniciar":
                    
                    self.label_exec.configure(text = "Reinciando...")
                    msg = CTkMessagebox(title="Warning",message="Seu PC reiniciará em 5 minutos\nFeche tudo que precisar!!! ")
                    result = sub.run("shutdown -f -r -t 300",capture_output=True, text=True,shell=True)
                    self.label_stdout.configure(text=f"{result.stdout}") 
                    self.__save_log(i,result.stdout,result.stderr) 
                
                case _:
                    msg = CTkMessagebox(title="Warning",message="Processo finalizado")
                          
    def __start_func(self,options):
        self.top_level = ctk.CTkToplevel(self,height = 300, width = 450)
        self.top_level.resizable(False,False)
        self.top_level.title('Limpa Tudo')
        screen_width = self.top_level.winfo_screenwidth()
        screen_height = self.top_level.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x = (screen_width - window_width) // 2 -100
        y = (screen_height - window_height) // 2 -100
        self.top_level.geometry(f"{250}x{300}+{x}+{y}")        
        self.top_level.after(2000, lambda: self.msg.destroy())
        
        self.top_level.focus_force()
        self.label_exec = ctk.CTkLabel(self.top_level, text="Iniciando", font=("Arial",16))
        self.label_stdout= ctk.CTkLabel(self.top_level, text="Iniciando", font=("Arial",10))
        self.label_exec.pack(pady=50)
        
        self.progressbar = ctk.CTkProgressBar(self.top_level,determinate_speed=1)
        self.progressbar.pack(fill = 'x')
        self.label_stdout.pack()
        self.progressbar.set(0)
        self.progressbar.start() 
        
        for i in options:
            threading.Thread(target=self.__run_command, args=(i,)).start()                       
                        

  
    def __run_app(self):
        options_select_list = []
        options_select = ''
        
        for check in self.checkbox:
            if check.get() == 1:
                a = check.cget("text")
                options_select_list.append(a)
                if options_select == '':
                    options_select = a
                else:
                    options_select = options_select + ', ' + a    
        if len(options_select) > 0: 
            self.msg = CTkMessagebox(title="Warning",message=f"As seguintes opções serão executadas:\n {options_select}") 
            self.msg.after(50,lambda options = options_select_list :  self.__start_func(options))
            
            
            
        else: 
            msg = CTkMessagebox(title="Warning",message=f"Nenhuma opção foi marcada.")     
            
            
def is_admin():
    """Verifica se o programa está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    if not is_admin():
        # Se não for admin, solicita permissões elevadas e relança o script
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()  # Sai do processo atual após tentar relançar como administrador
    else:
        # Somente executa a aplicação se já estiver como administrador
        app = AppMain()
        app.mainloop()