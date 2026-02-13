import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def rbc_predict_1nn(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray) -> np.ndarray:
    preds = []
    for i in range(X_test.shape[0]):
        dists = np.linalg.norm(X_train - X_test[i], axis=1)
        idx = np.argmin(dists)
        preds.append(y_train[idx])
    return np.array(preds)

def main():
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    y_pred = rbc_predict_1nn(X_train, y_train, X_test)
    acc = accuracy_score(y_test, y_pred)
    print("=== RBC on Iris (1-NN, Euclidean) ===")
    print(f"Train size (past cases): {X_train.shape[0]}  |  Test size (new cases): {X_test.shape[0]}")
    print(f"Accuracy: {acc:.4f}")  # <-- print
    print("\nConfusion Matrix (rows=true, cols=pred):")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

if __name__ == "__main__":
    main()
