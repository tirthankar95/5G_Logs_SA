import glob
import logging
import random
logger = logging.getLogger(__name__)
logging.basicConfig(
    format=f'%(levelname)s:%(message)s', 
    level=logging.INFO
)

template_logs = [
    "Downlink Throughput: 1024 kbps",
    "Downlink Throughput: 2048 kbps",
    "Uplink Throughput: 1024 kbps",
    "Uplink Throughput: 2048 kbps",
    "UE 1 - RACH Process: success",
    "UE 1 - RACH Process: unsuccessful",
    "UE 0 - RACH Process: success",
    "UE 2 - RACH Process: unsuccessful ",
    "UE 0 - Connection Status: connected",
    "UE 0 - Connection Status: connected",
    "UE 1 - Connection Status: disconnected",
    "UE 1 - Connection Status: disconnected"
]

def get_latest_version():
    filenames = glob.glob("../*.txt")
    versions = []
    prefix = "/5G_logs_v"
    for filename in filenames:
        versions.append(int(filename.split(".")[2][len(prefix):]))
    versions.sort()
    return versions[-1]

latest = get_latest_version() + 1
NUMBER_OF_SENTENCE = 100000
indices = [random.randint(0, len(template_logs)-1) for _ in range(NUMBER_OF_SENTENCE)]
with open(f"5G_logs_v{latest}.txt", "a") as txt_file:
    for index in indices:
        print(template_logs[index], file = txt_file)