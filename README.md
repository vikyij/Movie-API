# Movie-API
- 

## Create S3 bucket to store movie cover images of each image
- Create bucket 
    ```
        aws s3 mb s3://unique-bucket-name
    ```
- upload images
    ```
        aws s3 cp filename s3://unique-bucket-name 
    ```
- list contents of bucket to confirm upload
    ```
       aws s3 ls s3://unique-bucket-name
    ```

## Create NoSQL database (dynamo db) to store movie data
- Create table
    ```
        aws dynamodb create-table --table-name movie-data \
         --attribute-definitions \
            AttributeName=movieId,AttributeType=S \
        --key-schema \
            AttributeName=movieId,KeyType=HASH \
        --provisioned-throughput \
            ReadCapacityUnits=5,WriteCapacityUnits=5 \
        <!-- on demand mode -->
        --billing-mode PAY_PER_REQUEST
    ```
    
    
- Verify table has been created
    ```
        aws dynamodb describe-table --table-name movie-data 
    ```

- Write items to table
    ```
        aws dynamodb putitem --table-name movie-data --item \
        '{"movieId":{"S": "1"}, "title": {"S": "A good day"}, "releaseYear": {"S": "2024"}, "genre": {"S": "romantic-comedy"}, "coverUrl": {"S":"s3://link-to-cover-url"}}'
    ```

- Read items from table
    ```
        aws dynamodb get-item --consistent-read --table-name movie-data \
        --key '{"movieId": {"S": "1"}}' 
    ```

- Create a Global Secondary index so I can be able to query by year
    ```
        aws dynamodb update-table \
            --table-name movie-data \
            --attribute-definitions \
                AttributeName=releaseYear,AttributeType=S \
            --global-secondary-index-updates \
                "[{\"Create\":
                     {\"IndexName\": \"releaseYearIndex\", 
                     \"KeySchema\":[{\"AttributeName\": \"releaseYear\", \"KeyType\": \"HASH\"}],
                     \"Projection\": {\"ProjectionType\": \"ALL\"}}
                }]"
    ```

- Query the Global Secondary index
    ```
        aws dynamodb query --table-name Movie-data \
            --index-name releaseYearIndex \
            --key-condition-expression "releaseYear= :year" \
            --expression-attribute-values '{":year": {"S": "2020"}}' --output json
    ```