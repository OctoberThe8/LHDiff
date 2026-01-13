import os
import re
import json
import time
import torch
import warnings
import argparse
from pathlib import Path
from transformers import pipeline
from few_shot.five_shot import shot_five
from few_shot.chat_history import chat_history
from few_shot.chat_shot import ChatFewShot
from few_shot.base_shot import BaseModelFewShot
from metrics.sentence_similarity import cos_similarity, load_embedding_model
from metrics.Rouge_n import rouge_n
from metrics.count_score import count_score_by_topic
from transformers.generation.utils import LogitsProcessorList
from transformers.generation.logits_process import LogitsProcessor
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline,AutoModel


# 忽略所有 UserWarning 类型的警告
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser(description="LLMs Security Evaluation")
parser.add_argument("--output_dir",type=str,default="./logs",help="Specify the output directory.")
parser.add_argument("--datas",type=str,default="./datas/AI-EN-80.json",help="path of questions.")
parser.add_argument("--chat",action="store_true",default=False,help="Evaluate on chat model.")
# parser.add_argument("--binary_clsfy",action="store_true",default=False,help="binary classfication")
# parser.add_argument("--multi_clsfy",action="store_true",default=False,help="multi classfication")
# parser.add_argument("--Sub_QA",action="store_true",default=False,help="Subjective question answer")
parser.add_argument("--embedding_model_path",type=str,default="/home/nfs/U2020-ls/WACX/weights/bge-m3",help="path of embedding model.")

parser.add_argument("--shot", type=int, help="number of few shot", default=5)
parser.add_argument("--weight_path",type=str,default="/home/nfs/U2020-ls/WACX/weights",help="path of llm weights")
parser.add_argument("--rouge_n", type=int, help="rouge n", default=3)
parser.add_argument("--threshold", type=float, help="threshold of similarity", default=0.75)
parser.add_argument("--device", type=int, help="number of few shot", default=0)
parser.add_argument("-m","--model",type=str,required=True,help="Specify the model.")
parser.add_argument("-d","--debug",action="store_true",default=False,help="Help to debug.")

args = parser.parse_args()
torch.cuda.set_device(args.device)
device = torch.device("cuda")
result = []

class InvalidScoreLogitsProcessor(LogitsProcessor):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        if torch.isnan(scores).any() or torch.isinf(scores).any():
            scores.zero_()
            scores[..., 5] = 5e4
        return scores

def load_dataset(data_path: str)->list:

    with open(data_path, 'r') as f:
        datas = json.load(f)
    return datas

def load_locl_base_model(model_id: str):

    
    root_path = args.weight_path
    model_path = os.path.join(root_path,model_id)
    print(model_path)
    if args.model in ["BlueLM-7B-Chat"]:
        # from modelscope import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True, ignore_mismatched_sizes=True)
        model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True, ignore_mismatched_sizes=True).to(device)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True, ignore_mismatched_sizes=True)
        model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True, ignore_mismatched_sizes=True).to(device)
    return model,tokenizer
    # pass

def base_model_eval(model, tokenizer, datas,args):

    if args.model in ["CodeLlama-7b-hf"]:
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=10,device=args.device,batch_size=1,pad_token_id=model.config.eos_token_id)
        # pipe.tokenizer.pad_token_id = 2
    else:
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=10,device=args.device,batch_size=1)

    if args.model in ["Qwen-7B"]:
        pipe.tokenizer.pad_token_id = model.config.eos_token_id
        print("Set pad_token_id")
    ###############################################################################
    if args.debug:

        print("{}模型测试成功！".format(args.model))
        with open("./models.txt", 'a', encoding='utf-8') as file:
            model_name = ""
            model_name += args.model + "\n"
            file.write(model_name)  
        return
    ###############################################################################
    
    for data in datas:
        # if args.binary_clsfy:
        if data["mission_class"] == "binary":
            few_shot = BaseModelFewShot(data, args.shot)
            llm_input = few_shot.binary_clsfy_shot()

            inputs = tokenizer([llm_input], return_tensors="pt")
            inputs = inputs.to(model.device)
            logits_processor = LogitsProcessorList()
            logits_processor.append(InvalidScoreLogitsProcessor())
            gen_kwargs = {"num_beams": 1, "do_sample": False, "max_new_tokens": 1,
                            "logits_processor": logits_processor}
            if args.model in ["CodeLlama-7b-hf"]:
                outputs = model.generate(**inputs, return_dict_in_generate=True, output_scores=True, **gen_kwargs, pad_token_id=2)
            else:
                outputs = model.generate(**inputs, return_dict_in_generate=True, output_scores=True, **gen_kwargs)
            score = outputs.scores[0][0].tolist()
            import numpy as np
            yes_id = tokenizer("YES").input_ids[-1]
            no_id = tokenizer("NO").input_ids[-1]

            choice_score = [score[yes_id], score[no_id]]

            if choice_score[0] >= choice_score[1]:
                data["llm_answer"] = "YES"
            else:
                data["llm_answer"] = "NO"
            data["score"] = int(
                data["llm_answer"].lower() == data["answer"].lower()
            )
            result.append(data)            
        
        # if args.multi_clsfy:
        if data["mission_class"] == "multi":
            few_shot = BaseModelFewShot(data, args.shot)
            llm_input = few_shot.multi_clsfy_shot()

            llm_outputs = pipe(llm_input)
            for llm_output in llm_outputs:
                generated_text = llm_output["generated_text"]

                data["llm_input"] = llm_input
                data["llm_output"] = generated_text
                print(generated_text)
                # positions = [i for i in range(len(generated_text)) if generated_text.startswith("Answer", i)]
                # index = positions[args.shot-1]
                # print(generated_text[index:])

                # print(len(re.findall(r"Answer: ([A-D]+)", generated_text)), re.findall(r"Answer: ([A-D]+)", generated_text), data["id"])
                print(len(re.findall(r"Answer[\s\S]*?([A-D]+)", generated_text)), re.findall(r"Answer[\s\S]*?([A-D]+)", generated_text), data["id"])
                print("#"*100)
                if len(re.findall(r"Answer[\s\S]*?([A-D]+)", generated_text)) > args.shot:
                    data["llm_answer"] = re.findall(r"Answer[\s\S]*?([A-D]+)", generated_text)[-1]
                    data["score"] = int(
                        data["llm_answer"].lower() == data["answer"].lower()
                    )
                else:
                    data["llm_answer"] = "None"
                    data["score"] = 0
                result.append(data)
    return result

