#!/usr/bin/env python3

###
# Manage knowledge base using Astra DB
#
# This script allows to push and delete knowledge chunks in an Astra DB database.
#
# Usage:
#   ./manage-knowledge.py <command>
# Commands:
#   push   - Split and store file content as knowledge chunks
#   clear  - Delete all knowledge chunks
###

import os
from astrapy import DataAPIClient

def connect_to_db():
    # load environment variables
    DATA_API_TOKEN = os.getenv("ASTRA_DB_TOKEN")
    DB_ENDPOINT = "https://03f698d0-0aca-4200-aedd-44888cb4a236-us-east-2.apps.astra.datastax.com"
    if not DATA_API_TOKEN:
        raise ValueError("ASTRA_DB_TOKEN environment variable not set.")

    # Initialize the client
    client = DataAPIClient(DATA_API_TOKEN)
    db = client.get_database_by_api_endpoint(DB_ENDPOINT)

    return db


def push_knowledge(file_path):
    """Push knowledge chunks from a file to the database."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Simple chunking by splitting on double newlines
    chunks = content.split('\n\n')
    db = connect_to_db()
    collection = db.get_collection("knowledge_chunks")
    
    for i, chunk in enumerate(chunks):
        doc = {
            "id": f"chunk_{i}",
            "content": chunk.strip()
        }
        collection.create_document(doc)
        print(f"Pushed chunk {i} to database.")
    print("All chunks pushed successfully.")

def clear_knowledge():
    """Delete all knowledge chunks."""
    db = connect_to_db()
    collection = db.get_collection("iaqro")
    try:
        collection.delete_many({})
        print("Deleted all knowledge chunks.")
    except Exception as e:
        print(f"Error deleting chunks: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./manage-knowledge.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "push":
        if len(sys.argv) != 3:
            print("Usage: ./manage-knowledge.py push <file_path>")
            sys.exit(1)
        file_path = sys.argv[2]
        push_knowledge(file_path)

    elif command == "clear":
        clear_knowledge()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)