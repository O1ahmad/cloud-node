<!-- @format -->

<p><img src="https://code.benco.io/icon-collection/logos/ansible.svg" alt="ansible logo" title="ansible" align="left" height="60" /></p>

# Cloud-Node
[![Galaxy Role](https://img.shields.io/ansible/role/d/0x0i/cloud-node
)](https://galaxy.ansible.com/ui/standalone/roles/0x0i/cloud-node/)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/cloud-node?color=yellow)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Provision a node across the various cloud infrastructure providers with security best practices.

## Requirements

`-`

## Role Variables

### Common Variables

|         var         |                        description                         |     default      |
| :-----------------: | :--------------------------------------------------------: | :--------------: |
|   _cloud_provider_  |      Cloud provider to use for resource management         |     `aws`         |
|   _cloud_location_    |           Cloud region where resources will be deployed    |     `us-east-1`    |
|   _cloud_user_      |      User for SSH and instance management                  |     `ubuntu`      |
|   _instance_name_    |          Name of the instance                              |     `default-instance` |
|   _instance_type_   |               Instance type for the deployment             |     `t2.micro` (AWS), `n1-standard-1` (GCP), `Standard_B1s` (Azure), `s-1vcpu-1gb` (DO)     |
|   _instance_image_  |      Instance image for the deployment                    |     `ami-0e001c9271cf7f3b9`    |
|   _instance_tag_     |          Tag for the instance and security group           |        ` `         |
|   _storage_size_    |           Storage size for the instance in GB              |       `30`         |
|   _public_ip_       |        Whether to assign a public IP to the instance       |      `true`        |
| _ssh_private_key_path_ |        Path to the SSH private key for the instance     | `~/.ssh/default`    |
|   _ssh_public_key_       | SSH public key or keypair for the Cloud instance | `~/.ssh/default.pub `       |
|   _wait_for_ssh_    |     Whether to wait for SSH to become available during setup |     `true`        |
|  _ingress_ports_    | List of ingress ports and protocols for the security group |  `[{ protocol: 'tcp', port: 22, cidr: '0.0.0.0/0' }]` |
|  _security_group_name_    |       Name of the security group to create            | `default-security-group` |
|  _security_group_description_ |  Description for the security group  | `Default Security Group` |
|   _uninstall_       |      Whether to uninstall/remove the created resources     |     `false`       |

### AWS Specific Variables

#### Environment Variables

To authorize access to your AWS resources, set the following environment variables:
```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
export AWS_DEFAULT_REGION=<your-region>
```

### GCP Specific Variables

|           var            |              description              |   default    |
| :----------------------: | :-----------------------------------: | :----------: |
|   _gcp_project_          |           GCP project ID             | ` ` |

#### Environment Variables

To authorize access to your GCP resources, set the following environment variable:
```
export GCP_AUTH_KIND=<path-to-your-service-account-json>
```

### Azure Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _resource_group_       |        Azure resource group           | ` ` |
|   _vnet_name_            |    Name of the Azure virtual network  | ` ` |
|   _subnet_name_          |      Name of the Azure subnet         | ` ` |
|   _public_ip_name_       |  Name of the Azure public IP address  | ` ` |
|   _nic_name_             |     Name of the Azure network interface | ` ` |

#### Environment Variables

To authorize access to your Azure resources, set the following environment variables:
```
export AZURE_SUBSCRIPTION_ID=<your-subscription-id>
export AZURE_CLIENT_ID=<your-client-id>
export AZURE_SECRET=<your-secret>
export AZURE_TENANT=<your-tenant-id>
```

### DigitalOcean Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _do_ssh_key_fingerprint_ | SSH key fingerprint for the droplet | ` `       |


#### Environment Variables

To authorize access to your DigitalOcean resources, set the following environment variable:
```
export DO_API_TOKEN=<your-api-token>
```

## Dependencies

`-`

## Example Playbook
```
- hosts: controller
  roles:
```

- Provision a `t3.micro` EC2 instance:
```
  - role: 0x0i.cloud-node
    vars:
      cloud_provider: aws
      image: ami-0e001c9271cf7f3b9
      instance: "t3.micro"
```

## License

MIT

## Author Information

This Ansible role was created in 2024 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

- **ETH (Ethereum):** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

- **BTC (Bitcoin):** 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

- **ATOM (Cosmos):** cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09
