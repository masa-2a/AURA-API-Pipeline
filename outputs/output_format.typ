#let json = json("test_no_prompt.json")

= Aggregated outputs



== Structure:

each prompt will be assigned a unique id. Followed by the ID and the prompt itself, will be the outputs each model gave in response to that prompt.

#for key in json.keys() [
  
  == Prompt information:

  - Prompt id: #key\  
  - Prompt: #json.at(key).at("prompt")\
  - Category: #json.at(key).at("category")\
  - Risk Level: #json.at(key).at("risk_level")\
  == Model Responses:\

  #for model in json.at(key).at("outputs").keys() [
    === #model:\

    *Model emotion classifier*: #json.at(key).at("outputs").at(model).at("emotion")
    
    *AI Risk Assessment*: #json.at(key).at("outputs").at(model).at("ai_risk_assessment")
    
    *Should Continue*: #json.at(key).at("outputs").at(model).at("should_continue")
    
    *Classification*: #json.at(key).at("outputs").at(model).at("classification")
    
    #json.at(key).at("outputs").at(model).at("response")

  ]
  
]
