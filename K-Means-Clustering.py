import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd

class KMeans():
    def __int__(self, k, max_iteration=10):
        self.k = k
        self.max_iteration = max_iteration
        self.all_centroids = []
        self.all_labels = []

    # Hàm tạo thuật toán k-Means lấy đầu vào là một bọo dữ liệu và số lượng cluster k. Trả về tâm của k cụm
    def fit(self, dataSet):
        # Khoi tao k tam cum
        numFeatures = dataSet.shape[1]      # lay ra so cot cua dataFarme
        centroids = self.get_random_centroids(numFeatures, self.k)
        self.all_centroids.append(centroids)
        self.all_labels.append(None)

        # Khởi tạo các biến iterations, oldCentroids
        iterations = 0
        oldCentroids = None

        # Vòng lặp cập nhật centroids trong thuật toán k-Means
        while not self.should_stop(oldCentroids, centroids, iterations):
            # Lưu lại centroids cũ cho quá trình kiểm tra hội tụ
            oldCentroids = centroids
            iterations += 1

            # Gán nhãn cho mỗi diểm dữ liệu dựa vào centroids
            labels = self.get_labels(dataSet, centroids)
            self.all_labels.append(labels)

            # Cập nhật centroids dựa vào nhãn dữ liệu
            # print('0ld centroids: ', centroids)
            centroids = self.get_centroids(dataSet, labels, self.k)
            # print('new centroids: ', centroids)
            self.all_centroids.append(centroids)

        return centroids

    # Hàm khởi tạo centroids ngẫu nhiên
    def get_random_centroids(self, numFeatures, k):
        return np.random.rand(k, numFeatures)

    # Hàm này trả về nhãn cho mỗi điểm dữ liệu trong datasets
    def get_labels(self, dataSet, centroids):
        # Với mỗi quan sát trong dataset, lựa chọn centroids gần nhất để gán label cho dữ liệu.
        labels = []
        for x in dataSet:
            # Tính khoảng cách tới các centroids và cập nhận nhãn
            distances = np.sum((x - centroids) ** 2, axis=1)
            label = np.argmin(distances)
            labels.append(label)
        return labels

    # Hàm này trả về True hoặc False nếu k-Means hoàn thành. Điều kiện k-Means hoàn thành là
    # thuật toán vượt ngưỡng số lượng vòng lặp hoặc centroids ngừng thay đổi
    def should_stop(self, oldCentroids, centroids, iterations):
        if iterations > self.max_iteration:
            return True
        return np.all(oldCentroids == centroids)

    # Trả về toan độ mới cho k centroids của mỗi chiều.
    def get_centroids(self, dataSet, labels, k):
        centroids = []
        for j in np.arange(k):
            # Lấy index cho mỗi centroids
            idx_j = np.where(np.array(labels) == j)[0]
            centroid_j = dataSet[idx_j, :].mean(axis=0)
            centroids.append(centroid_j)
        return np.array(centroids)

dataset, _ = make_blobs(n_samples=250, cluster_std=3.0, random_state=123)
kmean = KMeans()
kmean.k = 3
kmean.max_iteration = 15
kmean.all_centroids = []
kmean.all_labels = []
centroids = kmean.fit(dataset)

gs = GridSpec(nrows=3, ncols=3)
plt.figure(figsize=(20, 20))
plt.subplots_adjust(wspace=0.2, hspace=0.4)
colors = ['green', 'blue', 'red']
labels = ['cluster 1', 'cluster 2', 'cluster 3']

# Lấy centroids và labels tại bước thứ i
i = 4
centroids_i = kmean.all_centroids[i]
labels_i = kmean.all_labels[i]

j = 0
idx_j = np.where(np.array(labels_i) == j)[0]
plt.scatter(dataset[idx_j, 0], dataset[idx_j, 1], color=colors[j], label=labels[j], s=50, alpha=0.3, lw=0)
plt.scatter(centroids_i[j, 0], centroids_i[j, 1], marker='x', color=colors[j], s=100, label=labels[j])

for i in np.arange(len(kmean.all_centroids)):
  ax = plt.subplot(gs[i])
  if i == 0:
    centroids_i = kmean.all_centroids[i]
    plt.scatter(dataset[:, 0], dataset[:, 1], s=50, alpha=0.5, color='red')
    for j in np.arange(kmean.k):
      plt.scatter(centroids_i[j, 0], centroids_i[j, 1], marker='x', s=100, color='red')
    plt.title('All points in original dataset')
    plt.show()
  else:
    # Lấy centroids và labels tại bước thứ i
    centroids_i = kmean.all_centroids[i]
    labels_i = kmean.all_labels[i]
    # Visualize các điểm cho từng cụm
    for j in np.arange(kmean.k):
      idx_j = np.where(np.array(labels_i) == j)[0]
      plt.scatter(dataset[idx_j, 0], dataset[idx_j, 1], color=colors[j], label=labels[j], s=50, alpha=0.3, lw = 0)
      plt.scatter(centroids_i[j, 0], centroids_i[j, 1], marker='x', color=colors[j], s=100, label=labels[j])
    plt.title(r'iteration {}'.format(i))
    plt.show()


a = float(input("x: "))
b = float(input("y: "))
x = np.array([a, b])

is_in_array = np.all(np.equal(dataset, x).all(axis=1))
if is_in_array:

    indices = np.where((dataset == x).all(axis=1))
    first_index = indices[0][0]
    dodai = len(kmean.all_labels)
    print("[{}, {}] thuoc cum {}." .format(a, b, kmean.all_labels[dodai-1][first_index]))
else:
    dataset = np.vstack([dataset, x])
    kmean = KMeans()
    kmean.k = 3
    kmean.max_iteration = 15
    kmean.all_centroids = []
    kmean.all_labels = []
    centroids = kmean.fit(dataset)

    dodai = len(kmean.all_labels)-1
    dodai2 = len(dataset)-1
    print("[{}, {}] thuoc cum {}.".format(a, b, kmean.all_labels[dodai][dodai2]))

dataset, _ = make_blobs(n_samples=250, cluster_std=3.0, random_state=123)
dataset = pd.DataFrame(data=dataset, columns=["Feature_1", "Feature_2"])

dataset.to_csv('C:\\GR1\\data.csv', index=False, mode='w')
