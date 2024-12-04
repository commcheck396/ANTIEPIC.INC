import matplotlib.pyplot as plt

# 数据
years = [2011, 2012, 2013, 2014, 2015, 2016]
accuracy = [0.8464343598055105, 0.8435980551053485, 0.8476499189627229,
            0.8512965964343598, 0.8549432739059968, 0.853322528363047]

# 绘图
plt.figure(figsize=(8, 5))
plt.plot(years, accuracy, marker='o', linestyle='-', color='b', label='Accuracy')

# 设置标题和标签
plt.title('Model with time_weight', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)

# 显示数据点的值
for x, y in zip(years, accuracy):
    plt.text(x, y, f'{y:.4f}', ha='center', va='bottom', fontsize=10)

# 设置纵轴的范围，使图像更加集中在上半部分
plt.ylim(0.82, 0.86)  # 设定纵轴范围

# 添加网格和图例
plt.grid(alpha=0.5)
plt.legend()
plt.tight_layout()

# 显示图表
plt.show()