def chat_model_eval(model, tokenizer, datas,args):

    flag = False
    for data in datas:
        # if args.binary_clsfy:
        if data["mission_class"] == "binary":
            chat_few_shot = ChatFewShot(data,args.shot)
            history = chat_few_shot.binary_clsfy_shot()
            question = "Codes: "+data['question']
            response, history = model.chat(tokenizer, question , history=history)
            data["llm_input"] = question
            data["llm_output"] = response
            print(data["id"], response)

            matches = re.findall(r"YES|NO", response)
            print(len(matches), matches)
            print("#"*100)
            if len(matches) == 0:

                data["llm_answer"] = None
                data["score"] = 0
            else:
                data["llm_answer"] = matches[0]
                data["score"] = int(
                    data["llm_answer"].lower() == data["answer"].lower()
                )
            result.append(data)
            
        if data["mission_class"] == "multi":
            chat_few_shot = ChatFewShot(data,args.shot)
            history = chat_few_shot.multi_clsfy_shot()
            question = "Question: "+data['question']+" ".join(data["choices"])
            response, history = model.chat(tokenizer, question , history=history)
            data["llm_input"] = question
            data["llm_output"] = response
            print(data["id"], response)
            ans_nums = len(re.findall(r"Answer[\s\S]*?([A-D]+)", response))
            # print(len(re.findall(r"Answer: ([A-D]+)", response)), re.findall(r"Answer: ([A-D]+)", response))
            print(len(re.findall(r"Answer[\s\S]*?([A-D]+)", response)), re.findall(r"Answer[\s\S]*?([A-D]+)", response))
            print("#"*100)
            if(ans_nums == 0):
                data["llm_answer"] = "None"
                data["score"] = 0
            else:
                data["llm_answer"] = re.findall(r"Answer[\s\S]*?([A-D]+)", response)[-1]
                data["score"] = int(
                    data["llm_answer"].lower() == data["answer"].lower()
                )
            result.append(data)

        if data["mission_class"] == "sub_qa":

            # chat_few_shot = ChatFewShot(data,args.shot)
            if flag == False:
                embedding_model = load_embedding_model(args.embedding_model_path)
                flag = True

            history = []
            question = data['question']
            response, history = model.chat(tokenizer, question , history=history)
            data["llm_input"] = question
            data["llm_output"] = response
            print("response:", response)
            similarity = cos_similarity(embedding_model, [response], [data['answer']])
            # rouge_x = rouge_n(response, data['answer'], args.rouge_n)
            print(data["id"], similarity, rouge_x)
            print("#"*30)

            if(similarity < args.threshold):
                data["llm_answer"] = "None"
                data["score"] = 0
            else:
                data["llm_answer"] = response
                data["score"] = 1
            result.append(data)
    return result


def main():


    datas = load_dataset(args.datas)
    # if args.debug:
    #     print("True")
    model, tokenizer = load_locl_base_model(args.model)



    if args.chat:
        result = chat_model_eval(model, tokenizer, datas,args)
    else:
        result = base_model_eval(model, tokenizer, datas,args)

    if len(result)==0:
        print("Result为空")
        return
    score_fraction, score_float = count_score_by_topic(result)

    # count_score_by_topic(data)
    result_with_score = {
        "score_fraction": score_fraction,
        "score_float": score_float,
        "detail": result,
    }

    output_path = (
        Path(args.output_dir)
        / f"{Path(args.datas).stem}_{os.path.basename(args.model)}_{str(args.shot)}_shot.json"
    )
    with open(output_path, "w") as f:
        json.dump(result_with_score, f, indent=4)
    
if __name__ == "__main__":
    main()