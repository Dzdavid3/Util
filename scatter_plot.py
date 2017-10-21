import matplotlib.pyplot as plt

x = [2,4,6,5,8,10,12]
y = [6,7,8,5,2,4,6]


plt.scatter(x,y, label="SCAT", color="k", marker="^", s=15)


plt.xlabel("Time")
plt.ylabel("Prices")
plt.title("Stock Data \n8/31/2017")

plt.legend()
plt.show()