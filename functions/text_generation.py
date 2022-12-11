def text_generation(text):

  from transformers import pipeline, set_seed
  generator = pipeline('text-generation', model='gpt2')

  set_seed(2022)

  text_list = generator(text, max_length=100, num_return_sequences=5)
  return text_list
