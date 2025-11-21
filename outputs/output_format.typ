#let json = json("test_no_prompt.json")

= Aggregated outputs



== Structure:

each prompt will be assigned a unique id. Followed by the ID and the prompt itself, will be the outputs each model gave in response to that prompt.

#for key in json.keys() [
  
  == Prompt information:

  - Prompt id: #key\  
  - Prompt: #json.at(key).at("prompt")\
  - Category: #json.at(key).at("category")\
  == Model Responses:\

  #for model in json.at(key).at("outputs").keys() [
    === #model:\

    *Model emotion classifier*: #json.at(key).at("outputs").at(model).at("emotion")
    
    #json.at(key).at("outputs").at(model).at("response")

  ]
  
]
