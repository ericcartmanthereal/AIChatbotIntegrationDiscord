from google.cloud import aiplatform

service_account = './ai-integration-discord-3e92ac634b2d'
client_options = aiplatform.gapic.EndpointServiceAsyncClientOptions(
    client_certs=service_account
)
endpoint = aiplatform.gapic.EndpointServiceAsyncClient(client_options=client_options)
model = aiplatform.gapic.PredictionServiceAsyncClient(client_options=client_options)
