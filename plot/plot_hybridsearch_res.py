import json

import numpy as np
import matplotlib.pyplot as plt

with open("../res/hybridsearch_ls_res.json", "r") as file:
    data1 = json.load(file)
with open("../res/hybridsearch_gt_res.json", "r") as file:
    data2 = json.load(file)
# x轴刻度标签
x_ticks = []
for i in range(10, 231, 10):
    x_ticks.append(i)

# x轴范围（0, 1, ..., len(x_ticks)-1）
x = np.arange(len(x_ticks))
# 第1条折线数据
y1 = []
for i in x_ticks:
    y1.append(data1[str(i)])

y2 = []
for i in x_ticks:
    y2.append(data2[str(i)])

# 设置画布大小
plt.figure(figsize=(20, 6))
# 画第1条折线，参数看名字就懂，还可以自定义数据点样式等等。
plt.plot(x, y1, color='#FF0000', label='entry_text_len < ', linewidth=3.0)
plt.plot(x, y2, color='#00FF00', label='entry_text_len > ', linewidth=3.0)

# 给第1条折线数据点加上数值，前两个参数是坐标，第三个是数值，ha和va分别是水平和垂直位置（数据点相对数值）。
for a, b in zip(x, y1):
    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=8)
for a, b in zip(x, y2):
    plt.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=8)
# 添加x轴和y轴刻度标签
plt.xticks([r for r in x], x_ticks, fontsize=18, rotation=20)
plt.yticks(fontsize=18)
# 添加x轴和y轴标签
plt.xlabel(u'threshold', fontsize=18)
plt.ylabel(u'hybridsearch time cost', fontsize=18)
# 标题
plt.title(u'hybridsearch time cost with different threshold', fontsize=18)
# 图例
plt.legend(fontsize=18)
# 保存图片
plt.savefig('./hybridsearch_lt_and_gt_res_figure.png', bbox_inches='tight')
# 显示图片
plt.show()
