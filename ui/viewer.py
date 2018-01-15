from tkinter import *
from tkinter import ttk
from usr.gen_excel import *
from usr.update_db import *
from usr.show_last_day import *
#import tkMessageBox

ENGLISH = 1
CHINESE = 2

language = CHINESE
if language == ENGLISH:
    STR_GP_1_BTN = "Check Database"
    STR_GP_1_SH = "SH Last Day: "
    STR_GP_1_HK = "HK Last Day: "
    STR_GP0_RBTN_SH = "SH"
    STR_GP0_RBTN_HK = "HK"
    STR_GP1_BTN = "UPDATE"
    STR_GP1_TEXT = "Idle"
    STR_GP2_BTN = "GEN"
    STR_GP2_TEXT = "Idle"
if language == CHINESE:
    STR_GP_1_BTN = "查看数据库更新日期"
    STR_GP_1_SH = "沪 更新日期: "
    STR_GP_1_HK = "港 更新日期: "
    STR_GP0_RBTN_SH = "沪"
    STR_GP0_RBTN_HK = "港"
    STR_GP1_BTN = "更新数据库"
    STR_GP1_TEXT = "空闲"
    STR_GP2_BTN = "生成Excel"
    STR_GP2_TEXT = "空闲"


STR_GAP = "*********************************"



TYPE_SH = "Hu"
TYPE_HK = "Gang"

