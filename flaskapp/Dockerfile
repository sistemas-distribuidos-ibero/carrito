FROM python:3-alpine
 
# Create app directory
WORKDIR /app
 
# Install app dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
 
# Bundle app source
COPY . .
 
EXPOSE 5000

CMD [ "python", "app.py"]