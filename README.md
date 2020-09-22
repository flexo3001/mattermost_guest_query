# mattermost_guest_query

## Dependencies
### CentOS 7
```
sudo yum install python3-pip
pip3 install --user -r requirements.txt  # (e.g. inside the **mattermost** user)
```

or to install the needed module system wide

```
sudo pip3 install -r requirements.txt
```

### CentOS 8
```
sudo dnf install python3-PyMySQL
```

## Usage
This reposity needs to be cloned or downloaded as archive. Next after cloning or extracting `cd` into
*mattermost_guest_query*. Afterwards one could use `chmod +x guest_query.py` and
```
./guest_query.py -u mmuser -D mattermost -p mmuser_password -d 60
```
to get a list of inactive users.
To deactivate them right away execute for example
```
/opt/mattermost/bin/mattermost user deactivate $(guest_query.py -u mmuser -D mattermost -H 127.0.0.1 -p mmuser_password -d 6)
```

Documentation for the Mattermost command line can be found
[here](https://docs.mattermost.com/administration/command-line-tools.html#mattermost-user-deactivate)
