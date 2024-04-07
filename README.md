# Tech Spec

Start writing things here

# Run the code 

```bash
docker network create elastic
docker run -d --rm --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.12.2

```