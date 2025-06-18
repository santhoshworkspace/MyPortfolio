from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson import Binary
import hashlib
import base64
from io import BytesIO
import smtplib

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

from PIL import Image
import io

@app.route('/upload-experience', methods=['POST'])
def post_experience():
    try:
        # Initialize variables
        company_name = ''
        experience_details = ''
        company_image_base64 = ''
        
        # Check if request is JSON or form-data
        if request.is_json:
            data = request.get_json()
            company_name = data.get('Companyname', '')
            experience_details = data.get('ExperienceDetails', '')
            company_image_base64 = data.get('companyImage', '')
        else:
            # Handle form-data
            company_name = request.form.get('Companyname', '')
            experience_details = request.form.get('ExperienceDetails', '')
            
            # Handle image file upload
            image_file = request.files.get('companyImage')
            if image_file:
                # Resize the image to icon size (e.g., 64x64)
                img = Image.open(image_file)
                img.thumbnail((64, 64))  # Resize while maintaining aspect ratio
                
                # Convert to base64
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                company_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Validate required fields
        if not all([company_name, experience_details]):
            return jsonify({"error": "Company name and experience details are required"}), 400
        
        # Store in MongoDB
        experience_data = {
            "type": "experience",
            "Companyname": company_name,
            "ExperienceDetails": experience_details
        }
        
        if company_image_base64:
            experience_data["companyImage"] = company_image_base64
        
        collection.insert_one(experience_data)
        
        return jsonify({"message": "Experience uploaded successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-experience', methods=['GET'])
def get_experience():
    try:
        experiences = list(collection.find({"type": "experience"}))
        if not experiences:
            return jsonify({"error": "Experience not found"}), 404
        
        # Convert MongoDB documents to JSON-serializable format
        experience_list = []
        for exp in experiences:
            experience_data = {
                "Companyname": exp['Companyname'],
                "ExperienceDetails": exp['ExperienceDetails']
            }
            if 'companyImage' in exp:
                experience_data["companyImage"] = exp['companyImage']
            experience_list.append(experience_data)
        
        return jsonify({"experiences": experience_list})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
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
    
@app.route('/Uploadcontactlinks', methods=['POST'])
def Uploadlink():
    try:
        links = ''
        linkimages = ''

        if request.is_json:
            data = request.get_json()
            links = data.get('Links', '')
            linkimages = data.get('Linkimages', '')
        else:
            links = request.form.get('Links', '')
            image_file = request.files.get('Linkimages')
            if image_file:
                linkimages = base64.b64encode(image_file.read()).decode('utf-8')

        if not all([links, linkimages]):
            return jsonify({'error': 'Missing required fields'}), 400

        link_id = str(collection.count_documents({"type": "LinksData"}) + 1)

        LinksData = {
            "type": "LinksData",
            "id": link_id,
            "links": links,
            "linkimage": linkimages
        }

        collection.insert_one(LinksData)
        return jsonify({'message': 'Link uploaded successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/get-contactlinks', methods=['GET'])
def get_contactlinks():
    try:
        links = list(collection.find({"type": "LinksData"}))
        return jsonify({
            "links": [{
                "id": l["id"],
                "link": l["links"],
                "imageBase64": l["linkimage"]
            } for l in links]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/form', methods=['POST'])
def handle_form():
    try:
        # Get form data
        first_name = request.form.get("first_name")
        user_email = request.form.get("user_email")
        textarea = request.form.get("textarea")
        subject = request.form.get("subject", "No Subject")  # Default if subject not provided
        
        # Validate required fields
        if not all([first_name, user_email, textarea]):
            return jsonify({"error": "Missing required fields"}), 400

        # Email configuration - using YOUR email as both sender and receiver
        sender_email = "ssanthoshraj2730@gmail.com"
        receiver_email = "ssanthoshraj2730@gmail.com"  # Changed to your email
        password = "xelp pjux vkme zjzz"  # Your app password
        
        # Create more detailed message
        message = f"""\
Subject: New Contact Form Submission - {subject}

From: {first_name} <{user_email}>

Message:
{textarea}
"""
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
        
        return jsonify({"message": "Email sent successfully"}), 200
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({"error": "Failed to send email"}), 500

@app.route('/upload-contact-info', methods=['POST'])
def upload_contact_info():
    try:
        # Get data from request
        email = request.form.get('email')
        phone = request.form.get('phone')
        email_image = request.files.get('email_image')
        phone_image = request.files.get('phone_image')

        if not all([email, phone]):
            return jsonify({"error": "Email and phone required"}), 400

        # Prepare image data
        email_image_data = base64.b64encode(email_image.read()).decode('utf-8') if email_image else None
        phone_image_data = base64.b64encode(phone_image.read()).decode('utf-8') if phone_image else None

        # Delete existing contact info
        collection.delete_many({"type": "contact_info"})

        # Insert new contact info
        contact_data = {
            "type": "contact_info",
            "email": email,
            "phone": phone
        }
        
        if email_image_data:
            contact_data["email_image"] = email_image_data
        if phone_image_data:
            contact_data["phone_image"] = phone_image_data

        collection.insert_one(contact_data)
        
        return jsonify({"message": "Contact info uploaded successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-contact-info', methods=['GET'])
def get_contact_info():
    try:
        contact_info = collection.find_one({"type": "contact_info"})
        if not contact_info:
            return jsonify({"error": "Contact info not found"}), 404
        
        response = {
            "email": contact_info.get('email'),
            "phone": contact_info.get('phone')
        }
        
        if 'email_image' in contact_info:
            response["email_image"] = contact_info['email_image']
        if 'phone_image' in contact_info:
            response["phone_image"] = contact_info['phone_image']
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Add these routes to your existing Flask app

@app.route('/upload-menu-icon', methods=['POST'])
def upload_menu_icon():
    """Endpoint to upload the menu icon"""
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    # Generate a unique identifier for the image
    image_hash = hashlib.sha256(image_data).hexdigest()
    
    # Delete any existing menu icon first
    collection.delete_many({"filename": "menu-icon"})
    
    # Store the image in MongoDB
    collection.insert_one({
        "hash": image_hash,
        "data": Binary(image_data),
        "filename": "menu-icon",  # Fixed filename for easy retrieval
        "content_type": image_file.content_type
    })
    
    return jsonify({
        "message": "Menu icon uploaded successfully",
        "image_id": image_hash
    })

@app.route('/get-menu-icon', methods=['GET'])
def get_menu_icon():
    """Endpoint to retrieve the menu icon"""
    # Find the menu icon by its filename
    menu_icon = collection.find_one({"filename": "menu-icon"})
    
    if not menu_icon:
        return jsonify({"error": "Menu icon not found"}), 404
    
    # Return the image directly as binary data with proper content type
    return send_file(
        BytesIO(menu_icon["data"]),
        mimetype=menu_icon.get("content_type", "image/png"),
        as_attachment=False
    )    

if __name__ == '__main__':

    app.run(debug=True)