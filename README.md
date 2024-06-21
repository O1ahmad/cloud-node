<!-- @format -->

<p><img src="https://code.benco.io/icon-collection/logos/ansible.svg" alt="ansible logo" title="ansible" align="left" height="60" /></p>

# Cloud-Node
[![Galaxy Role](https://img.shields.io/ansible/role/d/0x0i/cloud-node
)](https://galaxy.ansible.com/ui/standalone/roles/0x0i/cloud-node/)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/cloud-node?color=yellow)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Provision a node across the various cloud infrastructure providers

## Requirements

`-`

## Role Variables

|       var       |                        description                         |     default      |
| :-------------: | :--------------------------------------------------------: | :--------------: |
|     _create_secure_node_     |          whether to create a secure node to setup          |       `false`       |
|     _setup_iptables_     |          configure IP tables to allow ingress paths          |       `false`       |
|   _security_group_name_   |     name of the security group to create      |     ` `     |
|   _security_group_description_   |  description for the security group   |  `Security group for EC2 instance`  |
|   _region_   |    AWS region where resources will be deployed     |     `us-east-1`     |
|   _aws_access_key_   |    AWS access key     |     ` `     |
|   _aws_secret_key_   |    AWS secret key     |     ` `     |
|   _instance_type_   |    EC2 instance type     |     `t2.micro`     |
|   _instance_tag_   |    Tag for the EC2 instance and security group     |     ` `     |
|   _storage_size_   |    Storage size for the EC2 instance in GB     |     `8`     |


## Dependencies

`-`

## Example Playbook
```
- hosts: controller
  roles:
```

- Provision a t3.micro EC2 instance:
```
  - role: 0x0I.cloud-node
    vars:
      namcloud_provider: aws
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
