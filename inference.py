from transformers import GPT2Tokenizer, GPT2LMHeadModel
from dataset import clean
import re

def load_tokenizer_model():
    model_name="ChatbotCheckpoint"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.eval()
    tokenizer=GPT2Tokenizer.from_pretrained(model_name)
    tokenizer.pad_token=tokenizer.eos_token
    return tokenizer,model

def generate_answer(query):
    tokenizer,model=load_tokenizer_model()
    inputs = tokenizer.encode(query, return_tensors='pt')
    attention_mask = (inputs != tokenizer.pad_token_id).long() 
    outputs =model.generate(inputs, attention_mask=attention_mask, max_length=100, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def inference(query):
    query=clean(query)
    answer = generate_answer(query)
    modified_answer = re.sub(query, "", answer)
    answer=modified_answer.strip()
    return answer

