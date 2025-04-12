from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from transformers import Qwen2_5_VLForConditionalGeneration
from qwen_vl_utils import process_vision_info
import torch
import os




def get_model_processor(model_dir, device='cuda:0'):

    if any([_ in model_dir.lower() for _ in ['2vl', '2-vl']]):
        target_class = Qwen2VLForConditionalGeneration
    if any([_ in model_dir.lower() for _ in ['2.5vl', '2.5-vl']]):
        target_class = Qwen2_5_VLForConditionalGeneration


    model = target_class.from_pretrained(
        model_dir, 
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
    ).to(device)

    # default processer
    processor = AutoProcessor.from_pretrained(
        model_dir, 
        # # if not enough memory:
        # min_pixels=min_pixels, 
        # max_pixels=max_pixels,
    )

    return model, processor 




def get_response(image, question: str, model, processor, device='cuda:0'):
    messages = [
        {
            'role': 'system',
            'content': (
                "You are VL-Thinking🤔, a helpful assistant with excellent reasoning ability."
                " A user asks you a question, and you should try to solve it."
                " You should first think about the reasoning process in the mind and then provides the user with the answer."
                " The reasoning process and answer are enclosed within <think> </think> and"
                " <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think>"
                " <answer> answer here </answer>"
            )
        },
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": question},
            ],
        }
    ]
    # Preparation for inference
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to(device)

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=1000, do_sample=False, use_cache=True)
    torch.cuda.empty_cache()
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    # print(output_text)


    return output_text[0]





# model_dir = 'UCSC-VLAA/VLAA-Thinker-Qwen2VL-2B'
# model_dir = 'UCSC-VLAA/VLAA-Thinker-Qwen2VL-7B'
# model_dir = 'UCSC-VLAA/VLAA-Thinker-Qwen2VL-7B-Zero'

# model_dir = 'UCSC-VLAA/VLAA-Thinker-Qwen2.5VL-3B'
model_dir = 'UCSC-VLAA/VLAA-Thinker-Qwen2.5VL-7B'
device = 'cuda:0'
model, processor = get_model_processor(model_dir, device)



image = os.path.join('./assets/example_gen_func-func_polynomial_22134847_iynn.png')
res = get_response(
    image,
    'Determine the function.',
    model, 
    processor,
    device=device,
)

print(res)

