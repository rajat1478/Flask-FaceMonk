#pip install flask opencv-python
from flask import Flask, jsonify,render_template,request,flash
import os
import cv2
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}   

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def processImg(filename,operation):
    print(f"the operation is {operation} and file name is {filename}")

    #read an image from uploads folder:
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "gray":
            gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f"static/{filename}",gray_img)
        case detect:
            
            #create a cascade classifier 
            face_cascade=cv2.CascadeClassifier('C:\\Users\\Rajat arya\\Desktop\\haarcascade_frontalface_default.xml')
            gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            #search for coordinates
            faces = face_cascade.detectMultiScale(gray_img, scaleFactor = 1.05 , minNeighbors = 5)

            for x,y,w,h in faces :
                img = cv2.rectangle(img , (x,y) , (x+w , y+h) , (255 , 0 , 0) , 5)
            cv2.imwrite(f"static/{filename}",img)
    
            


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/doc')
def doc():
    return render_template("doc.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/edit', methods=['POST'])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selection file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImg(filename, operation)
            flash(f"Your image has been processed and is available <a href='/static/{filename}' target='_blank'>here</a>")
            #return redirect(url_for('download_file', name=filename))
    
    return render_template("index.html")


if __name__ =='__main__':
    app.run(debug=True, port = 5001)