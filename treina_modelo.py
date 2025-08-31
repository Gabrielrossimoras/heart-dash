# -*- coding: utf-8 -*-
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib

# Importa os dados
heart_disease = fetch_ucirepo(id=45)
dados = heart_disease.data.features

# Acrescenta coluna binária 'doenca'
dados['doenca'] = 1 * (heart_disease.data.targets > 0)

# Separa preditores (X) e alvo (y)
X = dados.drop(columns='doenca')
y = dados['doenca']

# Divide em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Cria e treina modelo XGBoost
modelo = xgb.XGBClassifier(objective='binary:logistic')
modelo.fit(X_train, y_train)

# Avalia
preds = modelo.predict(X_test)
acuracia = accuracy_score(y_test, preds)
print(f"Acurácia: {acuracia:.2%}")

# Salva modelo e medianas
joblib.dump(modelo, "modelo_xgboost.pkl")
joblib.dump(X.median(), "medianas.pkl")

