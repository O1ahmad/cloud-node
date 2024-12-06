### README: Cloud Pricing APIs

---

## Overview

This Python Flask application provides REST APIs to fetch and store pricing, regions, and instance type information for cloud providers, including **AWS**, **GCP**, and **DigitalOcean**. It also supports saving results into a MongoDB database.

---

## Features

1. Fetch **AWS EC2 regions** and **instance types**.
2. Retrieve **on-demand pricing** for AWS, GCP, and DigitalOcean.
3. Retrieve **spot pricing** for AWS and **preemptible pricing** for GCP.
4. Store fetched data into MongoDB with provider details.

---

## Setup

### Prerequisites

1. **Python 3.7+** and `pip`
2. **MongoDB** instance [**Required for persistence**]
3. Cloud credentials:
   - AWS: Configured using the AWS CLI (`aws configure`).
   - GCP: `GCP_API_KEY` environment variable.
   - DigitalOcean: `DO_API_TOKEN` environment variable.

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export GCP_API_KEY="your_gcp_api_key"
   export DO_API_TOKEN="your_digitalocean_api_token"
   export MONGO_URI="your_mongodb_connection_string"
   ```

3. Run the application:
   ```bash
   python app.py
   ```

---

## API Endpoints

### 1. **Fetch Regions**
Retrieve all regions for a provider.

- **URL**: `/regions/<provider>`
- **Method**: `GET`
- **Query Parameters**:
  - `save` (optional): Save results to MongoDB (`true` or `false`).

#### Example Request:
```bash
curl "http://127.0.0.1:5000/regions/aws?save=true"
```

#### Response:
```json
{
    "success": true,
    "regions": ["us-east-1", "us-west-1", "eu-central-1", ...]
}
```

---

### 2. **Fetch Instance Types**
Retrieve all instance types for a provider.

- **URL**: `/instance-types/<provider>`
- **Method**: `GET`
- **Query Parameters**:
  - `save` (optional): Save results to MongoDB (`true` or `false`).

#### Example Request:
```bash
curl "http://127.0.0.1:5000/instance-types/aws?save=true"
```

#### Response:
```json
{
    "success": true,
    "instanceTypes": ["t2.micro", "m5.large", "c5.xlarge", ...]
}
```

---

### 3. **Fetch Pricing**
Retrieve on-demand pricing for a specific provider.

- **URL**: `/pricing/<provider>`
- **Method**: `GET`
- **Query Parameters**:
  - `region`: Cloud region (required for AWS).
  - `instance_type`: Instance type (required for AWS).
  - `save` (optional): Save results to MongoDB (`true` or `false`).

#### Example Request (AWS):
```bash
curl "http://127.0.0.1:5000/pricing/aws?region=us-east-1&instance_type=t2.micro&save=true"
```

#### Response:
```json
{
    "success": true,
    "prices": [
        {
            "ProductDescription": "Linux/UNIX",
            "InstanceType": "t2.micro",
            "Region": "US East (N. Virginia)",
            "PricePerUnitUSD": "0.0116",
            "Unit": "Hrs"
        }
    ]
}
```

---

### 4. **Fetch Spot Pricing**
Retrieve spot pricing for AWS or preemptible pricing for GCP.

- **URL**: `/spot-pricing/<provider>`
- **Method**: `GET`
- **Query Parameters**:
  - `region`: Cloud region (required for AWS).
  - `instance_type`: Instance type (required for AWS).
  - `save` (optional): Save results to MongoDB (`true` or `false`).

#### Example Request (AWS):
```bash
curl "http://127.0.0.1:5000/spot-pricing/aws?region=us-east-1&instance_type=t2.micro&save=true"
```

#### Response:
```json
{
    "success": true,
    "spotPrices": [
        {
            "InstanceType": "t2.micro",
            "AvailabilityZone": "us-east-1a",
            "SpotPrice": "0.0038",
            "Timestamp": "2024-12-05T12:00:00Z"
        }
    ]
}
```

---

### MongoDB Data Schema

Each saved document in MongoDB includes:
- **Provider**: `aws`, `gcp`, or `digitalocean`.
- **Data**: The retrieved API results.
- **Timestamp**: When the data was saved.

---

## Notes

- **Permissions**:
  Ensure the following permissions for cloud credentials:
  - AWS: `ec2:DescribeRegions`, `ec2:DescribeInstanceTypes`, `pricing:GetProducts`, `ec2:DescribeSpotPriceHistory`.
  - GCP: Billing API enabled.
  - DigitalOcean: API token with read access.
- **Environment Variables**:
  Ensure `GCP_API_KEY`, `DO_API_TOKEN`, and `MONGO_URI` are correctly set.

---

## License

This project is licensed under the MIT License.

## Author Information

This project is being developed by O1.IO.

🏆 always happy to help & donations are always welcome 💸

ETH (Ethereum): 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

BTC (Bitcoin): 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

ATOM (Cosmos): cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09