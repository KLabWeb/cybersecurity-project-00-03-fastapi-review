# FastAPI over Uvicorn Docker image

# Specify base image to extend  & app dir
FROM python:3.14-slim
WORKDIR /usr/local/app

 # Install py dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy in source code & legacy data store to container, then expose app port
# data/sqlite is not copied - the DB file is supplied at runtime by the compose volume
COPY src ./src
COPY data/legacy ./data/legacy
# pytest.ini supplies pythonpath and testpaths, so the suite runs inside the container too
COPY pytest.ini ./
EXPOSE 8080

# Put the app root on the import path so the data layer resolves as data.legacy.*
# uvicorn's --app-dir only covers src, which leaves data/ unreachable
ENV PYTHONPATH=/usr/local/app

# Set default command to start univorn server when container starts
# Plus look for app.main for app to serve, set default interface, and set listening port
CMD ["uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080"]