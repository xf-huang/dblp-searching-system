# dblp文献匹配与导出系统

## 功能描述
用网络请求的方法获取https://dblp.org/网站返回的HTML文件或其他数据，解析返回的数据，获取BibTeX格式参考文献的文本数据，利用python文件操作的方法实现bib和txt格式的文件导出功能和批量导入导出功能，利用正则表达式匹配和python中str对象的方法实现选择导出条目、更改原始BixTeX文本和多个结果重要性排序的功能，利用python的tkinter库实现GUI界面。

## 使用方法
1.关键词搜索
![image](https://user-images.githubusercontent.com/54733565/195307440-e0b177e9-7b45-4445-9679-a040b2439ced.png)
2.论文标题搜索
![image](https://user-images.githubusercontent.com/54733565/195307656-08cad318-3af1-4f1b-a738-73f0db7d75e7.png)
3.批量导入搜索
![image](https://user-images.githubusercontent.com/54733565/195307842-4004aeaf-ae55-459e-964a-a17556d0cc5e.png)
![image](https://user-images.githubusercontent.com/54733565/195307883-e1df0d9b-55f6-4683-8af5-f5b093b92580.png)
点击“选择文件”按钮，弹出选择文件对话框，选择想要导入的文本文件（文本的格式需按图3-4所示的格式，每个搜索语句占一行，论文标题需要在前面加上‘#’），点击确定，“批量导入”输入框中即出现文件的路径，也可以直接在输入框中输入文件的路径。点击“开始搜索”按钮，等待程序响应后即可在文本框中看到每行关键词和论文标题的搜索结果。
4.选择导出条目
![image](https://user-images.githubusercontent.com/54733565/195308054-b0b5ef6f-793e-4057-a770-d7a25f6ab1d3.png)
以上搜索方法都可选择导出条目，只需在“导入条目”输入框中输入所要导出的条目（条目之间用空格分开）
5.导出文件
搜索完成后，可以将文本框中的搜索结果导出，点击单选按钮选择需要导出的文件格式，点击“导出文件”按钮，弹出保存文件对话框，在对话框中选择文件的保存路径，点击“保存”，即可将搜索结果保存到本地文件。
