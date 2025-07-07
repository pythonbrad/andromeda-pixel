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
Note that you shoud also config your AWS credentials. 
If you have the AWS CLI installed, then you can use the aws configure command to configure your credentials file:

```
aws configure
```

Alternatively, you can create the credentials file yourself. By default, its location is `~/.aws/credentials`. At a minimum, the credentials file should specify the access key and secret access key. In this example, the key and secret key for the account are specified in the default profile:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

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
