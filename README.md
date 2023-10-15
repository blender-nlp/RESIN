# RESIN
A Schema-guided Multi-document Event Extraction, Tracking, Prediction, and Visualization for News Articles
This repository holds the latest version of RESIN's system in DARPA KAIROS project.

## Instructions
### Data Preprocessing
As required by KAIROS evaluation, the input document clusters should be represented in LDC format. An example piece of data (two document clusters ) in this format are available at this [link](https://drive.google.com/file/d/1iZ16bOHo4_3H2xYykNxEOsu5QyMwojZ1/view?usp=share_link). We also provide easy-to-use python scripts to transform a document cluster from a much cleaner JSON format to the LDC format.

#### How to transform a document cluster into the LDC format?
First, install related python dependencies (`nltk`, `jieba`, and `docker-compose`) by running:
```
pip install -r requirements.txt
```
Then, you can go to the `preprocess` folder and run the following commands to get an LDC formatted dataset:
```
python transform_format.py --input_file [PATH_TO_A_DOC_CLUSTER] --name [CLUSTER_NAME] --output_dir [OUTPUT_DIR]
```
Here, the input document clusters should be formatted in JSON, where each key is the ID of the document and each value is the document text. An example is:
```
{
    "doc_1": "hello world!",
    "doc_2": "This is a test document cluster."
}
```
For the other two command-line arguments, you can use any name you want for your `CLUSTER_NAME` and the preprocessed dataset is generated under `OUTPUT_DIR`.

### Setup the APIs
1. Specify the `${KAIROS_LIB}` dir (to store intermediate results and outputs) at https://github.com/RESIN-KAIROS/RESIN-pipeline2023/blob/084bb05d6e2cd6d84bebe79bb22777a8cc7d367f/docker-compose.yaml#L8
2. Go to `${KAIROS_LIB}` and then run `./create_folders.sh` to create the folders for inputs and outputs. 
3. Set up the device number for each GPU-based component, e.g.,https://github.com/RESIN-KAIROS/RESIN-pipeline2023/blob/084bb05d6e2cd6d84bebe79bb22777a8cc7d367f/docker-compose.yaml#L38 NOTE: Running the whole pipeline typically needs at least 3*16GB GPUs.
4. Start the APIs by running: `docker-compose up`. It could be pretty slow when you set up the APIs for the first time, since docker-compose needs to pull all the dockers from dockerhub before running it.
5. Put the data folder (LDC formatted) under `{KAIROS_LIB}/resin/resin/input/` and put the schema library (JSON files) under `{KAIROS_LIB}/resin/resin/schemas/resin` (some example schema files can be found at https://github.com/RESIN-KAIROS/schemalib/tree/main/phase2b/curated)

### Run the Pipeline
After successfully setting up the APIs and put the data and schema files under the correct path, you can make a POST request to the main API to start processing:
```
curl -X POST --header "Content-Type: application/json" -d '{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "runId": "my_run_id", "sender": "string", "time": "2020-11-25T03:34:48.008Z", "content": {"data": "Example source document content here."}, "contentUri": "input/[DATA_FOLDER_NAME]"}' http://0.0.0.0:10100/kairos/entrypoint
```
Note that you need to specify the path to your data in `contentUri`. The pipeline will start processing and store all intermediate results and final outputs under `persist/my_run_id`.
