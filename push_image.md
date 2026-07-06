# Push image to 
```bash
docker build -t danda-ci .
docker tag danda-ci ghcr.io/shalabi67/danda-ci:latest
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
docker push ghcr.io/shalabi67/danda-ci:latest
```