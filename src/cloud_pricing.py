from flask import Flask, request, jsonify
import boto3
import json
import os
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

GCP_API_KEY = os.getenv('GCP_API_KEY')
DO_API_TOKEN = os.getenv('DO_API_TOKEN')

# AWS Pricing Functions
def fetch_ec2_pricing(region, instance_type):
    """Fetch on-demand pricing information for a specific EC2 instance type."""
    pricing_client = boto3.client('pricing', region_name='us-east-1')

    filters = [
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
        {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
        {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'}
    ]

    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=filters,
        FormatVersion='aws_v1'
    )

    all_prices = []
    for price_item in response.get('PriceList', []):
        product_details = json.loads(price_item)
        on_demand_terms = product_details.get('terms', {}).get('OnDemand', {})

        for term in on_demand_terms.values():
            for dimension in term.get('priceDimensions', {}).values():
                all_prices.append({
                    'ProductDescription': product_details.get('product', {}).get('attributes', {}).get('description', 'N/A'),
                    'InstanceType': product_details.get('product', {}).get('attributes', {}).get('instanceType', 'N/A'),
                    'Region': product_details.get('product', {}).get('attributes', {}).get('location', 'N/A'),
                    'PricePerUnitUSD': dimension.get('pricePerUnit', {}).get('USD', 'N/A'),
                    'Unit': dimension.get('unit', 'N/A'),
                    'Description': dimension.get('description', 'N/A')
                })

    if all_prices:
        return {"success": True, "prices": all_prices}
    else:
        return {"success": False, "message": f"No on-demand pricing found for instance type '{instance_type}' in region '{region}'."}

def fetch_spot_price_history(region, instance_type):
    """Fetch Spot Price History for a specific EC2 instance type."""
    ec2_client = boto3.client('ec2', region_name=region)

    end_time = datetime.now(UTC)
    start_time = end_time - timedelta(hours=1)

    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=['Linux/UNIX'],
        StartTime=start_time.isoformat(),
        EndTime=end_time.isoformat()
    )

    all_spot_prices = []
    for entry in response.get('SpotPriceHistory', []):
        all_spot_prices.append({
            'InstanceType': entry.get('InstanceType', 'N/A'),
            'AvailabilityZone': entry.get('AvailabilityZone', 'N/A'),
            'SpotPrice': entry.get('SpotPrice', 'N/A'),
            'Timestamp': entry.get('Timestamp', 'N/A').isoformat() if entry.get('Timestamp') else 'N/A'
        })

    if all_spot_prices:
        return {"success": True, "spotPrices": all_spot_prices}
    else:
        return {"success": False, "message": f"No spot price history found for instance type '{instance_type}' in region '{region}'."}


# GCP Pricing Functions
def fetch_gcp_pricing():
    """Fetch on-demand pricing from GCP, handling pagination."""
    url = f"https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus?key={GCP_API_KEY}"
    all_prices = []
    next_page_token = None

    while True:
        # Append the nextPageToken as a query parameter if it exists
        if next_page_token:
            paginated_url = f"{url}&pageToken={next_page_token}"
        else:
            paginated_url = url

        response = requests.get(paginated_url)
        if response.status_code == 200:
            pricing_data = response.json()

            all_prices.extend(pricing_data.get('skus', []))
            next_page_token = pricing_data.get('nextPageToken')
            if not next_page_token:
              break
        else:
            return {
                "success": False,
                "message": f"GCP Pricing API request failed with status code {response.status_code}",
                "error": response.text
            }

    return {"success": True, "prices": all_prices}

def fetch_gcp_preemptible_pricing():
    """Fetch preemptible pricing from GCP."""
    # Fetch all pricing data using fetch_gcp_pricing
    all_pricing = fetch_gcp_pricing()
    if not all_pricing.get("success"):
        return {
            "success": False,
            "message": "Failed to fetch GCP pricing data.",
            "error": all_pricing.get("message")
        }

    preemptible_prices = [
        sku for sku in all_pricing.get("prices", [])
        if sku.get("category", {}).get("usageType") == "Preemptible"
    ]

    return {"success": True, "preemptiblePrices": preemptible_prices}

# DigitalOcean Pricing Functions
def fetch_digitalocean_pricing():
    """Fetch pricing information for DigitalOcean."""
    url = "https://api.digitalocean.com/v2/sizes"
    headers = {"Authorization": f"Bearer {DO_API_TOKEN}"}
    all_sizes = []

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            all_sizes.extend(data.get('sizes', []))

            url = data.get('links', {}).get('pages', {}).get('next')
        else:
            return {
                "success": False,
                "message": f"DigitalOcean Pricing API request failed with status code {response.status_code}",
                "error": response.text
            }

    return {"success": True, "sizes": all_sizes}


# Flask Endpoints
@app.route('/pricing/<provider>', methods=['GET'])
def pricing(provider):
    """API endpoint to fetch pricing for a specific provider."""
    region = request.args.get('region')
    instance_type = request.args.get('instance_type')

    if provider == 'aws':
        if not region or not instance_type:
            return jsonify({"success": False, "message": "Both 'region' and 'instance_type' query parameters are required."}), 400
        return jsonify(fetch_ec2_pricing(region, instance_type))
    elif provider == 'gcp':
        return jsonify(fetch_gcp_pricing())
    elif provider == 'digitalocean':
        return jsonify(fetch_digitalocean_pricing())
    else:
        return jsonify({"success": False, "message": f"Provider '{provider}' not supported."}), 400


@app.route('/spot-pricing/<provider>', methods=['GET'])
def spot_pricing(provider):
    """API endpoint to fetch spot pricing for a specific provider."""
    region = request.args.get('region')
    instance_type = request.args.get('instance_type')

    if provider == 'aws':
        if not region or not instance_type:
            return jsonify({"success": False, "message": "Both 'region' and 'instance_type' query parameters are required."}), 400
        return jsonify(fetch_spot_price_history(region, instance_type))
    elif provider == 'gcp':
        return jsonify(fetch_gcp_preemptible_pricing())
    else:
        return jsonify({"success": False, "message": f"Provider '{provider}' not supported."}), 400


if __name__ == "__main__":
    app.run(debug=True)
