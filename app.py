from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson import Binary
import hashlib
import base64
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://ssanthoshraj2730:Kavi102109@cluster1.wxmubv4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["Profolio"]
collection = db["SmallPhoto"]

@app.route('/Smallimage', methods=['POST'])
def upload_smallphoto():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    # Generate a unique identifier for the image
    image_hash = hashlib.sha256(image_data).hexdigest()
    
    # Store the image in MongoDB
    collection.insert_one({
        "hash": image_hash,
        "data": Binary(image_data),
        "filename": "myphoto",  # Fixed filename for easy retrieval
        "content_type": image_file.content_type
    })
    
    return jsonify({
        "message": "Smallphoto uploaded successfully",
        "image_id": image_hash
    })
@app.route('/get-smallimage/<image_id>', methods=['GET'])
def get_image(image_id):
    # Find the image by its hash or filename
    findimage = collection.find_one({"$or": [{"hash": image_id}, {"filename": image_id}]})
    
    if not findimage:
        return jsonify({"error": "Image not found"}), 404
    
    # Return the image directly as binary data with proper content type
    return send_file(
        BytesIO(findimage["data"]),
        mimetype=findimage.get("content_type", "image/png"),
        as_attachment=False
    )

@app.route('/fullphoto',methods=['POST'])
def post_fullphoto():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    image_file = request.files['image']
    image_data = image_file.read()
    image_hash = hashlib.sha256(image_data).hexdigest()

    collection.insert_one({
        "hash":image_hash,
        "data":Binary(image_data),
        "filename":"Fullsizephone",
        "content_type":image_file.content_type
    })

    return jsonify({
         "message": "Smallphoto uploaded successfully",
         "image_id": image_hash
    })

@app.route('/get_largeimage/<image_id>',methods=['GET'])
def get_fullsizeimage(image_id):
    findimage = collection.find_one({"$or":[{"hash":image_id},{"filename":image_id}]})  # Fixed typo here
    if not findimage:
       return jsonify({"error": "Image not found"}), 404
    return send_file(
        BytesIO(findimage["data"]),
        mimetype=findimage.get("content_type", "image/png"),
        as_attachment=False
    )
@app.route('/upload-resume',methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return  jsonify({"error":"No resume uploaded"}),400
    resume_file = request.files['resume']
    resume_data = resume_file.read()
    resume_hash = hashlib.sha256(resume_data).hexdigest()

    collection.delete_many({"filename":"resume.pdf"})

    collection.insert_one({
        "hash":resume_hash,
        "data":Binary(resume_data),
        "filename":"resume.pdf",
        "content_type":resume_file.content_type
    }) 
    return jsonify({
        "message": "Resume uploaded successfully",
        "resume_id": resume_hash
    })

@app.route('/download-resume', methods=['GET'])
def download_resume():
    resume_doc = collection.find_one({"filename": "resume.pdf"})
    if not resume_doc:
        return jsonify({"error": "Resume not found"}), 404

    return send_file(
        BytesIO(resume_doc["data"]),
        mimetype=resume_doc.get("content_type", "application/pdf"),
        as_attachment=True,
        download_name="SanthoshRaj_Resume.pdf"
    )
@app.route('/upload-about',methods=['POST'])
def upload_para():
    about=request.get_json()
    if not about or 'paragraph' not in about:
        return jsonify({"error":"Paragrah"}),400
    collection.delete_many({"type":"para"})

    collection.insert_one({
        "type":"para",
        "content":about['paragraph']
    })
    return jsonify({"message": "Paragraph uploaded successfully"})

@app.route('/get-para', methods=['GET'])
def get_para():
    para_doc = collection.find_one({"type": "para"})
    if not para_doc:
        return jsonify({"error": "Paragraph not found"}), 404

    return jsonify({"paragraph": para_doc['content']})

# Add to your existing Flask routes
@app.route('/upload-skills', methods=['POST'])
def upload_skills():
    skills_data = request.get_json()
    if not skills_data or 'skills' not in skills_data:
        return jsonify({"error": "Skills data required"}), 400
    
    collection.delete_many({"type": "skills"})
    
    # Store each skill with its description
    for skill in skills_data['skills']:
        collection.insert_one({
            "type": "skills",
            "title": skill['title'],
            "description": skill['description']
        })
    
    return jsonify({"message": "Skills uploaded successfully"})

@app.route('/get-skills', methods=['GET'])
def get_skills():
    skills_docs = list(collection.find({"type": "skills"}))
    if not skills_docs:
        return jsonify({"error": "Skills not found"}), 404
    
    skills = [{"title": doc['title'], "description": doc['description']} for doc in skills_docs]
    return jsonify({"skills": skills})

@app.route('/upload-experience', methods=['POST'])
def post_experience():
    experience = request.get_json()
    if not experience or 'experience' not in experience:
        return jsonify({"error": "Frontend request missing"}), 400
    
    # Clear existing experiences
    collection.delete_many({"type": "experience"})
    
    # Insert new experiences
    for exp in experience['experience']:
        collection.insert_one({
            "type": "experience",
            "Companyname": exp['Companyname'],
            "ExperienceDetails": exp['ExperienceDetails']
        })
    
    return jsonify({"message": "Experience uploaded successfully"})

@app.route('/get-experience', methods=['GET'])
def get_experience():
    experiences = list(collection.find({"type": "experience"}))
    if not experiences:
        return jsonify({"error": "Experience not found"}), 404
    
    # Return the correct field names that match what you stored
    experience_list = [{
        "Companyname": doc['Companyname'],
        "ExperienceDetails": doc['ExperienceDetails']
    } for doc in experiences]
    
    return jsonify({"experiences": experience_list})
projects = []
@app.route('/upload-project', methods=['POST'])
def upload_project():
    try:
        # Initialize variables
        title = ''
        description = ''
        github_link = ''
        live_demo_link = ''
        image_base64 = ''
        
        # Check if request is JSON
        if request.is_json:
            data = request.get_json()
            title = data.get('title', '')
            description = data.get('description', '')
            github_link = data.get('githubLink', '')
            live_demo_link = data.get('liveDemoLink', '')
            image_base64 = data.get('imageBase64', '')
        else:
            # Handle form-data
            title = request.form.get('title', '')
            description = request.form.get('description', '')
            github_link = request.form.get('githubLink', '')
            live_demo_link = request.form.get('liveDemoLink', '')
            
            # Handle file upload
            image_file = request.files.get('image')
            if image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Validate required fields
        if not all([title, description, github_link, live_demo_link]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate project ID (you might want to use MongoDB's auto ID instead)
        project_id = str(len(projects) + 1)
        
        # Store in MongoDB
        project_data = {
            "type": "project",
            "id": project_id,
            "title": title,
            "description": description,
            "githubLink": github_link,
            "liveDemoLink": live_demo_link,
            "image": image_base64
        }
        
        collection.insert_one(project_data)
        
        return jsonify({
            'message': 'Project uploaded successfully',
            'project': {
                'id': project_id,
                'title': title,
                'description': description,
                'githubLink': github_link,
                'liveDemoLink': live_demo_link
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/get-projects', methods=['GET'])
def get_projects():
    try:
        projects = list(collection.find({"type": "project"}))
        if not projects:
            return jsonify({"error": "No projects found"}), 404
        
        projects_list = []
        for project in projects:
            projects_list.append({
                "id": project['id'],
                "title": project['title'],
                "description": project['description'],
                "githubLink": project['githubLink'],
                "liveDemoLink": project['liveDemoLink'],
                "imageBase64": project['image']  # Make sure this matches your storage field
            })
        
        return jsonify({"projects": projects_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':

    app.run(debug=True)