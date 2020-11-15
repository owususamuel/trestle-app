
import cv2
from flask import Flask, request, render_template, jsonify
from matplotlib import pyplot
from mtcnn import MTCNN

app = Flask(__name__)

ACCEPTED_VIDEO_FORMAT = ['avi', 'mp4', 'mov']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'avi', 'mp4', 'mov'])
UPLOAD_FOLDER = 'app/static/uploads/'
stream = None
detections = None
frame = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route('/camera',methods=['POST'])
def camera():
    cap=cv2.VideoCapture(0)
    while True:
        ret,img=cap.read()
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/frontend/images/placeholder.png",img)

        # return render_template("camera.html",result=)
        time.sleep(0.1)
        return json.dumps({'status': 'OK', 'result': "static/frontend/images/placeholder.png"})
        if cv2.waitKey(0) & 0xFF ==ord('q'):
            break
    cap.release()
    # file="/home/ashish/Downloads/THOUGHT.png"
    # with open(file,'rb') as file:
    #     image=base64.encodebytes(file.read())
    #     print(type(image))
    # return json.dumps({'status': 'OK', 'user': user, 'pass': password});
    return json.dumps({'status': 'OK', 'result': "static/frontend/images/placeholder.png"});

def gen(camera):
    while True:
        data= camera.get_frame()

        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        error = 'No Image Found!'
        return jsonify({"error": error}), 400

    file = request.files['file']
    if file.filename == '':
        error = 'No image selected for uploading'
        return jsonify({"error": error}), 400

    if file and allowed_file(file.filename):

        # load image from file
        pixels = pyplot.imread(file)
        # create the detector, using default weights
        detector = MTCNN()
        # detect faces in the image
        faces = detector.detect_faces(pixels)
        # display faces on the original image
        # draw_image_with_boxes(file, faces)
        return jsonify({"faces": len(faces)})

    else:
        error = 'Allowed image types are -> png, jpg, jpeg'
        return jsonify({"error": error}), 400

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=105)
    app.run()
