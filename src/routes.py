from flask import Flask,render_template,request
from src.tools.ineuronscrapper import scrapper
from src.tools.curriculumScrapper import curriculumScrapper
from src.logger import logger


app = Flask(__name__)

logger.info('flask application started')
iNeuron = scrapper("https://ineuron.ai")


@app.route('/home',methods=['GET'])
@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')



@app.route('/scrape',methods=['GET'])
def scrape():
    return render_template('scrapped.html',cat = iNeuron.course_categories())



@app.route('/courses' , methods=['POST'])
def course_list():
    ID=request.form['id']
    All = iNeuron.AllCourses()
    L=list()
      
    for name in All:
        if All[name]['categoryId'] == ID:
            L.append(name)

    return render_template('courses.html' , ID= ID , courseList= L)



@app.route('/<course_name>' , methods=['POST'])
def course_details(course_name):
    name=request.form['name']
    Details= iNeuron.AllCourses()
    return render_template('courseDetails.html',name=name, Details= Details[name])



@app.route('/<courseName>/curriculum',methods=['POST'])
def courseCurriculum(courseName):
    Scr = curriculumScrapper(courseName)
    data = Scr.scrape()
    name=courseName.replace('-',' ')
    return render_template('curriculum.html',name=name,data=data)