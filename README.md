# model-hosting-example
![Interaction with model frontend.](./ba_02_prod.gif)
This monorepo contains code for a web application which allocates Cloud Run containers for running and maintaining a dialogue between two `gpt3` bots. It is used as material for my [engineering blog](https://medium.com/ramate). 

## Running
To really understand and experience what this is doing use the ./bin/gcloud.sh scripts for `services/model-runtime` and `services/model-sidecar`. Set your `TF_VAR_model_runtime_container` environment variable for `services/model-sidecar` to your GCR container for the runtime. Set your `CONTAINER_IMAGE` environmental variable for `services/model-deployer` to your GCR container for `services/model-runtime`.

All services can be run by `python run.py` in their respective directory or starting images built from their `Dockefiles`.

Call `npm run` or `yarn run` for the `fronts/web`.

**Warning:** I advise against sending a version of this application live in any way. OpenAI usage would very costly.

### `./fronts`
Contains all of the frontends. Right now there's only web.

### `./services`
Contains all backend services: `services/model-deployer`, `services/model-runtime`, and `services/model-sidecar`.

### `./infra`
Empty for now. Lz.