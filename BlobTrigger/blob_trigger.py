import logging
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="myblob", path="samples/{name}", connection="AzureWebJobsStorage")
def blob_trigger(myblob: func.InputStream) -> None:
    logging.info(f'Blob trigger processed blob: {myblob.name}, Size: {myblob.length} bytes')