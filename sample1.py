import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

#生成模拟数据
np.random.seed(0)

x = np.random.rand(100, 1)*10 - 5
y = 0.5*x**2 + x + 2 + np.random.randn(100, 1)

#print (x)
#print (y)

#多项式回归：将数据转换为多项式
poly_features = PolynomialFeatures(degree=2, include_bias=False)
x_poly = poly_features.fit_transform(x)

#训练模型
lin_reg = LinearRegression()
lin_reg.fit(x_poly, y)

#获取模型参数
b0, b1, b2 = lin_reg.intercept_[0], lin_reg.coef_[0][0], lin_reg.coef_[0][1]
print(f"模型参数：b0 = {b0}, b1 = {b1}, b2 = {b2}")


#绘制多项式回归拟合结果
x_new = np.linspace(-5, 5, 100).reshape(100, 1)
x_new_poly = poly_features.transform(x_new)
y_new = lin_reg.predict(x_new_poly)

plt.scatter(x, y, color = 'blue', label = 'Data points')
plt.plot(x_new, y_new, color = 'red', label = 'Polynomial Regression Fit')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polynomial Regression Example')
plt.legend()
plt.show()