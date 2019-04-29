# Knowledge Graph for AI Researchers

## Installation Steps
1. Bulk-Loading Elastic-Search with data
    - make sure you have elastic-search running at ```localhost:9200```
    - ```cd <project-path>/scraping/kaladhar/dblp/dblp/data/```
    - ```curl -X POST 'http://localhost:9200/research_doc/research_information/_bulk?pretty' -H 'Content-Type: application/json' --data-binary '@dblp_elastic_upload.json'```
2. Installing and running the client
    - ```cd client && npm i```
    - ```npm run dev```
3. Installing and running server
    - ```cd server && npm i```
    - ```nodemon start```

## Team Members
- Balasubramaniam Thiagarajan
- David Goodfellow
- Kaladhar Mummadi
- Vishal Seshagiri