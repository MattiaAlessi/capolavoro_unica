import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

if not pd.io.common.file_exists('dataset.csv'): #guardo se esiste dataset
    exit()

df = pd.read_csv('dataset.csv') #leggo dataset


# X sono le coordinate 
# y è l'etichetta (sasso,carta,forbice)
X = df.drop('label', axis=1)
y = df['label']

# training set (80%) e test set (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC(kernel='rbf', probability=True))
])


print("Addestramento")
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print(f"Accuratezza: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nReport di classificazione:")
print(classification_report(y_test, y_pred))


with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modello salvato")