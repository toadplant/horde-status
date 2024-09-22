import streamlit as st # type: ignore
import requests as rq
import pandas as pd
import json

st.title('Horde status')

def get_awailable_models():
    workers_url = 'https://aihorde.net/api/v2/workers?type=text'
    workers = pd.json_normalize(rq.get(workers_url).json())
    workers = workers.rename(columns={"name": "worker", "models": "model"})
    workers['model'] = workers['model'].apply(lambda m: m[0])
    models_url = 'https://aihorde.net/api/v2/status/models?type=text&model_state=all'
    models = pd.json_normalize(rq.get(models_url).json())
    models = models.rename(columns={"name": "model"})
    awailable_models = workers.merge(models, on='model')
    awailable_models = awailable_models[['model', 'eta', 'performance_y', 'worker', 'max_length', 'max_context_length']]
    awailable_models['model'] = awailable_models['model'].apply(lambda m: m.split('/')[-1])
    return awailable_models

awailable_models = get_awailable_models()
st.dataframe(awailable_models,
             hide_index=True,
              column_config={
              "model": st.column_config.TextColumn("Models"),
              "eta": st.column_config.ProgressColumn("Wait Rate",
                                                      format="%d sec"),
              "performance_y": st.column_config.NumberColumn("Speed",
                                                             format="%d tok/sec"),
              "worker": st.column_config.TextColumn("Workers"),
              "max_length": st.column_config.NumberColumn("Max response",
                                                             format="%d tokens"),
              "max_context_length": st.column_config.NumberColumn("Max context",
                                                             format="%d tokens")})