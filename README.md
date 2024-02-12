[![Continous integration](https://github.com/Redmar-van-den-Berg/exonviz-web/actions/workflows/ci.yml/badge.svg)](https://github.com/Redmar-van-den-Berg/exonviz-web/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

# Exonviz-web

------------------------------------------------------------------------
## Documentation
Web server and deploy script for the ExonViz server.

## Testing
You can test the deployment using vagrant:
```bash
vagrant up
vagrant provision
```

# Deploy
To deploy the ExonViz web app to the server, use
```bash
ansible-playbook playbook.yml --ask-vault-password --inventory inventory --ask-become-pass
```

## First deployment
If you deploy Exonviz-web to a server for the first time,
you have to pass the `never` tag to the playbook to copy over the nginx
configuration.
**WARNING: This will break the https configuration set up by Certbot, ONLY use
this when provisioning the server for the first time**
```bash
ansible-playbook playbook.yml --tags "all,never"
```

Next, manually set up the letsencrypt ssl certificate using
[Certbot](https://certbot.eff.org/instructions?ws=nginx&os=debianbuster). This
will overwrite the default nginx config that was set with the ansible playbook.

## Update the server For updates, first test your changes using vagrant (it
uses the `never` tag by default). Next, simply deploy using `ansible-playbook
playbook.yml`, without any tags. This will leave the nginx configuration that
was modified by Certbot in place.
