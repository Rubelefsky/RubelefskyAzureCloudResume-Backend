import logging
import json
import os
import azure.functions as func
from azure.data.tables import TableServiceClient, TableClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GetVisitorCount function processed a request.')

    try:
        # Get connection string from environment variable
        connection_string = os.environ["AzureWebJobsStorage_CosmosDB"]
        table_name = "VisitorCounter"
        
        # Connect to Table Storage
        table_client = TableClient.from_connection_string(
            conn_str=connection_string,
            table_name=table_name
        )
        
        # Get current count
        entity = table_client.get_entity(
            partition_key="visitor",
            row_key="count"
        )
        
        # Increment count
        current_count = entity.get("count", 0) + 1
        
        # Update entity
        entity["count"] = current_count
        table_client.update_entity(entity, mode="merge")
        
        # Return the count
        return func.HttpResponse(
            json.dumps({"count": current_count}),
            status_code=200,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
