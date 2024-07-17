#!/usr/bin/env python3
"""
Log statistics from MongoDB using pymongo.
"""

from pymongo import MongoClient

def count_documents(mongo_collection):
    """
    Count the number of documents in a collection.
    """
    return mongo_collection.count_documents({})

def count_methods(mongo_collection):
    """
    Count the number of documents with each HTTP method.
    """
    pipeline = [
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ]
    method_counts = {method["_id"]: method["count"] for method in mongo_collection.aggregate(pipeline)}
    return method_counts

def top_ips(mongo_collection, top=10):
    """
    Get the top IPs by count.
    """
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": top}
    ]
    top_ips = {doc["_id"]: doc["count"] for doc in mongo_collection.aggregate(pipeline)}
    return top_ips

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Count total logs
    total_logs = count_documents(nginx_collection)
    print(f"{total_logs} logs")

    # Count HTTP methods
    method_counts = count_methods(nginx_collection)
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")

    # Top 10 IPs
    top_ips_result = top_ips(nginx_collection)
    print("IPs:")
    for ip, count in top_ips_result.items():
        print(f"    {ip}: {count}")
