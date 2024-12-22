import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# 定义文件处理函数
def remove_specific_blocks(lines):
    pattern = re.compile(r'^\w+\(\d+\) \d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$')
    cq_pattern = re.compile(r'\[CQ:.*?\]')
    image_pattern = re.compile(r'\[图:.*?\]')  

    i = 0
    while i < len(lines):
        if pattern.match(lines[i]):
            j = i + 1
            has_cq_or_image = False
            while j < len(lines) and lines[j].strip() != '':
                if cq_pattern.search(lines[j]) or image_pattern.search(lines[j]):
                    has_cq_or_image = True
                    break
                j += 1

            if has_cq_or_image and j == i + 1:
                lines[i] = ''
                lines[j] = ''
                i = j + 1
            else:
                j = i + 1
                while j < len(lines) and lines[j].strip() != '':
                    if cq_pattern.search(lines[j]) or image_pattern.search(lines[j]):
                        lines[j] = ''
                    j += 1
                i = j
        else:
            i += 1

    return lines

def remove_remaining_cq_codes(lines):
    cq_pattern = re.compile(r'\[CQ:.*?\]')

    for i in range(len(lines)):
        if cq_pattern.search(lines[i]):
            lines[i] = ''

    return lines

def remove_isolated_lines(lines):
    pattern = re.compile(r'^\w+\(\d+\) \d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$')

    i = 0
    while i < len(lines):
        if pattern.match(lines[i]) and (i == 0 or lines[i - 1].strip() == '') and (i == len(lines) - 1 or lines[i + 1].strip() == ''):
            lines[i] = ''
        i += 1

    return lines

def remove_consecutive_blank_lines(lines):
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip() == '' and lines[i + 1].strip() == '':
            lines[i] = ''
        i += 1

    return lines

def process_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines = remove_specific_blocks(lines)
    lines = remove_remaining_cq_codes(lines)
    lines = remove_isolated_lines(lines)
    lines = remove_consecutive_blank_lines(lines)

    output_file = os.path.join(os.path.dirname(input_file), "跑团记录(最终处理).txt")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    return output_file

class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件处理器")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="选择文件进行处理：")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self.root, text="选择文件", command=self.select_file)
        self.select_button.pack(pady=5)

        self.process_button = tk.Button(self.root, text="处理文件", command=self.process_selected_file)
        self.process_button.pack(pady=5)

    def select_file(self):
        self.input_file = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("Text Files", "*.txt")]
        )
        if self.input_file:
            self.label.config(text=f"已选择文件: {self.input_file}")

    def process_selected_file(self):
        if hasattr(self, 'input_file') and self.input_file:
            try:
                output_file = process_file(self.input_file)
                messagebox.showinfo("处理完成", f"文件已处理并保存到:\n{output_file}")
            except Exception as e:
                messagebox.showerror("错误", f"处理文件时出错：\n{e}")
        else:
            messagebox.showerror("错误", "未选择文件")

# 运行应用程序
if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessorApp(root)
    root.mainloop()