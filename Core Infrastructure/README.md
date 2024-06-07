
# Test the application

### Test Locally
To start the HTTP server, in Cloud Shell, run the following command:
```bash 
cd ~/bookshelf; ~/.local/bin/gunicorn -b :8080 main:app
```

### Test Externally
To start the HTTP server, in Cloud Shell, run the following command:

```bash 
cd ~/bookshelf; EXTERNAL_HOST_URL="https://8080-$WEB_HOST" ~/.local/bin/gunicorn -b :8080 main:app
```

There is an environment variable being passed in to the application:

- **EXTERNAL_HOST_URL** specifies the scheme and hostname that should be used in the callback URL. If this environment variable is not specified, the redirect_uri passed to Google in the authorization URL will use the hostname that the application sees in incoming URLs: 127.0.0.1:8080, which is localhost. Web Preview forwards requests from the cloudshell.dev URL to localhost (http://127.0.0.1:8080).
