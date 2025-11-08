from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output,MODEL_VERSION,model

app = FastAPI()


#human readable
@app.get("/home")
def home():
    return( {'message': "Insurance premium prediction app"})

#machine readable
@app.get('/health')
def health_check():
    return{
        'status':'ok',        
        'model_loaded': model is not None,
        'version':MODEL_VERSION,
    }

@app.post("/predict",response_model=PredictionResponse)
def predict_premium(data:UserInput):

    user_input={ 'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
                },
    try:
         prediction=predict_output(user_input)
    except Exception as E:
        JSONResponse(status_code=500,content=str(E))

    return JSONResponse(
        status_code=200,
        content={
            "response": prediction
        }
    )



