MODEL = r'ml/model/resnet50_body_shape_classification_model_3.keras'
BEST_MODEL = r'ml/model/best_model_3.keras'
NO_COLS = 4
RECOMMENDATION_CONTAINER = 400
URL = "https://me.meshcapade.com/editor"

result = 'pear'

def updateResult(shape:str):
    """
    The function `updateResult` updates the global variable `result` with the value of the input
    parameter `shape`.
    
    :param shape: The `updateResult` function takes a parameter `shape` of type `str`. This function
    updates a global variable `result` with the value of the `shape` parameter
    :type shape: str
    """
    global result
    result = shape