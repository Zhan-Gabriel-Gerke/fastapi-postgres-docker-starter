# script to run the tests
docker-compose --profile test --env-file .env.test run --rm web pytest