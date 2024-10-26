import os
import tkinter as tk
from tkinter import filedialog

size = input("请输入要分割的文件大小（以MB为单位）：")

def split_file(file_path, chunk_size=size * 1024 * 1024):
    try:
        chunk_size = int(chunk_size)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = os.path.dirname(file_path)

        with open(file_path, 'rb') as file:
            part = 1
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                try:
                    # 将二进制数据解码为UTF-8字符串
                    text = chunk.decode('utf-8')
                except UnicodeDecodeError:
                    # 如果解码失败，尝试找到有效的UTF-8边界
                    for i in range(len(chunk) - 1, -1, -1):
                        try:
                            text = chunk[:i].decode('utf-8')
                            file.seek(file.tell() - (len(chunk) - i))  # 将文件指针移回
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        raise ValueError("无法将文件内容解码为UTF-8")

                output_file = os.path.join(output_dir, f"{base_name}_part{part}.txt")
                with open(output_file, 'w', encoding='utf-8') as out_file:
                    out_file.write(text)
                part += 1

        print(f"文件已成功分割为{part - 1}个部分！")
    except Exception as e:
        print(f"发生错误：{str(e)}")


def select_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口，只显示文件选择对话框

    file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
    if file_path:
        split_file(file_path)


if __name__ == "__main__":
    select_file()