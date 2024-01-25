search `terraform google provider`

terraform fmt

export GOOGLE_APPLICATION_CREDENTIALS='/workspaces/DE-Zoomcamp24/.ssh/gcp-sv.json'


 terraform init

 `terraform google cloud storage bucket`

 terraform apply
 terraform destroy


 git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch google-cloud-sdk/bin/anthoscli'


 On branch main
Your branch and 'origin/main' have diverged,
and have 9 and 5 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

[text](https://poanchen.github.io/blog/2020/09/19/what-to-do-when-git-branch-has-diverged)
`git rebase origin/main`

`git merge origin/main`

### Create SSH key
`ssh-keygen -t rsa -f gcp -C daniel -b 2048`

`ssh -i .ssh/gcp daniel@34.16.76.44`

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '.ssh/gcp' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key ".ssh/gcp": bad permissions
daniel@34.16.76.44: Permission denied (publickey).

`ls -l gcp`

-rw-r--r-- 1 codespace codespace 1811 Jan 23 18:41 gcp

chmod 0400 gcp

-r-------- 1 codespace codespace 1811 Jan 23 18:41 gcp



ls -l gcp

Host de-zoomcamp
    HostName 34.16.76.44
    User daniel
    IdentityFile ~/.ssh/gcp


`python3 --version`

`gcloud --version`

Google Cloud SDK 460.0.0
alpha 2024.01.12
beta 2024.01.12
bq 2.0.101
bundled-python3-unix 3.11.6
core 2024.01.12
gcloud-crc32c 1.0.0
gsutil 5.27
minikube 1.32.0
skaffold 2.9.0


which python3
/usr/bin/python3

`sudo apt-get update`

sudo groupadd docker

sudo gpasswd -a $USER docker

[text](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)

[text](https://docs.docker.com/desktop/install/ubuntu/)

[text](https://wiki.crowncloud.net/?How_to_Install_and_use_Docker_Compose_on_Ubuntu_22_04)


### GCP VM

ssh de-zoomcamp


sftp de-zoomcamp

export GOOGLE_APPLICATION_CREDENTIALS='/home/daniel/.ssh/gcp-sv.json'

## Aunthentication
`gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS`