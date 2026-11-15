"""Obtain selected official ZIP entries, checking HTTP ranges, size and CRC."""
import argparse,struct,zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
URL='https://zenodo.org/records/13305826/files/videos.zip'
parser=argparse.ArgumentParser();parser.add_argument('--videos',nargs='+',default=['PM_000','PM_039']);args=parser.parse_args()
targets={f'Ex1/{v}-Camera17-30fps.mp4' for v in args.videos}
out=Path('data/samples');out.mkdir(parents=True,exist_ok=True)
def fetch(start,end):
    response=requests.get(URL,headers={'Range':f'bytes={start}-{end}'},timeout=180)
    response.raise_for_status()
    if response.status_code!=206 or len(response.content)!=end-start+1:raise RuntimeError('Invalid HTTP range response')
    return response.content
head=requests.head(URL,timeout=30);head.raise_for_status();size=int(head.headers['Content-Length'])
tail=fetch(max(0,size-65536),size-1);pos=tail.rfind(b'PK\x05\x06')
if pos<0:raise RuntimeError('ZIP directory not found')
eocd=struct.unpack_from('<4s4H2LH',tail,pos);directory=fetch(eocd[6],eocd[6]+eocd[5]-1)
entries=[];pos=0
while pos<len(directory):
    e=struct.unpack_from('<4s6H3L5H2L',directory,pos)
    if e[0]!=b'PK\x01\x02':raise RuntimeError('Invalid ZIP directory')
    name=directory[pos+46:pos+46+e[10]].decode('utf-8');pos+=46+e[10]+e[11]+e[12]
    if name in targets:entries.append((name,e))
if {name for name,e in entries}!=targets:raise RuntimeError('Missing selected entries')
def download(item):
    name,e=item;target=out/Path(name).name
    if target.exists() and target.stat().st_size==e[9] and zlib.crc32(target.read_bytes())==e[7]:
        print('Verified existing:',target,flush=True);return
    h=struct.unpack('<4s5H3L2H',fetch(e[16],e[16]+29));start=e[16]+30+h[9]+h[10]
    data=fetch(start,start+e[8]-1)
    if e[4]==8:data=zlib.decompress(data,-15)
    elif e[4]!=0:raise RuntimeError('Unsupported compression')
    if len(data)!=e[9] or zlib.crc32(data)!=e[7]:raise RuntimeError('Integrity failure')
    target.write_bytes(data);print('Downloaded:',target,len(data),flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(download,entries))
for name in ['Segmentation.csv','Segmentation.txt']:
    response=requests.get(f'https://zenodo.org/records/13305826/files/{name}',timeout=60);response.raise_for_status();(out/name).write_bytes(response.content)
