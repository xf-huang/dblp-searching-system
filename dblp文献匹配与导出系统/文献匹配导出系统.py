# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:56:43 2022

@author: Administrator
"""
# 引入相关的库
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import re


# GUI界面窗口设置
window = tk.Tk()
window.title("文献匹配导出系统")
window.geometry("600x800")
window["background"] = "#00FF00"
# 标签和输入框
label_keywords = tk.Label(window, text="搜索关键词:", font=('Times',10), bg="#00FF00")
label_keywords.grid(row=0, column=0, padx=5, pady=5)

entry_keywords = tk.Entry(window, width=40)
entry_keywords.grid(row=0,column=1, padx=5, pady=5)


label_title = tk.Label(window, text="论文题目:", font=('Times',10), bg="#00FF00")
label_title.grid(row=1, column=0, padx=5, pady=5)

entry_title = tk.Entry(window, width=40)
entry_title.grid(row=1,column=1, padx=5, pady=5)


label_import = tk.Label(window, text="批量导入:", font=('Times',10), bg="#00FF00")
label_import.grid(row=2, column=0, padx=5, pady=5)

entry_import = tk.Entry(window, width=40)
entry_import.grid(row=2, column=1, padx=5, pady=5)





def url(search_str):
    '''
    根据用户输入的关键词或论文题目，构造查询的url.

    Parameters
    ----------
    search_str : string
        用户输入的关键词或论文题目.

    Returns
    -------
    url_results: string
        查询结果的url
    url_bib: string
        获取bib文档的url

    '''
    str_list = search_str.split() # 将输入的字符串拆成单词组成的列表
    argument = "%20".join(str_list) # 用'%20'连接单词组成新的字符串
    url_bib = "https://dblp.org/search/publ/bibtex?q=" + argument # 构造获取bib文档的url
    
    return url_bib
    

def open_file():
    '''
    “选择文件”按钮的响应函数

    Returns
    -------
    None.

    '''
    # 从本地选择一个文件，并返回文件的路径
    file_path = filedialog.askopenfilename()
    if file_path != '':
        entry_import.delete(0, tk.END) # 删除输入框中已有的内容
        entry_import.insert(0, file_path) # 将选择的文件路径插入到输入框中
    else:
        messagebox.showerror(title="错误", message="您没有选择任何文件") # 如果没有选择任何文件，弹出错误信息

# 导入文件按钮
button_import = tk.Button(window, text="选择\n文件", font=('Times',10), bd=3, bg="#EF1241", command=open_file)
button_import.grid(row=2, column=2, padx=5, pady=5)

label_filt = tk.Label(window, text="导出条目:", font=('Times',10), bg="#00FF00")
label_filt.grid(row=3, column=0, padx=5, pady=5)

entry_filt = tk.Entry(window, width=40)
entry_filt.grid(row=3, column=1, padx=5, pady=5)


label_format = tk.Label(window, text="保存格式:", font=('Times',10), bg="#00FF00")
label_format.grid(row=4, column=0, padx=5, pady=5)

v = tk.StringVar()

# 单选按钮
radio_button1 = tk.Radiobutton(window, text="bib", variable=v, value="bib")
radio_button1.grid(row=4, column=1, sticky='w')
radio_button2 = tk.Radiobutton(window, text="txt", variable=v, value="txt")
radio_button2.grid(row=4, column=1)

def filt_fields(bibtxt, fields_list):
    '''
    选择bib的导出条目

    Parameters
    ----------
    bibtxt : string
        bib文本
    fields_list : list
        导出条目的列表

    Returns
    -------
    bib_filt : string
        导出条目组成的bib文本

    '''
    # 构造筛选bib条目的正则表达式
    pattern = '(\n@.*?\n).*?'
    for item in fields_list:
        if item != 'bibsource':
            pattern += '(' + item + '\s+= {.*?},\n).*?'
        else:
            pattern += '( bibsource.*?\n}\n)'
    #匹配bib文本，并用join方法组成新的bib文本
    r = re.compile(pattern, re.S) 
    result = r.match(bibtxt)
    s = result.groups()
    bib_filt = '  '.join(s)
    
    return bib_filt     

def bib_alter(bib_text):
    '''
    修改BibTeX的内容

    Parameters
    ----------
    bib_text : string
        原始bib

    Returns
    -------
    bib_text : string
        修改后的bib

    '''
    if bib_text.startswith("\n@inproceedings"):
        pattern1 = r'booktitle = {(.+?),'
        r1 = re.compile(pattern1, re.S)
        con_name = r1.search(bib_text).group(1)
        pattern2 = r'(booktitle.+?},\n)'
        r2 = re.compile(pattern2, re.S)
        bktt_old = r2.search(bib_text).group(1)
        bktt_new = "booktitle = {Proceedings of the " + con_name + "},\n"
        bib_text = bib_text.replace(bktt_old, bktt_new)
    if bib_text.startswith("\n@article"):
        pattern3 = r'volume    = {(\d+)},'
        r3 = re.compile(pattern3, re.S)
        volume = r3.search(bib_text).group(1)
        pattern4 = r'  (journal.+?},\n)'
        r4 = re.compile(pattern4, re.S)
        journal_old = r4.search(bib_text).group(1)
        journal_new = "journal   = {arXiv preprint arXiv:" + volume + "},\n"
        bib_text = bib_text.replace(journal_old, journal_new)
    return bib_text
    
    
    
def search_kw(keywords):
    '''
    关键词搜索
    Parameters
    ----------
    keywords: string
        搜索的关键词

    Returns
    -------
    bib_text : string
        根据条件返回相应的bib文本.

    '''
    #调用url()函数返回相应的url
    
    url_bib = url(keywords)
    # 获取url的响应内容并解析
    
    r = requests.get(url_bib)
    soup = BeautifulSoup(r.text, "html.parser")
    
    bib_text = ''
    # 判断“选择条目”输入框是否为空，并返回相应的bib文本
    fields = entry_filt.get()
    if fields != '':
        for item in soup.find_all("pre")[:10]:
            item_text = item.get_text()
            item_text = bib_alter(item_text)
            try:
                item_filt = filt_fields(item_text, fields.split())
                bib_text += item_filt
            except:
                continue
    else:
        for item in soup.find_all("pre")[:10]:
            item_text = item.get_text()
            item_text = bib_alter(item_text)
            bib_text += item_text       
    # 将前20个搜索结果显示在文本框
    text.insert(tk.INSERT, bib_text)
    return bib_text

# 论文题目搜索函数
def search_tt(title):
    #调用url()函数返回相应的url 
    url_bib = url(title)
    # 获取url的响应内容并解析
    r = requests.get(url_bib)
    soup = BeautifulSoup(r.text, "html.parser")
    
    bib_text = ""
    # 判断论文题目是否对应多个结果，并返回相应的bib文本
    items = soup.find_all("pre")
    # 如果结果大于一个，则按期刊>会议>arxiv>其他，输出最重要的一项。
    if len(items) > 1:
        for item in items:
            item_text = item.get_text()
            # 如果bib文本以"\n@article"开头，则将其保存到变量article中，下同
            if item_text.startswith("\n@article"):
                article = item_text
            elif item_text.startswith("\n@inproceedings"):
                inpro = item_text
            elif item_text.startswith("\n@arxiv"):
                arxiv = item_text
            else:
                other = item_text
        # 如果article变量非空，则令bib_text=article，下同
        if article:
            bib_text = article
        elif inpro:
            bib_text = inpro
        elif arxiv:
            bib_text = arxiv
        else:
            bib_text = other
    else:
        bib_text = items[0].get_text()
        bib_text = bib_alter(bib_text)
    # 判断“选择条目”输入框是否为空，并返回相应的bib文本
    fields = entry_filt.get()
    if fields != '':
        item_filt = filt_fields(bib_text, fields.split())
        bib_text = item_filt
    # 将搜索结果显示在文本框
    text.insert(tk.INSERT, bib_text)
    return bib_text

# 批量搜索函数
def multi_search():

    bib_text = ""
    # 打开文件
    filepath = entry_import.get()
    with open(filepath) as f:
        lines = f.readlines() # 读取文件中的行
        for item in lines:
            if item.startswith('#'):
                title = item.strip('#').strip('\n')
                text.insert(tk.INSERT, title+':'+'\n\n')
                item_bib = search_tt(title)
                bib_text += item_bib
            else:
                key_words = item.strip('\n')
                text.insert(tk.INSERT, key_words+':'+'\n\n')
                item_bib = search_kw(key_words)
                bib_text += item_bib    
 
    return bib_text

# 总的搜索函数
def search():
    filepath = entry_import.get()
    keywords = entry_keywords.get()
    title = entry_title.get()

    if filepath != '':
        multi_search()
    elif keywords != '':
        search_kw(keywords=keywords)
    else:
        search_tt(title=title)
    
       
# “开始搜索”按钮   
button_search = tk.Button(window, text="开始\n检索", font=('Times',10), bd=10, bg="#47E2A1", command=search)
button_search.grid(row=4, column=1, padx=5, pady=5, sticky='e')

# 导出文件的函数
def save():
    save_format = v.get()
    if save_format == 'txt':
        filenewpath = filedialog.asksaveasfilename(title='保存文件',
                                                defaultextension='.txt',
                                                initialdir='C:/Users/Administrator/Desktop' )
    else:
        filenewpath = filedialog.asksaveasfilename(title='保存文件',
                                                defaultextension='.bib',
                                                initialdir='C:/Users/Administrator/Desktop' )
    bib_text = text.get("1.0", tk.END)
    with open(filenewpath, 'w') as f:
        f.write(bib_text)

# “导出文件”按钮
button_export = tk.Button(window, text="导出\n文件", font=('Times',10), bd=10, bg="#47E2A1", command=save)
button_export.grid(row=4, column=2, padx=5, pady=5)

# 文本框
text = tk.Text(window, width=60, height=50, undo=True, autoseparators=False, wrap='word')
text.grid(row=5, column=1, columnspan=3)

window.mainloop()