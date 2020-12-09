FROM python:3.7-alpine

# Prepare the app
RUN mkdir /code/
WORKDIR /code/

# Install PipEnv
RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install requirements
RUN pipenv install --deploy --system
# Copy all source code
COPY . .
CMD ["python", "/code/app.py"]
