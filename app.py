import logging
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image
from Code import CNN_Model
from flask_cors import CORS

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
cors = CORS(app)

# Initialize the CNN model and generate plots
object = CNN_Model()
#make model ready to use
object.TrainModel()
# img=object.fig2img("./uploads/test.jpg")
# print(img)
# plot1, plot2, plot3, plot4 = object.TrainModel()
# plot1_img = secure_filename("plot1.png")
# plot2_img = secure_filename("plot2.png")
# plot3_img = secure_filename("plot3.png")
# plot4_img = secure_filename("plot4.png")
# plot1.save(os.path.join('uploads', plot1_img))
# plot2.save(os.path.join('uploads', plot2_img))
# plot3.save(os.path.join('uploads', plot3_img))
# plot4.save(os.path.join('uploads', plot4_img))
print("CNN model and plots initialized")
# logging.info("CNN model and plots initialized")


@app.route('/')
def index():
    return 'Flask server running...'


# @app.route('/api/classify_image', methods=['POST'])
# def classify_image():
#     logging.info("Received a POST request to classify_image endpoint")
#     # Check if the POST request has the file part
#     if 'file' not in request.files:
#         logging.error("No file part in the POST request")
#         return jsonify({'error': 'No file part'})
#     file = request.files['file']
#     # Check if the file is one of the allowed file types
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join('uploads', filename))
#         output = object.classifyImage(os.path.join('uploads', filename))
#         os.remove(os.path.join('uploads', filename))
#         logging.info("Image classification completed successfully")
#         return jsonify({'output': output})
#     else:
#         logging.error("File type not allowed")
#         return jsonify({'error': 'File type not allowed'})
@app.route('/upload_image', methods=['POST'])
def upload_image():
    # logging.info("Received a POST request to upload_image endpoint")
    print("Received a POST request to upload_image endpoint")
    try:
        # get the uploaded image from the request body
        image = request.files['image']
        print(image.filename)
        # create a new file name for the uploaded image
        filename = secure_filename(image.filename)

        # save the image to the server
        image.save(os.path.join('uploads', filename))
        #evaluate the image using the CNN model
        object.fileDialog(os.path.join('uploads', filename))
        print(object.output)
        
        # os.remove(os.path.join('uploads', filename))
        print("Image uploaded successfully")
        return jsonify({'output': object.output})

    except Exception as e:
        # logging.error(f"Error occurred during image upload: {str(e)}")
        print(f"Error occurred during image upload: {str(e)}")
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    
    if(app.run(host='0.0.0.0',port=5001)):
        print("server uis running")
