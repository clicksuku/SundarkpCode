FROM agrigorev/zoomcamp-model:2025

# Install pipenv
RUN pip install pipenv

# Set the working directory inside the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
# --deploy ensures the lockfile is up-to-date and prevents automatic updates
# --system installs packages directly into the system Python distribution
RUN pipenv install --deploy --system


COPY pipeline_v1.bin /app/pipeline_v1.bin
COPY model_serve.py /app/model_serve.py
COPY lead.py /app/lead.py

CMD ["uvicorn", "model_serve:app", "--reload"]
