from flask import Flask, request, jsonify
import boto3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def fetch_ec2_pricing(region, instance_type):
    """Fetch on-demand pricing information for a specific EC2 instance type."""
    pricing_client = boto3.client('pricing', region_name=region)  # Pricing API is global; region is always us-east-1

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

    if response['PriceList']:
        price_list = json.loads(response['PriceList'][0])
        on_demand_terms = price_list.get('terms', {}).get('OnDemand', {})
        
        # Extract price details
        prices = []
        for term in on_demand_terms.values():
            for dimension in term.get('priceDimensions', {}).values():
                prices.append({
                    'Description': dimension.get('description'),
                    'PricePerUnitUSD': dimension.get('pricePerUnit', {}).get('USD')
                })
        
        return {"success": True, "prices": prices}
    else:
        return {"success": False, "message": f"No on-demand pricing found for instance type '{instance_type}' in region '{region}'."}


def fetch_spot_price_history(region, instance_type):
    """Fetch Spot Price History for a specific EC2 instance type."""
    ec2_client = boto3.client('ec2', region_name=region)
    
    # Define the start and end times for the query (last hour)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)

    # Call the EC2 API to get Spot Price History
    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=['Linux/UNIX'],
        StartTime=start_time.isoformat(),
        EndTime=end_time.isoformat()
    )

    spot_prices = []
    for entry in response['SpotPriceHistory']:
        spot_prices.append({
            'InstanceType': entry['InstanceType'],
            'AvailabilityZone': entry['AvailabilityZone'],
            'SpotPrice': entry['SpotPrice'],
            'Timestamp': entry['Timestamp'].isoformat()
        })

    if spot_prices:
        return {"success": True, "spotPrices": spot_prices}
    else:
        return {"success": False, "message": f"No spot price history found for instance type '{instance_type}' in region '{region}'."}


@app.route('/pricing', methods=['GET'])
def pricing():
    """API endpoint to fetch EC2 on-demand pricing."""
    region = request.args.get('region')
    instance_type = request.args.get('instance_type')

    if not region or not instance_type:
        return jsonify({"success": False, "message": "Both 'region' and 'instance_type' query parameters are required."}), 400

    result = fetch_ec2_pricing(region, instance_type)
    return jsonify(result)


@app.route('/spot-price-history', methods=['GET'])
def spot_price_history():
    """API endpoint to fetch Spot Price History."""
    region = request.args.get('region')
    instance_type = request.args.get('instance_type')

    if not region or not instance_type:
        return jsonify({"success": False, "message": "Both 'region' and 'instance_type' query parameters are required."}), 400

    result = fetch_spot_price_history(region, instance_type)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
