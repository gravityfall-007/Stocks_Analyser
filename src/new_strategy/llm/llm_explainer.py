from groq import Groq


class ForecastExplainer:
    def __init__(self, api_key):
    self.client = Groq(api_key=api_key)


    def explain(self, model_name, metrics, horizon):
        prompt = f"""
        You are a financial analyst.


        Model used: {model_name}
        Forecast horizon: {horizon} days
        MAE: {metrics['avg_mae']:.4f}
        RMSE: {metrics['avg_rmse']:.4f}


        Explain:
        - Model behavior
        - Reliability of forecast
        - Risk level
        - When this model may fail"""


        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )


return response.choices[0].message.content