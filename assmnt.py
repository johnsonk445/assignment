## List AWS services being used region wise
#!/usr/bin/env python
import skew
from skew.arn import ARN
arn = ARN()
services=arn.service.choices()
services.sort()
print('Enumerating all resources in the following services: ' + ' '.join(services) + '\n')
resources = [];
for service in services:
  arn.service.pattern = service
  for resource in arn:
      with open('myAWSServices-listAudit', 'a') as file1:
          file1.write(resource)
      with open('myAWSServices-detailAudit','a') as file2:
          file2.write(resource.data)
  file.close()
  
  
  ## List each service in detail, like EC2, RDS etc.
  
  import sys
sys.stderr = open('/dev/null')       # Silence silly warnings from paramiko
import paramiko as pm
sys.stderr = sys.__stderr__
import os

class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

HOST = 'MY EC2 HOST' # codedeploy host
USER = 'ec2-user'
PASSWORD = ''

client = pm.SSHClient()
client.load_system_host_keys()
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
client.set_missing_host_key_policy(AllowAllKeys())
client.connect(HOST, username=USER, password=PASSWORD)

channel = client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')

stdin.write('''
sudo yum -y update
sudo yum install -y ruby
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install awscli
cd /home/ec2-user
sudo aws s3 cp s3://aws-codedeploy-ap-southeast-1/latest/install . --region ap-southeast-1
sudo chmod +x ./install
sudo ./install auto
aws deploy create-application --application-name myApp
aws deploy create-deployment-group \
  --application-name myApp \
  --auto-scaling-groups AutoScalingGroup \
  --deployment-group-name myApp \
  --deployment-config-name CodeDeployDefault.OneAtATime \
  --service-role-arn service-role-arn
''')
