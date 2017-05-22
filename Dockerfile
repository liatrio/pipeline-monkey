# Uses the Python 3.5 runtime
FROM python:3.5.3-slim

# Sets the working directory to /pipeline-monkey
WORKDIR /pipeline-monkey

# Copies the current directory (this repo) in the container at /pipeline-monkey
ADD . /pipeline-monkey

# Installs any needed package specified in requirements.txt
RUN apt-get update
RUN apt-get install git -y
RUN pip install -r requirements.txt

# Define environment variables using the following template
# ENV NAME NAME

CMD ["python", "monkey.py"]
