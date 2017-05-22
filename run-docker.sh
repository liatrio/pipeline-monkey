mkdir -p .monkey

docker build -t pipeline-monkey .

docker run \
  -v ~/.gitconfig:/root/.gitconfig \
  -v ~/.ssh/pipeline-monkey:/root/.ssh/id_rsa \
  -v ~/.ssh/known_hosts:/root/.ssh/known_hosts \
  -v $(pwd)/.monkey:/pipeline-monkey/.monkey \
  -v $(pwd)/config.json:/pipeline-monkey/config.json \
  liatrio/pipeline-monkey:initial python monkey.py $@
