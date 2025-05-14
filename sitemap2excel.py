import requests
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO
from tkinter import Tk, simpledialog, messagebox
import os

def get_sitemap_source():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    input_str = simpledialog.askstring("输入 sitemap 地址", "请输入 sitemap.xml 的网络链接或本地路径：")
    root.destroy()
    return input_str

def extract_urls(sitemap_input, output_excel):
    try:
        if sitemap_input.lower().startswith("http"):
            # 网络 sitemap
            response = requests.get(sitemap_input)
            response.raise_for_status()
            tree = ET.parse(BytesIO(response.content))
        else:
            # 本地文件
            if not os.path.isfile(sitemap_input):
                raise FileNotFoundError("本地文件不存在")
            tree = ET.parse(sitemap_input)

        root = tree.getroot()
        namespace = ''
        if '}' in root.tag:
            namespace = root.tag.split('}')[0] + '}'

        urls = [elem.text for elem in root.iter(namespace + 'loc')]
        df = pd.DataFrame(urls, columns=["URL"])
        df.to_excel(output_excel, index=False)

        messagebox.showinfo("成功", f"成功导出 {len(urls)} 条 URL 到 {output_excel}")
    except Exception as e:
        messagebox.showerror("错误", f"处理失败：{str(e)}")

if __name__ == "__main__":
    sitemap_input = get_sitemap_source()
    if sitemap_input:
        extract_urls(sitemap_input, "sitemap_urls.xlsx")
