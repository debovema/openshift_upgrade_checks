# OpenShift upgrade checks

This Ansible role allows you to perform validation checks on your OpenShift cluster before an upgrade. Each check is a single task in the role and can be skipped to avoid redundancy when relaunching the checks.

Detailed checks documentation can be found in the [`docs/checks.md`](docs/checks.md) file.

## Requirements

### Supported OpenShift versions

This role is intended to be run on any OpenShift 4.x cluster. OpenShift 3.x is not supported by the role.

### Python and Ansible environment

This role requires the following Ansible collection:
 - [Openshift collection](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/openshift) (v4.0.1)

and the following Python packages:
* kubernetes
* requests
* requests-oauthlib

#### Python virtual environment (optional)

It is advised to use a Python virtual environment to install Ansible and the requirements:

```shell
# create a Python virtual environment
python3 -m venv .venv
# activate the virtual environment
source .venv/bin/activate

# install pip and Ansible
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade ansible
```

#### Python packages

Install the Python packages requirements with this command:

```shell
pip install -r requirements.txt
```

#### Ansible collection

Install the Ansible collection requirement with this command:

```shell
ansible-galaxy collection install -r requirements.yml
```

> To keep everything in the Python virtual environment (if using one), install the collection in the *venv* `site-packages` directory:
>
> ```shell
> export ANSIBLE_GALAXY_COLLECTIONS_PATH_WARNING=false
> VENV_SITE_PACKAGES_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")
>
> ansible-galaxy collection install -r requirements.yml -p $VENV_SITE_PACKAGES_DIR
> ```

> In a disconnected environment, use `requirements.offline.yml` file instead of `requirements.yml` and copy the `redhat-openshift-4.0.1.tar.gz` archive in the directory of this repository (file will be Git-ignored).

## Usage

### Variables

This role requires some variables to function properly. You can pass them as [extra vars, through a variables file](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html) or [a Vault-encrypted variables file](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-files-with-ansible-vault).

The minimal variables required to target a cluster:

| Variable | Comments | Examples |
|----------|----------|----------|
|openshift_upgrade_checks_api_url | Holds the cluster api URL | `https://api.cluster.domain.com:6443`
|openshift_upgrade_checks_validate_certs | Should the API and Prometheus certs be validated against the system CA ? | `true/false`
|openshift_upgrade_checks_username | Holds the username of the user that will perform the checks | `admin-viewer`
|openshift_upgrade_checks_password | Holds the password of the user that will perform the checks | `really-long-and-secure-password` 

### Test playbook

A test playbook is included.

Before running the test playbook, create a `vars.yml` with the required variables of this role:

```shell
cat <<EOF > vars.yml
openshift_upgrade_checks_api_url: '<OpenShift API URL>'
openshift_upgrade_checks_validate_certs: false
openshift_upgrade_checks_username: "<username>"
openshift_upgrade_checks_password: "<password>"
EOF
```

> The `vars.yml` is Git-ignored to avoid leaking credentials

Run the playbook :

```shell
ansible-playbook -v test.yml
```

To choose which checks to run, use Ansible tags:

```shell
ansible-playbook --skip-tags verify_upgrade_path test.yml
```

> This will skip the `verify_upgrade_path` check (useful if running in a disconnected environment)

## Variables

| Variable | Default | Comments | Examples |
|----------|---------|----------|----------|
| openshift_upgrade_checks_api_url | None (mandatory) | Holds the cluster api URL | `https://api.cluster.domain.com:6443`
| openshift_upgrade_checks_validate_certs | `false` | Should the API and Prometheus certs be validated against the system CA ? | `true/false`
| openshift_upgrade_checks_username | None (mandatory) | Holds the username of the user that will perform the checks | `admin-viewer`
| openshift_upgrade_checks_password | None (mandatory) | Holds the password of the user that will perform the checks | `really-long-and-secure-password`
| openshift_upgrade_checks_prometheus_alerts| see [defaults/main/prometheus_alerts.yml](defaults/main/prometheus_alerts.yml) | This variable holds a list of critical alerts, that can be modified if needed | see [defaults/main/prometheus_alerts.yml](defaults/main/prometheus_alerts.yml)

## License

BSD