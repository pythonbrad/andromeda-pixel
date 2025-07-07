# Andromeda Galaxy Discovery

![screenshot](https://github.com/user-attachments/assets/a16b563e-f584-4230-b09c-a14a860fe4ed)

A website to share picture of the Andromeda galaxy with the world.

### Requirements

- [Python3.11+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/): An extremely fast Python package and project manager (*optional*)
- [AWS account](https://aws.amazon.com)

### Installation

**pip**

```
pip install .
flask --app flaskr init-db
```

**uv**

```
uv sync
uv run flask --app flaskr init-db
```

**environment**

You should config the `AWS_S3_BUCKET_NAME` environment variable at `instance/config.py`.
Note that you shoud also config your AWS credentials. You can use [`aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for it.

### How to run

**pip**

```
flask --app flaskr run --debug
```

**uv**

```
uv run flask --app flaskr run --debug:
```

After the server is ready, you can access the webapp at http://127.0.0.1:5000/.

### License

MIT
