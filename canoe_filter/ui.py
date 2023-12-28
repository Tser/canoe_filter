#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2023/12/28 0:15
@File  : ui.py
'''
'''
基于Tkinter设计UI界面，首先是第一行输入框可以输入CANoe配置文件的地址或者点击后面的选择文件的按钮【...】
'''

import re
import threading
import tkinter as tk
from tkinter.ttk import Separator
from tkinter import filedialog, ttk
from py_canoe import CANoe, wait

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('CANoe信号过滤工具')
        # 窗口设置为自适应
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # self.root.geometry('600x400')
        # self.root.resizable(False, False)
        self.file_path = tk.StringVar()
        self.file_path.set('输入CANoe配置文件')
        # 通道
        self.channel = tk.IntVar()
        self.channel.set(1)
        # ID
        self.ECU_filter_id = tk.StringVar()
        self.ECU_filter_id.set('0x00')
        # 信息/数据
        self.ECU_filter_data = tk.StringVar()
        self.ECU_filter_data.set('00 00 00 00 00 00 00 00')

        self.status = tk.StringVar()
        self.status.set('stop')

        self.status_text = tk.StringVar()
        self.status_text.set('停止')

        self.index = 0

        self.thread = threading.Thread(target=self.start_thread, daemon=True)

        self.create_widgets()

    def create_widgets(self):
        row_0 = tk.Frame(self.root, height=20)
        row_0.pack()

        row_1 = tk.Frame(self.root, height=20)
        self.file_path_entry = tk.Entry(row_1, width=50, textvariable=self.file_path)
        self.file_path_entry.grid(row=0, column=0)
        tk.Label(row_1, width=2).grid(row=0, column=1)
        self.button = tk.Button(row_1, text='. . .', command=self.open_file, width=5)
        self.button.grid(row=0, column=2)

        # 监控输入框内焦点，当输入框获得焦点时会触发事件
        self.file_path_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.file_path_entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.file_path_entry.bind('<KeyRelease-Return>', self.on_entry_focus_out)
        row_1.pack()

        row_2 = tk.Frame(self.root, height=20)
        row_2.pack()

        # row_3添加开始过滤按钮，
        row_3 = tk.Frame(self.root, height=20)
        tk.Button(row_3, text='开始过滤', width=10, command=self.start_filtering).grid(row=0, column=0)
        tk.Label(row_3, width=2).grid(row=0, column=1)
        tk.Button(row_3, text='暂停过滤', width=10, command=self.suspend_filtering).grid(row=0, column=2)
        tk.Label(row_3, width=2).grid(row=0, column=3)
        tk.Button(row_3, text='停止过滤', width=10, command=self.stop_filtering).grid(row=0, column=4)
        tk.Label(row_3, width=2).grid(row=0, column=5)
        tk.Button(row_3, text='重置过滤', width=10, command=self.reset_filtering).grid(row=0, column=6)
        row_3.pack()

        row_32 = tk.Frame(self.root, height=20)
        # 添加分界线
        Separator(row_32, orient='horizontal').pack(fill='x', pady=5)
        row_32.pack()

        # 通道下拉框选择，ID输入框，信息输入框
        row_4 = tk.Frame(self.root, height=20)
        tk.Label(row_4, text='通 道:').grid(row=0, column=0)
        ttk.Combobox(row_4, values=(1, 2), width=3, textvariable=self.channel).grid(row=0, column=1)
        tk.Label(row_4, width=2).grid(row=0, column=2)
        tk.Label(row_4, text='I D:').grid(row=0, column=3)
        self.ecu_id_entry = tk.Entry(row_4, width=6, textvariable=self.ECU_filter_id)
        self.ecu_id_entry.grid(row=0, column=4)
        # 监控输入框内焦点，当输入框获得焦点时会触发事件
        self.ecu_id_entry.bind('<FocusIn>', self.on_id_focus_in)
        self.ecu_id_entry.bind('<FocusOut>', self.on_id_focus_out)
        self.ecu_id_entry.bind('<KeyRelease-Return>', self.on_id_focus_out)  # 回车键松开时执行

        tk.Label(row_4, width=2).grid(row=0, column=5)
        tk.Label(row_4, text='信 息:').grid(row=0, column=6)
        self.ecu_data_entry = tk.Entry(row_4, width=25, textvariable=self.ECU_filter_data)
        self.ecu_data_entry.grid(row=0, column=7)
        # 监控输入框内焦点，当输入框获得焦点时会触发事件
        self.ecu_data_entry.bind('<FocusIn>', self.on_data_focus_in)
        self.ecu_data_entry.bind('<FocusOut>', self.on_data_focus_out)
        self.ecu_data_entry.bind('<KeyRelease-Return>', self.on_data_focus_out)  # 回车键松开时执行
        row_4.pack()

        row_5 = tk.Frame(self.root, height=20)
        row_5.pack()

        row_6 = tk.Frame(self.root, height=20)
        # 多行表格（编号、时间、通道、ID、数据），支持滚动条
        self.tree = ttk.Treeview(row_6, columns=('时间', '通道', 'ID', '数据'))
        self.tree.heading('#0', text='编号', anchor='w')
        self.tree.heading('时间', text='时间', anchor='w')
        self.tree.heading('通道', text='通道', anchor='center')
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('数据', text='数据', anchor='w')
        # # 设置列宽
        self.tree.column('#0', width=50)
        self.tree.column('时间', width=130)
        self.tree.column('通道', width=50)
        self.tree.column('ID', width=50)
        self.tree.column('数据', width=300)
        self.tree.pack()
        row_6.pack()

        row_7 = tk.Frame(self.root, height=40)
        tk.Label(row_7, textvariable=self.status_text, bg='yellow', fg='red', font=12).pack(side='left')
        row_7.pack()


    def on_entry_focus_in(self, event):
        if self.file_path.get() == '输入CANoe配置文件':
            self.file_path.set('')

    def on_entry_focus_out(self, event):
        if self.file_path.get() == '':
            self.file_path.set('输入CANoe配置文件')

    def on_id_focus_in(self, event):
        if self.ECU_filter_id.get() == '0x00':
            self.ECU_filter_id.set('')

    def on_id_focus_out(self, event):
        if self.ECU_filter_id.get() == '':
            self.ECU_filter_id.set('0x00')
        elif not self.ECU_filter_id.get().lower().startswith('0x'):
            self.ECU_filter_id.set('0x' + self.ECU_filter_id.get())
        else:
            pass


    def on_data_focus_in(self, event):
        if self.ECU_filter_data.get() == '00 00 00 00 00 00 00 00':
            self.ECU_filter_data.set('')

    def on_data_focus_out(self, event):
        if self.ECU_filter_data.get() == '':
            self.ECU_filter_data.set('00 00 00 00 00 00 00 00')
        else:
            # 使用正则验证数据是否满足标准格式：xx xx xx xx xx xx xx xx ，其中xx为十六进制数, 没有空格的自动添加上空格
            patten = re.compile(r'^[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}\s+[0-9a-fA-F]{2}$')
            if patten.match(self.ECU_filter_data.get()):
                pass
            else:
                self.ECU_filter_data.set('00 00 00 00 00 00 00 00')



    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('CANoe配置文件', '*.cfg')],
            title='选择CANoe配置文件',
            initialdir='~/Desktop',
        )
        self.file_path.set(file_path)

    def start_filtering(self):
        # 通过py_canoe启动CANoe并实时获取CAN信号
        self.status.set('start')
        self.status_text.set('开始')
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.start_thread, daemon=True)
            self.thread.start()

    def suspend_filtering(self):
        self.status.set('suspend')
        self.status_text.set('暂停')

    def stop_filtering(self):
        self.status.set('stop')
        self.status_text.set('停止')

    def reset_filtering(self):
        self.tree.delete(*self.tree.get_children())
        self.index = 0

    def start_thread(self):
        # canoe = CANoe()
        # canoe.open(self.file_path.get())

        # wait(2)
        while True:
            while True:
                # 监控关闭窗口事件，防止卡线程
                self.root.protocol('WM_DELETE_WINDOW', self.window_close)

                if self.status.get() == 'start':
                    # canoe.start_measurement()
                    # canoe_data = canoe.get_can_bus_statistics(1)
                    # 将实时数据添加到表格中,编号自动累计
                    self.index += 1
                    self.tree.insert('', 'end', text=str(self.index), values=('2023-01-01 00:00:00', '1', '1', '10 02 00 00 00 00 00 00'))

                    wait(1)  # 实际场景去掉

                elif self.status.get() == 'suspend':
                    wait(0.5)
                elif self.status.get() == 'stop':
                    break
                else:
                    pass

        # canoe.stop_measurement()

    def stop_thread(self):
        pass

    def suspend_thread(self):
        pass

    def window_close(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()