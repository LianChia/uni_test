# Installation

## Use python env
```
conda create --name cvat-fastapi python=3.9
```

```
conda activate cvat-fastapi
```

Install requirements
```
pip install -r requirements.txt
```

## Logging in huggingface
Input the huggingface token
```
huggingface-cli login
```

## Pull new file to update [Optional]

Pull the huggingface repo
```
cd ./src/huggingface
```
```
git clone https://huggingface.co/spaces/smartsurgery/smartsurgery-dentistry-models-Demo
```
Copy the file to the fastapi
```
copy ./src/huggingface/Smartsurgery_Dentistry_Models_Demo/dental_measure_utils.py src/dental_measure/utils.py
```

```
copy ./src/huggingface/Smartsurgery_Dentistry_Models_Demo/dental_measure.py src/dental_measure/main.py
```

## Download model from huggingface
After loggin with token, run the download scipt

```
python src/scripts/download.py
```


## Run app

run uvicorn or run main.py
```
python main.py
```

