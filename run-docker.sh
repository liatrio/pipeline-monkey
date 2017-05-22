docker build -t pipeline-monkey .

mkdir -p .monkey

docker run \
  -v ~/.gitconfig:/root/.gitconfig \
  -v ~/.ssh/pipeline-monkey:/root/.ssh/id_rsa \
  -v ~/.ssh/known_hosts:/root/.ssh/known_hosts \
  -v $(pwd)/.monkey:/pipeline-monkey/.monkey \
  -v $(pwd)/config.json:/pipeline-monkey/config.json \
  pipeline-monkey python monkey.py $@
