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

Here's the updated README markdown to reflect the updated variable values:

## Role Variables

### Common Variables

|         var         |                        description                         |     default      |
| :-----------------: | :--------------------------------------------------------: | :--------------: |
|   _create_secure_node_   |       Whether to create a secure node to setup         |       `false`       |
|   _cloud_region_    |           Cloud region where resources will be deployed    |     `us-east-1`    |
|   _instance_tag_    |          Tag for the instance and security group           |        ` `         |
|   _instance_type_   |               Instance type for the deployment             |     `t2.micro`     |
|   _storage_size_    |           Storage size for the instance in GB              |       `30`         |
|   _public_ip_       |        Whether to assign a public IP to the instance       |      `true`        |
| _ssh_private_key_path_ |        Path to the SSH private key for the instance     | `~/.ssh/id_rsa`    |
|   _wait_for_ssh_    |     Whether to wait for SSH to become available during setup |     `true`        |
|  _ingress_ports_    | List of ingress ports and protocols for the security group |  `[{ protocol: 'tcp', port: 22, cidr: '0.0.0.0/0' }]` |

### AWS Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _ami_id_               |      AMI ID for the EC2 instance      | `ami-0d5d9d301c853a04a` |
|   _security_group_name_  |    Name of the AWS security group     |    `aws-security-group`    |
|   _security_group_description_ |  Description for the AWS security group  | `AWS Security Group` |

### GCP Specific Variables

|           var            |              description              |   default    |
| :----------------------: | :-----------------------------------: | :----------: |
|   _gcp_project_          |           GCP project ID             | ` ` |
|   _image_                |  Source image for the GCP instance   | `projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20210623` |
|   _zone_                 |            GCP zone                  | `us-east1-b` |
|   _gcp_security_group_name_ |   Name of the GCP firewall rule    |    `gcp-firewall-rule`       |

### Azure Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _resource_group_       |        Azure resource group           | ` ` |
|   _location_             |         Azure location                | `eastus` |
|   _vnet_name_            |    Name of the Azure virtual network  | ` ` |
|   _subnet_name_          |      Name of the Azure subnet         | ` ` |
|   _public_ip_name_       |  Name of the Azure public IP address  | ` ` |
|   _nic_name_             |     Name of the Azure network interface | ` ` |
|   _azure_security_group_name_ | Name of the Azure security group | `azure-security-group`       |
|   _ssh_public_key_       | SSH public key for the Azure instance | ` `       |

### DigitalOcean Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _do_token_             |  DigitalOcean API token               | ` `       |
|   _do_region_            |  DigitalOcean region                  | `nyc3`    |
|   _do_size_              |  DigitalOcean droplet size            | `s-1vcpu-1gb` |
|   _do_image_             |  DigitalOcean droplet image           | `ubuntu-20-04-x64` |
|   _do_ssh_key_fingerprint_ | SSH key fingerprint for the droplet | ` `       |
|   _do_firewall_name_     |  Name of the DigitalOcean firewall    | `do-firewall` |


## Dependencies

`-`

## Example Playbook
```
- hosts: controller
  roles:
```

- Provision a t3.micro EC2 instance:
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

This Ansible role was created in 2023 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

- **ETH (Ethereum):** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

- **BTC (Bitcoin):** 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

- **ATOM (Cosmos):** cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09
