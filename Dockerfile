FROM tensorflow/tensorflow:2.13.0

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# app code
COPY api ./api
COPY streamlit_OG ./streamlit_OG
COPY model ./model
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
EXPOSE 8501

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
