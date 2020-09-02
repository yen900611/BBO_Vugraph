import tkinter as tk

class TransferUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BBO Vugraph File Transfer")
        '''
        寬度 500,高度 400,螢幕位置 X 400,螢幕位置 Y 200
        '''
        self.window.geometry('500x400+400+200')
        self.action = Transfer(self)

    def create_widget(self):
        self.header_label = tk.Label(self.window, text='僅可輸入英文及數值字元')
        self.header_label.pack()  # 標籤化

        self.eventName_frame = tk.Frame(self.window)  # 容器
        self.eventName_frame.pack(side=tk.TOP)  # 容器位置
        self.eventName_label = tk.Label(self.eventName_frame, text='輸入比賽名稱')  # 標籤內容
        self.eventName_label.pack(side=tk.LEFT)  # 標籤位置
        self.eventName_entry = tk.Entry(self.eventName_frame)  # 輸入成績
        self.eventName_entry.pack(side=tk.LEFT)  # 輸入格位置

        self.scoreType_frame = tk.Frame(self.window)  # 容器
        self.scoreType_frame.pack(side=tk.TOP)  # 容器位置
        self.scoreType_label = tk.Label(self.scoreType_frame, text='輸入計分方式，IMP計分請輸入"I"')  # 標籤內容
        self.scoreType_label.pack(side=tk.LEFT)  # 標籤位置
        self.scoreType_entry = tk.Entry(self.scoreType_frame)  # 輸入成績
        self.scoreType_entry.pack(side=tk.LEFT)  # 輸入格位置

        self.team1name_frame = tk.Frame(self.window)  # 容器
        self.team1name_frame.pack(side=tk.TOP)  # 容器位置
        self.team1name_label = tk.Label(self.team1name_frame, text='輸入Team1隊名')  # 標籤內容
        self.team1name_label.pack(side=tk.LEFT)  # 標籤位置
        self.team1name_entry = tk.Entry(self.team1name_frame)  # 輸入成績
        self.team1name_entry.pack(side=tk.LEFT)  # 輸入格位置

        self.team2name_frame = tk.Frame(self.window)  # 容器
        self.team2name_frame.pack(side=tk.TOP)  # 容器位置
        self.team2name_label = tk.Label(self.team2name_frame, text='輸入Team2隊名')  # 標籤內容
        self.team2name_label.pack(side=tk.LEFT)  # 標籤位置
        self.team2name_entry = tk.Entry(self.team2name_frame)  # 輸入成績
        self.team2name_entry.pack(side=tk.LEFT)  # 輸入格位置

        self.team1preScore_frame = tk.Frame(self.window)  # 容器
        self.team1preScore_frame.pack(side=tk.TOP)  # 容器位置
        self.team1preScore_label = tk.Label(self.team1preScore_frame, text='輸入Team1帶分')  # 標籤內容
        self.team1preScore_label.pack(side=tk.LEFT)  # 標籤位置
        self.team1preScore_entry = tk.Entry(self.team1preScore_frame)  # 輸入成績
        self.team1preScore_entry.pack(side=tk.LEFT)  # 輸入格位置

        self.team2preScore_frame = tk.Frame(self.window)  # 容器
        self.team2preScore_frame.pack(side=tk.TOP)  # 容器位置
        self.team2preScore_label = tk.Label(self.team2preScore_frame, text='輸入Team2帶分')  # 標籤內容
        self.team2preScore_label.pack(side=tk.LEFT)  # 標籤位置
        self.team2preScore_entry = tk.Entry(self.team2preScore_frame)  # 輸入成績
        self.team2preScore_entry.pack(side=tk.LEFT)  # 輸入格位置

        self.calculate_btn = tk.Button(self.window, text='送出',command=self.action.action)  # 按鈕點選後跑出結果
        self.calculate_btn.pack()  # 按鍵位置，未定義設定為中

    def start(self):
        self.window.mainloop()

class Transfer():
    def __init__(self,UI):
        self.UI = UI
        self.event_name = None
        self.score_type = None
        self.number_of_board = 0
        self.team1name = None
        self.team2name = None
        self.team1_pre_point = 0
        self.team2_pre_point = 0
        self.title = None

    def action(self):
        self.search_imformation()
        self.transfer_first()
        self.transfer_second()
        self.UI.window.destroy()

    def search_imformation(self):
        self.event_name = self.UI.eventName_entry.get()
        self.score_type = self.UI.scoreType_entry.get()
        self.team1name = self.UI.team1name_entry.get()
        self.team2name = self.UI.team2name_entry.get()
        self.team1_pre_point = int(self.UI.team1preScore_entry.get())
        self.team2_pre_point = int(self.UI.team2preScore_entry.get())
        data = open("vugraph.lin", mode="r+")
        lines = data.readlines()
        for line in lines: # line是字串形式，內容為每一行的內容包含換行符
            if line[:2] == "bn":
                self.number_of_board = int(line[-3:-2])-int(line[3:4])+1
                self.title = f"vg|{self.event_name},1,{self.score_type},1,{self.number_of_board},{self.team1name},{self.team1_pre_point},{self.team2name},{self.team2_pre_point}|\n"

    def transfer_first(self):
        data = open("vugraph.lin", mode="r+")
        lines = data.readlines()
        data.seek(0)
        for line in lines: # line是字串形式，內容為每一行的內容包含換行符
            if line[:2] == "vg":
                data.write(self.title)
            elif line[:2] == "mn":
                card = ""
                for i in range(len(line)):
                    if line[i:i+2] == "pn":
                        card = line[i:]
                data.write("mn||\n")
                data.write(card)
            elif line[:2] == "pw":
                data.write("pw|" + ","*(self.number_of_board*4 -1)+ "|\n")
            else:
                data.write(line)
        data.truncate()
        data.close()

    def transfer_second(self):
        data = open("vugraph.lin", mode="r+")
        lines = data.readlines()
        data.seek(0)
        for line in lines: # line是字串形式，內容為每一行的內容包含換行符
            if line[:2] == "pn":
                line = line[0:2] +"|S,W,N,E|"+line[11:]
                data.write(line)
            else:
                data.write(line)

        for line in lines: # line是字串形式，內容為每一行的內容包含換行符
            if line[:2] == "pn":
                line = line[0:2] +"|S,W,N,E|"+line[11:14]+"c"+line[15:]
                data.write(line)
            elif line[:2] == "sa":
                data.write(line)
            else:
                pass

        data.truncate()
        data.close()

if __name__ == '__main__':
    transfer = TransferUI()
    transfer.create_widget()
    transfer.start()
