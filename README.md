# Primaa API image processing

It is a python API that trigger jobs for image processing. Jobs status and id are stored in a non-persistent database (python Class).

## Functionality

- Start a FastAPI server
- Submit a job
- Get job status, result and error

## Installation and usage

This application is written in Python. As said, the storage is non-persistent for this technical test, essentially because I constrain myself to not go beyond 4h45.

>I anticiapte a lot of discussion around this storage point (Thought about Redis, or even a RDBMS). very exciting topic.

### Installation

First check that Docker is installed in your system.

Once done you can clone or download the repository. Once in the root directory of the application run the following command:

```bash
docker build -t primaa/api .
```

This will build the image

Next you can run the following command:

```bash
docker run --rm -p 8000:8000 primaa/api
```

You should see this output:

```text
warning: Ignoring existing virtual environment linked to non-existent Python interpreter: .venv/bin/python3 -> python
Using CPython 3.10.18 interpreter at: /usr/local/bin/python3
Removed virtual environment at: .venv
Creating virtual environment at: .venv
Downloading virtualenv (5.7MiB)
Downloading ruff (11.9MiB)
 Downloading virtualenv
 Downloading ruff
Installed 61 packages in 943ms

   FastAPI   Starting development server 🚀

             Searching for package file structure from directories with
             __init__.py files
             Importing from /app

    module   🐍 main.py

      code   Importing the FastAPI app object from the module with the following
             code:

             from main import app

       app   Using import string: main:app

    server   Server started at http://0.0.0.0:8000
    server   Documentation at http://0.0.0.0:8000/docs

       tip   Running in development mode, for production use: fastapi run

             Logs:

      INFO   Will watch for changes in these directories: ['/app']
      INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
      INFO   Started reloader process [45] using WatchFiles
      INFO   Started server process [54]
      INFO   Waiting for application startup.
      INFO   Application startup complete.
```

## Usage

Now you can query the differnet endpoints. Two solutions:

- You can use your own app like Postman. I personally use [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) from VS Code. If you have the extension in your VS Code you can use the files in `tests/http_manual_testing`.
- You can just curl from the terminal. A typical sequence could look like:

```bash
# get inexisting job
curl http://localhost:8000/status/fake

# submit job
curl -X POST http://localhost:8000/job-submission \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg","callback_url":"https://webhook.site/6369a6fc-9575-409e-becf-e2237953c8ef","callback_token":"a1b2c3d4-e5f6-7890-1234-567890abcdef","algorithm_name":"poi_detection"}'

# This should return something like
{"code":200,"job_id":"88cf3e0e-9df3-4e2a-9638-72660958344f","status":"Pending","error":null}

#Collect the job id and get its status
curl http://localhost:8000/status/88cf3e0e-9df3-4e2a-9638-72660958344f

# this should return
{"code":200,"job_id":"88cf3e0e-9df3-4e2a-9638-72660958344f","status":"Completed","error":null}
```

>Note: I use the [webhook site](https://webhook.site/#!/view/6369a6fc-9575-409e-becf-e2237953c8ef/a1d1dd9c-2ce7-488d-9179-0581ad96a24f/1) service to check that everything works. So set the `callback_url` so that it matches your own webhook url.

## For developers

If you want to contribute. Ensure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed. Once done clone the repository adn run:

```bash
uv sync
```

It should install all dependencies and create a virtual envrionment. Activate it with:

```bash
source .venv/bin/activate
```

Now you can execute the server with:

```bash
fastapi dev main.py
```

You can then play with the app as described for the docker installation

To run the test. I encourage you to install [Task](https://taskfile.dev/), a really cool replacement of the `Makefile`. Once installed run:

```bash
task test
```

If you do not want to install `Task` just run:

```bash
uv run python -m coverage erase && uv run python -m coverage run --source . -m pytest tests/ -vv --durations=5 && uv run python -m coverage report --skip-empty --omit "tests/*" -m
```

## Author

Faouzi Braza
