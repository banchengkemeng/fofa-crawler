import os
import json
import base64
import requests
from ttkbootstrap import *
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *
from lxml import etree

def startCrawl():
    condition = base64.b64encode(entry_con.get().encode()).decode()

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50"
    }
    with open("cookie.json") as f:
        cookie = json.load(f)

    text_out.insert(INSERT, f"[*] 查询条件 {entry_con.get()}\n")
    text_out.insert(INSERT, f"[*] 开始查询...\n")
    for i in range(1,1000):
        cnt = 0
        url = f"https://fofa.info/result?qbase64={condition}&page={i}&page_size=10"
        try:
            resp = requests.get(url, cookies=cookie, headers=header)
            data = etree.HTML(resp.text)
            content_ul = data.xpath("//span[@class='aSpan']/a/@href")
            if len(content_ul) == 0:
                t = i
                break
            for u in content_ul:
                text_out.insert(INSERT,f"[+] {u}\n")
            urlList.extend(content_ul)
        except:
            cnt = cnt + 1
            if cnt > 4:
                text_out.insert(INSERT, f"[warning] 查询失败,请检查网络条件\n")
                return 0
    text_out.insert(INSERT,f"[+] 查询完成 | 共查询到{len(urlList)}条数据\n")

def writeFile():
    fileName = tkinter.filedialog.asksaveasfilename(defaultextension='.txt',filetypes=(("文本文件(txt)",".txt"),))
    if os.path.exists(fileName):
        opt = tkinter.messagebox.askokcancel(title='提示!',message='文件已存在,是否清空此文件？')
        if opt == False :
            text_out.insert(INSERT, f"[+] 已放弃导出结果!\n")
            return 0
        else:
            os.remove(fileName)
    for url in urlList:
        with open(f"{fileName}", "a") as f:
            f.write(url)
            f.write('\n')

    text_out.insert(INSERT, f"[+] 结果已保存到{fileName}中\n")
def clearOutput():
    text_out.delete(1.0,END)
    urlList.clear()

def init():
    text_out.insert(INSERT,"+ 使用本软件前,请先仔细阅读以下内容！\n")
    text_out.insert(INSERT, "+ 开始查询前,请先将config.json文件(同目录下)补充完整\n")
    text_out.insert(INSERT, "+ 文件内容为浏览器COOKIE中的refresh_token和fofa_token(先登录fofa)\n")
    text_out.insert(INSERT, "+ 点击“清空结果”可以将结果框清空\n")
    text_out.insert(INSERT, "+ 若不清空结果框,将会导出您所有的查询结果\n")
    text_out.insert(INSERT, "+ 导出结果时，只会导出URL部分,例如：http://127.0.0.1/\n")
    text_out.insert(INSERT, "+ 若无config.json文件,可在同目录下自行创建\n")
    text_out.insert(INSERT, "+ 文件内容：\n")
    text_out.insert(INSERT, "{\n  \"refresh_token\": \"\",\n  \"fofa_token\": \"\"\n}\n")
    text_out.insert(INSERT, "+ 现在先点击清空结果！！！\n")
if __name__ == '__main__':
    style = Style(theme='yeti')
    root = style.master
    # root = Tk()
    root.wm_title('Fofa_Crawler')
    root.resizable()

    label_con = Label(root,text='查询条件')
    label_out = Label(root,text='查询结果')
    entry_con = Entry(root,width=50)
    text_out = Text(root)
    urlList = []
    query = Button(root,text='查询',width=7,command=startCrawl)
    clear = Button(root,text='清空结果',width=7,command=clearOutput)
    export = Button(root,text='导出结果',width=7,command=writeFile)

    label_con.grid(row=0,column=0,sticky=W)
    entry_con.grid(row=0,column=1,sticky=W)
    query.grid(row=0,column=2,sticky=W)
    clear.grid(row=0,column=3,sticky=W)
    export.grid(row=0,column=4,sticky=W)
    label_out.grid(row=1,column=0,sticky=W)
    text_out.grid(row=1,column=1,columnspan=4,sticky=W)

    init()
    root.mainloop()
