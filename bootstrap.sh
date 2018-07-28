docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)

echo 'Setting env variable...'
export REACT_APP_USERS_SERVICE_URL=http://127.0.0.1:5001

wait
echo 'Building containers...'
docker-compose -f docker-compose-dev.yml build


wait
echo 'Install local packages...'
cd services/client && npm install

wait
cd ../..
echo 'Recreating Database...'
docker-compose -f docker-compose-dev.yml run users-service python manage.py recreate_db

wait
echo 'Seeding database...'
docker-compose -f docker-compose-dev.yml run users-service python manage.py seed_db


echo 'Spinning up containers...'
docker-compose -f docker-compose-dev.yml up
