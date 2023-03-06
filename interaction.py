import time
from tkinter import *
from PIL import ImageTk, Image
import shutil
import os

max_number = 10
src = "path/to/your/images/folder/"
filelist=[]
for root, dirs, files in os.walk(src):
    for x in files:
        if x[-4:] == ".JPG" or x[-4:] == ".jpg":
            filelist.append(x)
files = filelist

bv_negative = src + "bv_negative/"
bv_positive = src + "bv_positive/"
bv_mid = src + "bv_mid/"
vvc_spore = src + "vvc_spore/"
vvc_si = src + "vvc_si/"
coli_0 = src + "coli_0/"
coli_1 = src + "coli_1/"
coli_2 = src + "coli_2/"
coli_3 = src + "coli_3/"
coli_4 = src + "coli_4/"

pic_num = 0
pic_name = None
img = None
pre = None
LOG_LINE_NUM = 0
r = 0  # bv selector
t = 0  # coli selector
vvc = 0  # vvc selector


class MY_GUI():
    def __init__(self, pic_classification):
        self.pic = pic_classification

    def set_init_window(self):
        self.pic.title("Classification System")
        self.pic.geometry('1075x695+10+10')
        self.pic.resizable(0, 0)

        self.frame1 = Frame(self.pic)
        self.frame1.grid(row=0, column=0)
        self.frame2 = Frame(self.pic)
        self.frame2.grid(row=0, column=1)

        self.frame3 = Frame(self.frame2)
        self.frame3.grid(row=0, column=0)
        self.frame4 = Frame(self.frame2)
        self.frame4.grid(row=1, column=0)
        self.frame5 = Frame(self.frame2)
        self.frame5.grid(row=2, column=0)
        self.frame6 = Frame(self.frame2)
        self.frame6.grid(row=3, column=0)

        self.frame7 = Frame(self.frame1)
        self.frame7.grid(row=0, column=0)

        self.frame8 = Frame(self.frame1)
        self.frame8.grid(row=1, column=0)

        # ---------- START -------------
        self.start_button = Button(self.frame3, width=8, height=2, text="开始导入", command=self.startPic)
        self.start_button.grid()

        self.white0 = Label(self.frame3, width=8, height=2)
        self.white0.grid()

        # -----------BV--------------
        bv_r = IntVar()
        self.bv_label = Label(self.frame4, text="bv:")
        self.bv_label.grid(row=0, column=0)

        self.bv_negative = Radiobutton(self.frame4, text="bv阴性", value=1, variable=bv_r, command=self.bv1)
        self.bv_negative.grid(row=0, column=1)

        self.bv_mid = Radiobutton(self.frame4, text="bv中性", value=2, variable=bv_r, command=self.bv2)
        self.bv_mid.grid(row=0, column=2)

        self.bv_positive = Radiobutton(self.frame4, text="bv阳性", value=3, variable=bv_r, command=self.bv3)
        self.bv_positive.grid(row=0, column=3)

        # ---------VVC-------------
        checkVar = StringVar(value="0")
        self.vvc_label = Label(self.frame4, text="vvc:")
        self.vvc_label.grid(row=1, column=0)

        self.vvc_spore = Checkbutton(self.frame4, text="孢子", command=self.vvc1)
        self.vvc_spore.grid(row=1, column=1)

        self.vvc_turf = Checkbutton(self.frame4, text="菌丝", command=self.vvc2)
        self.vvc_turf.grid(row=1, column=2)

        # ----------Big coli-------------
        t = IntVar()

        self.coli_label = Label(self.frame4, text="大杆菌:")
        self.coli_label.grid(row=2, column=0)

        self.coli_0 = Radiobutton(self.frame4, text="大杆菌0级", value=1, variable=t, command=self.coli0)
        self.coli_0.grid(row=2, column=1)

        self.coli_1 = Radiobutton(self.frame4, text="大杆菌1级", value=2, variable=t, command=self.coli1)
        self.coli_1.grid(row=2, column=2)

        self.coli_2 = Radiobutton(self.frame4, text="大杆菌2级", value=3, variable=t, command=self.coli2)
        self.coli_2.grid(row=3, column=1)

        self.coli_3 = Radiobutton(self.frame4, text="大杆菌3级", value=4, variable=t, command=self.coli3)
        self.coli_3.grid(row=3, column=2)

        self.coli_4 = Radiobutton(self.frame4, text="大杆菌4级", value=5, variable=t, command=self.coli4)
        self.coli_4.grid(row=3, column=3)

        self.whiteSpace = Label(self.frame5, height=1)
        self.whiteSpace.grid()
        self.confirm = Button(self.frame5, height=2, width=10, text="确认", command=self.confirmAndNext)
        self.confirm.grid()
        self.whiteSpace = Label(self.frame5, height=1)
        self.whiteSpace.grid()

        self.log_button = Button(self.frame6, text="search_log", command=self.write_log_to_Text)
        self.log_button.grid(row=0, sticky="W")

        self.delete_button = Button(self.frame6, text="delete_log", command=self.delete_log)
        self.delete_button.grid(row=0, sticky="E")

        self.log_Text = Text(self.frame6, width=45, height=18)
        self.log_Text["bg"] = "lightyellow"
        self.log_Text.grid(row=1, column=0)

        # frame2----------

        self.pic_label = Label(self.frame1, textvariable=pic_name)
        self.pic_label.grid(row=0, column=0)
        self.pic_text = Text(self.frame1, width=100, height=40)
        self.pic_text["bg"] = "Honeydew"
        self.pic_text.grid(row=1, column=0)

        self.pic_control_button = Button(self.frame1, width=10, height=2, text="前一张", command=self.get_pre_pic)
        self.pic_control_button.grid(row=2, sticky=W)

        self.pic_control_button2 = Button(self.frame1, width=10, height=2, text="后一张", command=self.get_next_pic)
        self.pic_control_button2.grid(row=2, sticky=E)

    # frame1-------

    # 功能函数
    def startPic(self):
        global pic_num
        global img
        global pre
        dir = src + files[pic_num]
        try:
            pre = Image.open(dir).resize((640, 512), Image.ANTIALIAS)
        except Exception as e:
            self.get_next_pic()
        img = ImageTk.PhotoImage(pre)
        self.pic_text.delete(0.0, END)
        self.pic_text.image_create(END, image=img)
        return

    # todo:在第一张时需要跳出，且中间损坏照片应该自动过去
    def get_pre_pic(self):
        global pic_num
        global img
        global pre
        if pic_num<=0:
            return
        pre_num = pic_num - 1
        pic_num = pic_num - 1
        pic_name.set(files[pic_num])
        dir = src + files[pic_num]
        try:
            pre = Image.open(dir).resize((640, 512), Image.ANTIALIAS)
        except Exception as e:
            self.get_pre_pic()
        if pre is None:
            return
        img = ImageTk.PhotoImage(pre)
        self.pic_text.delete(0.0, END)
        self.pic_text.image_create(END, image=img)
        return

    # todo:在最后一张时需要跳出，且中间损坏照片应该自动过去
    def get_next_pic(self):
        global pic_num
        global img
        global pre
        if pic_num>=len(files):
            return
        next_num = pic_num + 1
        dir = src + files[next_num]
        print(dir)
        pic_num = pic_num + 1
        pic_name.set(files[pic_num])
        try:
            pre = Image.open(dir).resize((640, 512), Image.ANTIALIAS)
        except Exception as e:
            # pic_num = pic_num + 1
            # pic_name.set(str(pic_num)+".jpg")
            print("error")
            self.get_next_pic()
        if pre is None:
            return

        img = ImageTk.PhotoImage(pre)
        self.pic_text.delete(0.0, END)
        self.pic_text.image_create(END, image=img)
        return

    def confirmAndNext(self):
        global r
        global t
        global vvc
        if r == 0:
            print("error, please select bv")
            return
        if t == 0:
            print("error, please select coli")
            return
        dir1 = src+files[pic_num]
        if r == 1:
            shutil.copyfile(dir1 , bv_negative + files[pic_num])
        elif r == 2:
            shutil.copyfile(dir1 , bv_mid +  files[pic_num])
        elif r == 3:
            shutil.copyfile(dir1 , bv_positive +  files[pic_num])
        if t == 1:
            shutil.copyfile(dir1 , coli_0 + files[pic_num])
        elif t == 2:
            shutil.copyfile(dir1 , coli_1 + files[pic_num])
        elif t == 3:
            print("hi")
            print(dir)
            print(coli_2 + files[pic_num])
            shutil.copyfile(dir1 , coli_2 + files[pic_num])
        elif t == 4:
            shutil.copyfile(dir1 , coli_3 +files[pic_num])
        elif t == 5:
            shutil.copyfile(dir1 , coli_4 + files[pic_num])
        if vvc == 1:
            shutil.copyfile(dir1 , vvc_spore + files[pic_num])
            vvc = 0
        elif vvc == 2:
            shutil.copyfile(dir1 , vvc_si + files[pic_num])
            vvc = 0
        elif vvc == 3:
            shutil.copyfile(dir1 , vvc_si + files[pic_num])
            shutil.copyfile(dir1 , vvc_spore + files[pic_num])
            vvc = 0
        os.remove(dir1)
        self.get_next_pic()
        return

    def bv1(self):
        global r
        r = 1

    def bv2(self):
        global r
        r = 2

    def bv3(self):
        global r
        r = 3

    def coli0(self):
        global t
        t = 1

    def coli1(self):
        global t
        t = 2

    def coli2(self):
        global t
        t = 3

    def coli3(self):
        global t
        t = 4

    def coli4(self):
        global t
        t = 5

    def vvc1(self):
        global vvc
        if vvc == 2:
            vvc = 3
        else:
            vvc = 1

    def vvc2(self):
        global vvc
        if vvc == 1:
            vvc = 3
        else:
            vvc = 2

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 搜索动态打印
    def write_log_to_Text(self):
        global pic_num
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(pic_num) + "\n"  # 换行
        if LOG_LINE_NUM <= 10:
            self.log_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_Text.delete(1.0, 2.0)
            self.log_Text.insert(END, logmsg_in)

    def delete_log(self):
        self.log_Text.delete(1.0, 'end')

    def Delete_searchingText(self):
        self.result_data_Text.delete("0.0", END)
        self.music_Text.delete("0.0", END)
        self.comment_Text.delete("0.0", END)
        self.url_address_Text.delete("0.0", END)
        self.picture_Text.delete("0.0", END)
        self.presearch_Text.delete("0.0", END)
        self.rating_search_Text.delete("0.0", END)


def gui_start():
    global pic_name
    init_window = Tk()
    pic_name = StringVar()
    pic_name.set(str(pic_num) + ".jpg")

    MYY_MUS = MY_GUI(init_window)
    # 设置根窗口默认属性
    MYY_MUS.set_init_window()

    init_window.mainloop()


gui_start()
