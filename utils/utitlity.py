import streamlit as st



def load_css(file_path:str) -> None:
    """
    The function `load_css` reads a CSS file and injects its contents into an HTML file.
    :param file_path: The `file_path` parameter in the `load_css` function is a string that represents
    the path to the CSS file that you want to load and inject into an HTML document. This function reads
    the content of the CSS file and embeds it within a `<style>` tag in the HTML document
    """
    with open(file_path,'r') as f:
        st.html(f'<style>{f.read()}</style>')

# def cmToinche(cm:float) -> float:
#     """
#     The function `cmToinche` converts centimeters to inches by dividing by 2.54 and rounding to the
#     nearest whole number.
    
#     :param cm: The parameter `cm` in the `cmToinche` function represents the length in centimeters that
#     you want to convert to inches
#     :type cm: float
#     :return: An integer value representing the conversion of centimeters to inches is being returned.
#     """
#     return round(cm/2.54,2)

def shapeIdentifiyer(bust:float, waist:float , hip:float, by:str = "inches") -> str:
    """
    The function `shapeIdentifiyer` determines a person's body shape based on their bust, waist, and hip
    measurements.
    
    :param bust:
    :type bust: int
    :param waist:
    :type waist: int
    :param hip:
    :type hip: int
    :return: a string that represents the shape of a person based on their bust, waist, and hip measurements. The possible return values are "Rectangle", "Hourglass", "Apple", "Inverted triangle", or "Pear" depending on the conditions specified in the function.
    """
    if by.lower() == "inches":
        if abs(bust-hip)<=3:
            if 3>=hip-waist>=-1:
                return "Rectangle"
            else:
                if hip-waist>3:
                    return "Hourglass"
                else:
                    return "Apple"
        else:
            if bust>hip:
                if hip-waist < -1:
                    return "Apple"
                else:
                    return "Inverted triangle"
            else:
                if hip-waist < -1:
                    return "Apple"
                else:
                    return "Pear"
    elif by.lower() == "cm":
        if abs(bust-hip)<=7.62:
            if 7.62>=min(hip,bust)-waist>-5.08:
                return "Rectangle"
            else:
                if min(hip,bust)-waist>-7.62:
                    return "Hourglass"
                else:
                    return "Apple"
        else:
            if bust>hip:
                if bust-waist < -2.54:
                    return "Apple"
                else:
                    return "Inverted triangle"
            else:
                if hip-waist < -2.54:
                    return "Apple"
                else:
                    return "Pear"
                
def predictShape(img)->str:
    """
    The `predictShape` function takes an image file path, preprocesses the image, loads a pre-trained
    ResNet50 model for body shape classification, makes predictions on the image, and returns the
    predicted body shape label.
    
    :param img_path: The function `predictShape` takes in the file path of an image as input. It then
    loads a pre-trained model for shape classification, preprocesses the image, makes predictions using
    the model, and returns the predicted shape label for the input image
    :type img_path: str
    :return: The `predictShape` function returns the predicted shape label of the input image specified
    by the `img_path` parameter. The predicted shape label is determined by using a pre-trained ResNet50
    model for body shape classification. The function preprocesses the input image, makes predictions
    using the model, and then decodes the predictions to obtain the human-readable class label
    corresponding to the predicted shape. The predicted shape
    """
    from keras.models import load_model # type: ignore
    import cv2
    import numpy as np
    from constants import MODEL

    def preprocessing(image):
        image = cv2.resize(image, (224, 224))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1.4)
        edges_3_channel = cv2.merge([blurred_image, blurred_image, blurred_image])
        return edges_3_channel

    # Load the model
    model = load_model(MODEL)

    # # Load an image file that you want to test
    # img = cv2.imread(img_path)

    # Apply the preprocessing function
    processed_img = preprocessing(img)

    # Expand dimensions to match the input shape expected by the model
    img_array = np.expand_dims(processed_img, axis=0)

    # Make predictions
    predictions = model.predict(img_array)

    # Decode the predictions
    predicted_class = np.argmax(predictions, axis=1)

    # Assuming you have a list of class labels
    class_labels = ["apple", "pear", "rectangle", "inverted triangle", "hourglass"]

    # Get the human-readable class label
    predicted_label = class_labels[predicted_class[0]]
    
    return predicted_label


# if __name__=="__main__":
#     print(predictShape(r"assests\test3.jpg"))