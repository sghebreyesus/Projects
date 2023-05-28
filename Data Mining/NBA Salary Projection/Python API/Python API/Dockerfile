FROM python:3.8.12

# switch working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
#COPY . /app

EXPOSE 7373

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
