#!/usr/bin/env python3
"""Log stats
"""


def nginx_log_stats(mongo_collection):
    """displays stats about Nginx logs from a MongoDB collection
    """
    total_logs = mongo_collection.count_documents({})

    method_counts = {}
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        method_counts[method] = count

    status_checks = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    nginx_log_stats(collection)
