from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
iris.keys()

print('Target names: \n  {} ' .format(iris.target_names))
print('\n Features: \n {}'.format(iris.feature_names))

# Train set a Test
X_train, X_test, y_train, y_test = train_test_split(iris['data'],
                                                    iris['target'],
                                                    random_state=4)
# KNN

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# New array to test
X_new = [[1, 2, 1, 4],
         [2, 3, 4, 5]]

prediction = knn.predict(X_new)

print("\nNew array: \n {}"
      "\n\nTarget Names Prediction: \n {}" .format(X_new,
                                                   iris['target_names'][prediction]))
