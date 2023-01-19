# pwarden
![Supported Python versions](https://img.shields.io/badge/Python-3.9-green)
![License](https://img.shields.io/badge/Licence-Apache%202.0-yellowr)
![Level](https://img.shields.io/badge/Noob-yes-blue)


If you use bitwarden and are constantly annoyed about having to use an extension or installing an extra program in your workstation to access your stored credential, this repository is for you! 

pwarden is a python script on top of the bw cli bin that will make it easier to query your credentials and by default copies the selected password to your clipboard.


## bw cli

This script uses the BW_SESSION env variable to authenticate though bw cli.

To get this value you need to get your `Client ID` and `Client Secret` from your account.

These two can get retrieved from `Account Settings` > `Security` > `Api Key` > `View API Key`

Then you will need to export the values and log in:
```bash
# The next values are for obvious reasons fake.
export BW_CLIENTID=user.d2707991-abcd-3abb-69ab-in4dr4vkmrab
export BW_CLIENTSECRET=SWsPiBBdweFMcinm5ERIHxgGSpsm7v
[vagrant@centos8 bin]$ bw login --apikey
Could not find dir, "/home/vagrant/.config/Bitwarden CLI"; creating it instead.
Could not find data file, "/home/vagrant/.config/Bitwarden CLI/data.json"; creating it instead.
You are logged in!

To unlock your vault, use the `unlock` command. ex:
$ bw unlock
[vagrant@centos8 bin]$ bw unlock
? Master password: [hidden]   # <- type your master password
Your vault is now unlocked!

To unlock your vault, set your session key to the `BW_SESSION` environment variable. ex:
$ export BW_SESSION="BUm6WmGpy/maKASFxr7dOcFu5clPtVxMxWl7M7dYaS8Y3BysLLkIomyGcx51wd6XpFdx5Atun02LGF8D"
> $env:BW_SESSION="BUm6WmGpy/maKASFxr7dOcFu5clPtVxMxWl7M7dYaS8Y3BysLLkIomyGcx51wd6XpFdx5Atun02LGF8D"

You can also pass the session key to any command with the `--session` option. ex:
$ bw list items --session BUm6WmGpy/maKASFxr7dOcFu5clPtVxMxWl7M7dYaS8Y3BysLLkIomyGcx51wd6XpFdx5Atun02LGF8D
```

As mentioned in the previous box you can unlock your bitwarden vault with your session key. 

## Installation
pwarden uses a virtual environment in order to isolate pip packages and allow end users to use it and manage the dependencies without risking messing up the core libraries of their OS.

Follow these steps to begin with the setup:
1. Install python3.9 in your OS.
2. Install pipenv
``` bash
pip3.9 install --user pipenv
```
3. Install PWarden requirements
``` bash
cd <repo_path>
pipenv install
```
> **Note**  pyinquierer is not compatible with python 3.10 yet
>  * https://github.com/CITGuru/PyInquirer/issues/159
>  * https://github.com/CITGuru/PyInquirer/issues/14


## Usage

The easier way to use pwarden is creating an alias in your bash session. to do so you will need to add these lines in your `.bashrc` file
```bash 
export BW_SESSION='BUm6WmGpy/maKASFxr7dOcFu5clPtVxMxWl7M7dYaS8Y3BysLLkIomyGcx51wd6XpFdx5Atun02LGF8D'
alias pwarden="<full_pwarden_path>/.venv/bin/python /<full_pwarden_path>/pwarden.py"
```

Then by reloading your session you should be able to query your credentials.

**Help message**
```bash 
[vagrant@centos8 ~]$ pwarden --help
usage: pwarden.py [-h] string

Find & copy passwords to your clipboard from a Bitwarden

positional arguments:
  string      String to find

optional arguments:
  -h, --help  show this help message and exit
```

**Basic query**


```bash
[vagrant@centos8 ~]$ pwarden github
? Which credential do you need? GitHub dude account 
Full Item Name: GitHub dude account
URL: https://github.com/login
username: dude
Password: <hidden_password>
Password copied to clipboard
```