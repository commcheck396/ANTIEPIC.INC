import matplotlib.pyplot as plt

# 超参数和准确率数据
funny_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
accuracies = [0.8934359805510534, 0.8881685575364667, 0.8857374392220422,
              0.8849270664505673, 0.8857374392220422, 0.8849270664505673,
              0.8893841166936791, 0.8861426256077796, 0.8897893030794165,
              0.8873581847649918]

# 创建图形
plt.figure(figsize=(8, 6))

# 绘制折线图
plt.plot(funny_values, accuracies, marker='o', linestyle='-', color='b', label='Accuracy')

# 添加标题和标签
plt.title('Model with helpful_funny_weight', fontsize=14)
plt.xlabel('Funny Hyperparameter', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)

# 设置纵轴的范围，使图像更加集中在上半部分
plt.ylim(0.87, 0.9)  # 设定纵轴范围

# 显示网格
plt.grid(True)

# 显示图例
plt.legend()

# 显示图表
plt.show()
