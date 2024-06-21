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
|   _cloud_provider_  |      Cloud provider to use for resource management         |     `aws`         |
|   _cloud_location_    |           Cloud region where resources will be deployed    |     `us-east-1`    |
|   _cloud_user_      |      User for SSH and instance management                  |     `ubuntu`      |
|   _instance_name_    |          Name of the instance                              |     `default-instance` |
|   _instance_type_   |               Instance type for the deployment             |     `t2.micro` (AWS), `n1-standard-1` (GCP), `Standard_B1s` (Azure), `s-1vcpu-1gb` (DO)     |
|   _instance_image_  |      Instance image for the deployment                    |     `ubuntu-20-04-x64`    |
|   _instance_tag_     |          Tag for the instance and security group           |        ` `         |
|   _storage_size_    |           Storage size for the instance in GB              |       `30`         |
|   _public_ip_       |        Whether to assign a public IP to the instance       |      `true`        |
| _ssh_private_key_path_ |        Path to the SSH private key for the instance     | `~/.ssh/id_rsa`    |
|   _wait_for_ssh_    |     Whether to wait for SSH to become available during setup |     `true`        |
|  _ingress_ports_    | List of ingress ports and protocols for the security group |  `[{ protocol: 'tcp', port: 22, cidr: '0.0.0.0/0' }]` |
|  _security_group_name_    |       Name of the security group to create            | `default-security-group` |
|  _security_group_description_ |  Description for the security group  | `Default Security Group` |
|   _uninstall_       |      Whether to uninstall/remove the created resources     |     `false`       |

### AWS Specific Variables

(none)

### GCP Specific Variables

|           var            |              description              |   default    |
| :----------------------: | :-----------------------------------: | :----------: |
|   _gcp_project_          |           GCP project ID             | ` ` |

### Azure Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _resource_group_       |        Azure resource group           | ` ` |
|   _vnet_name_            |    Name of the Azure virtual network  | ` ` |
|   _subnet_name_          |      Name of the Azure subnet         | ` ` |
|   _public_ip_name_       |  Name of the Azure public IP address  | ` ` |
|   _nic_name_             |     Name of the Azure network interface | ` ` |
|   _ssh_public_key_       | SSH public key for the Azure instance | ` `       |

### DigitalOcean Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _do_ssh_key_fingerprint_ | SSH key fingerprint for the droplet | ` `       |

### Alibaba Cloud Specific Variables

|           var            |              description              |  default  |
| :----------------------: | :-----------------------------------: | :-------: |
|   _alicloud_vswitch_id_  | Alibaba Cloud VSwitch ID              | ` `       |
|   _alicloud_security_group_id_ | Alibaba Cloud Security Group ID | ` `       |

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
