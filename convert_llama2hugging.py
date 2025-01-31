import torch
from colorama import Style, Fore, Back
from transformers import AutoTokenizer, LlamaConfig, LlamaForCausalLM
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format=f'{Style.BRIGHT}{Fore.GREEN}%(levelname)s:%(asctime)s{Style.RESET_ALL} {Fore.BLUE}%(message)s{Style.RESET_ALL}', 
    level=logging.INFO
)

local_dir = "/mnt/d/Desktop/HuggingFaceModels/meta-llama/"
model_name = "Llama3.2-1B/"

tokenizer = AutoTokenizer.from_pretrained(local_dir + model_name)
state_dict = torch.load(local_dir + model_name + "consolidated.00.pth", \
                        map_location=torch.device('cpu'))
# Load the model configuration.
config = LlamaConfig.from_pretrained(local_dir + model_name + "config.json")
# Initialize the model with the configuration
'''
Doesn't work, downloads some big model. 
'''
model = LlamaForCausalLM(config)
# Load the model weights
model.load_state_dict(state_dict)
# Save the model and configuration
config.save_pretrained(local_dir + model_name)
model.save_pretrained(local_dir + model_name)
