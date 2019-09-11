import pandas as pd
import ast
import os
def D2S(ROOT_DIR,disease):
    data = pd.read_csv(os.path.join(ROOT_DIR,'datasets/preprocessed/ds.csv'))
    try:
        symptoms=data[data.Disease==disease].head(1).Symptom.item()
        symptoms=ast.literal_eval(symptoms)
        temp=','.join(symptoms[:-1])
        temp+=(" and "+symptoms[-1])
        return "Possible symptoms of "+disease+" include "+temp
    except ValueError:
        return None
