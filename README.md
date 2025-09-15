## OpenLibrary Data Pipeline (WIP)

This is an early-stage data pipeline that retrieves and processes book metadata from the OpenLibrary API. The pipeline is designed to collect, simplify, and merge information about books by author, preparing it for further analysis or storage in a database.

At this stage, the codebase consists of reusable utility functions for fetching and transforming book data.

## Features

- Fetch a list of books by a given author from OpenLibrary.
- Simplify and standardise book metadata (title, author, year, edition count, etc.).
- Retrieve subjects, ISBNs, and publisher data for each book.
- Merge multiple API responses into a single consistent dictionary.
- Generate pipeline-ready book records for an author with one function call.

## Next Steps

- Add database integration (Postgres / DynamoDB).
- Orchestrate pipeline with Airflow or AWS Step Functions.
- Add Docker containerisation and CI/CD pipeline.
- Expand to support multiple authors and bulk ingestion.