from time import time
import numpy as np
import pylab as pl

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

def load_contexts(filename):
    """
    Devuelve lista de contexts.
    """
    ctxt = []
    words = []
    f = open(filename, "r")
    lines = f.read().splitlines()
    for line in lines:
        aux = [np.float32(elem) for elem in line.split()[1:]]
        aux1 = np.array(aux, dtype=np.float32)
        ctxt.append(aux1)
        words.append(line.split()[0])
    return words, np.array(ctxt)
print "Cargando Archivo"
labels, data = load_contexts('resultados_clusters_con_indices.dat')
print "Finalizado Cargado de Archivo"
n_samples, n_features = data.shape

n_digits = len(np.unique(labels))


sample_size = 300

print("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_digits, n_samples, n_features))


print(79 * '_')
print('% 9s' % 'init'
      '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette')


def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('% 9s   %.2fs     %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             #metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
#             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

bench_k_means(KMeans(n_digits, init='k-means++', n_init=10),
              name="k-means++", data=data)

#bench_k_means(KMeans(n_digits, init='random', n_init=10),
#              name="random", data=data)

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
#pca = PCA(n_components=n_digits).fit(data)
#bench_k_means(KMeans(n_digits, init=pca.components_, n_init=1),
#              name="PCA-based",
#              data=data)
print(79 * '_')

###############################################################################
# Visualize the results on PCA-reduced data

#reduced_data = PCA(n_components=2).fit_transform(data)
#kmeans = KMeans(n_digits, init='k-means++', n_init=10)
#kmeans.fit(reduced_data)

## Step size of the mesh. Decrease to increase the quality of the VQ.
#h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

## Plot the decision boundary. For that, we will assign a color to each
#x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
#y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
#xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

## Obtain labels for each point in mesh. Use last trained model.
#Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

## Put the result into a color plot
#Z = Z.reshape(xx.shape)
#pl.figure(1)
#pl.clf()
#pl.imshow(Z, interpolation='nearest',
#          extent=(xx.min(), xx.max(), yy.min(), yy.max()),
#          cmap=pl.cm.Paired,
#          aspect='auto', origin='lower')

#pl.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
## Plot the centroids as a white X
#centroids = kmeans.cluster_centers_
#pl.scatter(centroids[:, 0], centroids[:, 1],
#           marker='x', s=169, linewidths=3,
#           color='w', zorder=10)
#pl.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
#         'Centroids are marked with white cross')
#pl.xlim(x_min, x_max)
#pl.ylim(y_min, y_max)
#pl.xticks(())
#pl.yticks(())
#pl.show()
