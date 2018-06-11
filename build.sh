export REACT_APP_USERS_SERVICE_URL=http://127.0.0.1:5001


env=$1
command=""

if [[ "${env}" == "nocache" ]]; then
  command="docker-compose -f docker-compose-dev.yml build --no-cache"
else
  command="docker-compose -f docker-compose-dev.yml build"
fi

echo "Running command: {$command}"

$command
