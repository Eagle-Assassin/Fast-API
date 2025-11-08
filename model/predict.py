import pickle
import pandas as pd



#import the ml model
with open("model/model.pkl",'rb') as f:
    model= pickle.load(f)
MODEL_VERSION ='1.0.0' #usually comes from ML flow


def predict_output(data:dict):
        input_df=pd.DataFrame(data,index=range(0,1))
        print(input_df)
        prediction = model.predict(input_df)[0]
        probs = model.predict_proba(input_df)[0]
        class_prob_dict = dict(zip(model.classes_, probs))
        confidence = class_prob_dict[prediction]

        return{
                "predicted_category": prediction,
                "confidence": float(confidence),
                "class_probabilities": {k: float(v) for k, v in class_prob_dict.items()}
            }