class viewer:
    def __init__(self):
        pass

    def close_callback(self):
        try:
            self.update_l.stop()
            self.gen_l.stop()
            time.sleep(1)
        except:
            pass
        self.tk_root.destroy()
        exit(0)

    def __init_basic(self):
        self.tk_root = Tk()
        self.tk_root.protocol("WM_DELETE_WINDOW", self.close_callback)


    def __init_wid_last_days(self):
        self.text_gp_1_hk = Text(self.tk_root, height=1)
        self.text_gp_1_hk.pack()
        self.text_gp_1_hk.config(state=DISABLED)
        self.text_gp_1_sh = Text(self.tk_root, height=1)
        self.text_gp_1_sh.pack()
        self.text_gp_1_sh.config(state=DISABLED)
        self.btn_gp1 = Button(self.tk_root, text = STR_GP_1_BTN,command=lambda: self.get_last_days())
        self.btn_gp1.pack()
        self.text_gp_1_gap = Text(self.tk_root, height=1)
        self.text_gp_1_gap.pack()
        self.text_gp_1_gap.insert('insert', STR_GAP)
        self.text_gp_1_gap.config(state=DISABLED)

    def __init_wid_mkt_type(self):
        ### Single Select Button
        self.mkt_type = StringVar()
        self.mkt_type.set(TYPE_SH)
        self.rbtn_gp0_sh = Radiobutton(self.tk_root, text=STR_GP0_RBTN_SH,variable=self.mkt_type, value=TYPE_SH,anchor=W,width=20)
        self.rbtn_gp0_sh.pack(fill=X)
        self.rbtn_gp0_hk = Radiobutton(self.tk_root, text=STR_GP0_RBTN_HK,variable=self.mkt_type, value=TYPE_HK,anchor=W,width=20)
        self.rbtn_gp0_hk.pack(fill=X)
        self.text_gp0_gap = Text(self.tk_root, height=1)
        self.text_gp0_gap.pack()
        self.text_gp0_gap.insert('insert', STR_GAP)
        self.text_gp0_gap.config(state=DISABLED)


    def __init_wid_update(self):
        ## Button for update
        self.btn_gp1 = Button(self.tk_root, text = STR_GP1_BTN,command=lambda: self.usr_update_db())
        self.btn_gp1.pack()
        self.text_gp1 = Text(self.tk_root, width=20, height=1)
        #self.text_gp1.config(state=DISABLED)
        self.text_gp1.pack()
        self.text_gp1_gap = Text(self.tk_root, height=1)
        self.text_gp1_gap.pack()
        self.text_gp1_gap.insert('insert', STR_GAP)
        self.text_gp1_gap.config(state=DISABLED)

    def __init_wid_cycle_num(self):
        ## Combobox for cycle and number
        self.text_gp2_cycle = Text(self.tk_root, width=20, height=1)
        self.text_gp2_cycle.pack()
        self.text_gp2_cycle.insert('insert', "Cycle")
        self.text_gp2_cycle.config(state=DISABLED)

        cycle_list = []
        for i in range(1, 21):
            cycle_list.append(str(i))
        self.comvalue_val_cycle = StringVar()
        self.comboxlist_gp2_cycle = ttk.Combobox(self.tk_root, textvariable=self.comvalue_val_cycle,width=10)  # 初始化
        self.comboxlist_gp2_cycle["values"] = cycle_list
        self.comboxlist_gp2_cycle.current(0)
        self.cycle = int(cycle_list[0])
        self.comboxlist_gp2_cycle.bind("<<ComboboxSelected>>", self.__set_combox_cycle)
        self.comboxlist_gp2_cycle.pack()


        self.text_gp2_num = Text(self.tk_root,width=20, height=1)
        self.text_gp2_num.pack()
        self.text_gp2_num.insert('insert', "Number")
        self.text_gp2_num.config(state=DISABLED)

        num_list = []
        for i in range(1, 11):
            num_list.append(str(i))
        self.comvalue_val_num = StringVar()
        self.comboxlist_gp2_num = ttk.Combobox(self.tk_root, textvariable=self.comvalue_val_num,width=10)
        self.comboxlist_gp2_num["values"] = num_list
        self.comboxlist_gp2_num.current(0)
        self.number = int(num_list[0])
        self.comboxlist_gp2_num.bind("<<ComboboxSelected>>", self.__set_combox_num)
        self.comboxlist_gp2_num.pack()


        self.btn_gp2_gen = Button(self.tk_root, text = STR_GP2_BTN,command=lambda: self.usr_gen_excel())
        self.btn_gp2_gen.pack()
        self.text_gp2 = Text(self.tk_root, height=1)
        self.text_gp2.insert('insert', STR_GP2_TEXT)
        #self.text_gp2.config(state=DISABLED)
        self.text_gp2.pack()
        self.text_gp2_gap = Text(self.tk_root, height=1)
        self.text_gp2_gap.pack()
        self.text_gp2_gap.insert('insert', STR_GAP)
        self.text_gp2_gap.config(state=DISABLED)


    def __set_combox_cycle(self, *args):
        self.cycle = int(self.comboxlist_gp2_cycle.get())
        #print("set cycle " + str(self.cycle))

    def __set_combox_num(self, *args):
        self.number = int(self.comboxlist_gp2_num.get())
        #print("set num " + str(self.number))


    def init_components(self):
        self.__init_basic()
        self.__init_wid_last_days()
        self.__init_wid_mkt_type()
        self.__init_wid_update()
        self.__init_wid_cycle_num()

    def get_last_days(self):
        show_ld = show_last_day()
        show_ld.run()
        #self.text_gp0_gap.insert('insert', STR_GAP)
        #self.text_gp0_gap.config(state=DISABLED)
        self.text_gp_1_sh.config(state=NORMAL)
        self.text_gp_1_sh.delete(1.0, "end")
        self.text_gp_1_sh.insert('insert', STR_GP_1_SH + str(show_ld.last_day_sh))
        self.text_gp_1_sh.config(state=DISABLED)

        self.text_gp_1_hk.config(state=NORMAL)
        self.text_gp_1_hk.delete(1.0, "end")
        self.text_gp_1_hk.insert('insert', STR_GP_1_HK + str(show_ld.last_day_hk))
        self.text_gp_1_hk.config(state=DISABLED)



    def start_viewer(self):
        self.tk_root.mainloop()



    def set_refresh_text_gp1(self, text, update_hl):
        str = update_hl.get_update_status()
        text.delete(1.0,"end")
        text.insert("end", str)
        text.after(100, self.set_refresh_text_gp1, text, update_hl)

    def set_refresh_text_gp2(self, text, gen_hl):
        str = gen_hl.get_gen_status()
        text.delete(1.0,"end")
        text.insert("end", str)
        text.after(100, self.set_refresh_text_gp2, text, gen_hl)

    def usr_update_db(self):
        self.update_l = update_db(self.mkt_type.get())
        self.set_refresh_text_gp1(self.text_gp1, self.update_l)
        self.update_l.start()


    def usr_gen_excel(self):
        self.gen_l = gen_excel(self.mkt_type.get(), self.cycle, self.number)
        self.set_refresh_text_gp2(self.text_gp2, self.gen_l)
        self.gen_l.start()

