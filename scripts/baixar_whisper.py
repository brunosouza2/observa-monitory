import argparse
from huggingface_hub import snapshot_download
parser = argparse.ArgumentParser()
parser.add_argument('--model', choices=['base', 'small'], default='base')
args = parser.parse_args()
snapshot_download(f'Systran/faster-whisper-{args.model}', local_dir=f'models/whisper-{args.model}', allow_patterns=['config.json','model.bin','tokenizer.json','vocabulary.*'])
