from flask import Flask, request, jsonify
import boto3
import json
from datetime import datetime, timedelta, UTC

app = Flask(__name__)

def fetch_ec2_pricing(region, instance_type):
    """Fetch on-demand pricing information for a specific EC2 instance type."""
    pricing_client = boto3.client('pricing', region_name='us-east-1')  # Pricing API is global

    # Filter for the specific instance type, location, operating system, and tenancy
    filters = [
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
        {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
        {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'}
    ]

    # Call the Pricing API to get the product data
    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=filters,
        FormatVersion='aws_v1'
    )

    # Initialize a list to hold all pricing details
    all_prices = []

    # Iterate over all items in the PriceList
    for price_item in response.get('PriceList', []):
        product_details = json.loads(price_item)
        on_demand_terms = product_details.get('terms', {}).get('OnDemand', {})

        # Extract and format pricing for each product
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

    # Check if any prices were found
    if all_prices:
        return {"success": True, "prices": all_prices}
    else:
        return {"success": False, "message": f"No on-demand pricing found for instance type '{instance_type}' in region '{region}'."}

def fetch_spot_price_history(region, instance_type):
    """Fetch Spot Price History for a specific EC2 instance type."""
    ec2_client = boto3.client('ec2', region_name=region)
    
    # Define the start and end times for the query (last hour)
    end_time = datetime.now(UTC)
    start_time = end_time - timedelta(hours=1)

    # Call the EC2 API to get Spot Price History
    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=['Linux/UNIX'],
        StartTime=start_time.isoformat(),
        EndTime=end_time.isoformat()
    )

    # Initialize a list to hold all spot price details
    all_spot_prices = []

    # Iterate over all spot price history entries
    for entry in response.get('SpotPriceHistory', []):
        all_spot_prices.append({
            'InstanceType': entry.get('InstanceType', 'N/A'),
            'AvailabilityZone': entry.get('AvailabilityZone', 'N/A'),
            'SpotPrice': entry.get('SpotPrice', 'N/A'),
            'Timestamp': entry.get('Timestamp', 'N/A').isoformat() if entry.get('Timestamp') else 'N/A'
        })

    # Check if any spot prices were found
    if all_spot_prices:
        return {"success": True, "spotPrices": all_spot_prices}
    else:
        return {"success": False, "message": f"No spot price history found for instance type '{instance_type}' in region '{region}'."}

@app.route('/pricing/<provider>', methods=['GET'])
def pricing(provider):
    """API endpoint to fetch pricing for a specific cloud provider."""
    region = request.args.get('region')
    instance_type = request.args.get('instance_type')

    if not region or not instance_type:
        return jsonify({"success": False, "message": "Both 'region' and 'instance_type' query parameters are required."}), 400

    if provider == 'aws':
        result = fetch_ec2_pricing(region, instance_type)
    else:
        return jsonify({"success": False, "message": f"Provider '{provider}' not supported."}), 400

    return jsonify(result)


@app.route('/spot-price-history/<provider>', methods=['GET'])
def spot_price_history(provider):
    """API endpoint to fetch Spot Price History for a specific cloud provider."""
    region = request.args.get('region')
    instance_type = request.args.get('instance_type')

    if not region or not instance_type:
        return jsonify({"success": False, "message": "Both 'region' and 'instance_type' query parameters are required."}), 400

    if provider == 'aws':
        result = fetch_spot_price_history(region, instance_type)
    else:
        return jsonify({"success": False, "message": f"Provider '{provider}' not supported."}), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
