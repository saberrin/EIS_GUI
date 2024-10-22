import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 假设电池为10x10的方形区域，生成模拟温度数据（实际可以使用测量值）
battery_size = 10
x = np.arange(0, battery_size, 1)  # X轴坐标
y = np.arange(0, battery_size, 1)  # Y轴坐标
x, y = np.meshgrid(x, y)  # 创建网格
temperature_data = np.random.uniform(20, 70, (battery_size, battery_size))  # 模拟20-70度的温度分布

# 创建一个绘图窗口
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 使用 plot_surface 绘制三维表面
surf = ax.plot_surface(x, y, temperature_data, cmap='hot', edgecolor='none')

# 添加颜色条，显示温度与颜色的映射
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="Temperature (°C)")

# 设置标题和轴标签
ax.set_title("3D Temperature Map of Square Li-ion Battery")
ax.set_xlabel("X-axis (Position)")
ax.set_ylabel("Y-axis (Position)")
ax.set_zlabel("Temperature (°C)")

# 调整视角
ax.view_init(45, 135)  # 设置仰角和方位角

# 显示图像
plt.show()
