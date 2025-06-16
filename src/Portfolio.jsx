import React, { useState, useEffect } from "react";
import "./Navbar.css"; // Import your CSS styles
import linkedin from './linkedin.png'
import github from './github.png'
import myphoto from './my_pho.png'
import aboutme from './full_size_photo.jpg'
import menu from './menu.png'
import axios from "axios";
import gmail from './gmail.png'
import phone from './phone.png'
import leetcode from './leetcode.png'
import linkdown from './linked_down.png'
import git_down from './git_down.png'
import Project1 from './AI_not_replace.png'
import Project3 from './E-learning.png'
import Project2 from './Project2.png'
const projectsData= [
  {
    id: 1,
    Image:Project1,
    title: "AI Not Replace Human",
    description: "This website showcases AI tools and upcoming projects, emphasizing AI as a helper, not a job threat.",
    githubLink: "https://github.com/Santhoshraj2730/webhack",
    liveDemoLink: "https://ai-not-replace-human.netlify.app/",
  },
  {
    id: 2,
    Image:Project2,
    title: "Project Two",
    description: "A futuristic e-commerce interface with holographic displays, dynamic shopping carts, and a seamless shopping experience.",
    githubLink: "https://github.com",
    liveDemoLink: "https://live-demo.com",
  },
  {
    id: 3,
    Image:Project3,
    title: "Project Three",
    description: "This project allows voice-controlled coding for HTML, CSS, and JS, making web development hands-free and efficient.",
    githubLink: "https://github.com",
    liveDemoLink: "https://live-demo.com",
  },
];


const Profile = () => {
  const Experience = [
    {
      title: 'Web Development',
      description:
        'I build user-friendly web apps (like E-com,E-learning) and fun browser games using HTML/CSS, JavaScript. I focus on clean design and smooth interactions.',
      icon: '📱', // You can replace this with an actual icon component or image
    },
    {
      title: 'AI Base Web',
      description:
        'Experienced in AI-based web development, building voice-enabled portfolios and AI-powered code integration. Skilled in creating interactive websites that use voice assistance for a better user experience.',
      icon: '🤖', // Replace with an icon
    },
    {
      title: 'Python (DSA)',
      description:
        'Skilled in Python Data Structures and Algorithms, with a strong understanding of problem-solving and optimization. Experienced in writing efficient code for complex challenges.',
      icon: '💻', // Replace with an icon
    },
  ];
    const openResume = () => {
      window.open("./assets/resume-example.pdf");
    };
  
    const goToContact = () => {
      window.location.href = "https://www.linkedin.com/in/santhoshworkspace";
    };
  const [menuVisible, setMenuVisible] = useState(false);
  useEffect(() => {
    const synth = window.speechSynthesis;
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  
    if (!synth || !recognition) {
      console.warn("Speech synthesis or recognition API not supported in this browser.");
      return;
    }
  
    const speakText = (text) => {
      const utterance = new SpeechSynthesisUtterance(text);
      synth.speak(utterance);
    };
  
    speakText(
      "Welcome to the website. You can say Home, About Us, Services, projects, or Contact to navigate."
    );
  
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = "en-US";
  
    recognition.onresult = (event) => {
      const command = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
      const scrollToSection = (sectionId) => {
        document.getElementById(sectionId).scrollIntoView({ behavior: "smooth" });
      };
  
      if (command.includes("home")) {
        scrollToSection("home");
        speakText("Navigating to Home");
      } else if (command.includes("about")) {
        scrollToSection("about-us");
        speakText("Navigating to About Us");
      } else if (command.includes("services")) {
        scrollToSection("services");
        speakText("Navigating to Services");
      } else if (command.includes("projects")) {
        scrollToSection("projects");
        speakText("Navigating to projects");
      } else if (command.includes("contact")) {
        scrollToSection("contact");
        speakText("Navigating to Contact");
      } else if (command.includes("show menu")) {
        handleMenuToggle();
        speakText("Menu opened.");
      } else if (command.includes("close menu")) {
        setMenuVisible(false); // Ensure menu closes
        speakText("Menu closed.");
      }else if (command.includes("open github") || command.includes("open git")) {
        window.location.href = "https://github.com/Santhoshraj2730";
        speakText("Opening GitHub");
    }
    else if (command.includes("open linkedin")|| command.includes("open Contact")) {
      window.location.href = "https://www.linkedin.com/in/santhoshworkspace";
      speakText("Opening Linkedin");
  }else if (command.includes("open leetcode")) {
    window.location.href = "https://leetcode.com/u/Santhosharry2730/";
    speakText("Opening Leetcode");
}}
  
    recognition.start();
  
    return () => {
      recognition.stop();
    };
  }, []);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate required fields
    if (!formData.name.trim() || !formData.email.trim() || !formData.message.trim()) {
      alert("Please fill in all required fields!");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/store", formData);
      alert(response.data.message);
      setFormData({ name: "", email: "", subject: "", message: "" }); // Clear form fields
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("Failed to submit the form.");
    }
  }



  const handleMenuToggle = () => {
    setMenuVisible(!menuVisible);
  };
  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId).scrollIntoView({ behavior: "smooth" });
    setMenuVisible(false);
  };
  return (
    <>
      <header className="header">
        <nav className="nav container">
          <div className="nav__logo">My Portfolio</div>

          <div className={`nav__menu ${menuVisible ? "show-menu" : ""}`} id="nav-menu">
            <ul className="nav__list">
              <li>
                <button className="nav__link" onClick={() => scrollToSection("home")}>
                  Home
                </button>
              </li>
              <li>
                <button className="nav__link" onClick={() => scrollToSection("about-us")}>
                  About Us
                </button>
              </li>
              <li>
                <button className="nav__link" onClick={() => scrollToSection("services")}>
                  Services
                </button>
              </li>
              <li>
                <button className="nav__link" onClick={() => scrollToSection("projects")}>
                  projects
                </button>
              </li>
              <li>
                <button className="nav__link" onClick={() => scrollToSection("contact")}>
                  Contact
                </button>
              </li>
            </ul>
          </div>

          <div className="nav__actions">
            <button
              className="nav__toggle"
              id="nav-toggle"
              onClick={handleMenuToggle}
              aria-label="Toggle Menu"
            >
             <img src={menu} alt=""   className="icon" />
            </button>
          </div>
        </nav>
      </header>
      <section id="home">
        <h5>❗Important Note:</h5><h6>This portfolio is accessible through voice assistance for better performance. You can use simple commands, for example: if you want to open the menu box, say 'show menu,' or 
        if you want to learn more about me, say 'about me.'</h6>
   <section id="profile">
      <div className="section__pic-container">
        <img
          src={myphoto}
          alt="John Doe profile picture"
        />
      </div>
      <div className="section__text">
        <p className="section__text__p1">Hello, I'm</p>
        <h1 className="title">Santhosh Raj</h1>
        <p className="section__text__p2">Web Developer</p>
        <div className="btn-container">
          <button className="btn btn-color-2" onClick={openResume}>
            Download CV
          </button>
          <button className="btn btn-color-2" onClick={goToContact}>
            Contact Info
          </button>
        </div>
        <div id="socials-container">
          <img
            src={linkedin}
            alt="My LinkedIn profile"
            className="icon"
            onClick={() => window.location.href = "https://www.linkedin.com/in/santhoshworkspace"}
          />
          <img
            src={github}
            alt="My Github profile"
            className="icon"
            onClick={() => window.location.href = "https://github.com/Santhoshraj2730"}
          />
          <img
            src={leetcode}
            alt="My Github profile"
            className="icon"
            onClick={() => window.location.href = "https://leetcode.com/u/Santhosharry2730/"}
          />
        </div>
      </div>
    </section>
</section>
<section id="about-us">
<div className="fullform">
  <img
    src={aboutme}
    alt="Profile"
  />
  <div className="content">
    <h1>About Me</h1>
    <p>
    A passionate full-stack developer with expertise in front-end technologies like HTML, CSS, JavaScript, and React.js. Proficient in backend development using MySQL and experienced in API development with Python Flask. Strong problem-solving skills with a solid foundation in Python Data Structures and Algorithms (DSA), ensuring efficient and scalable solutions for web applications.
    </p>
    <div className="section skills active">
      <h3>Web Development</h3>
      <p>Web app Development</p>
      <h3>Python Developer</h3>
      <p>problem-solving skills</p>
    </div>
  </div>
</div>

  
</section>
<section id="services"><div className="services-section">
      <h1>Experience</h1>
      <div className="services-container">
        {Experience.map((Experience, index) => (
          <div className="service-box" key={index}>
            <div className="icon">{Experience.icon}</div>
            <h3>{Experience.title}</h3>
            <p>{Experience.description}</p>
          </div>
        ))}
      </div>
    </div></section>
<section id="projects">
<h1 className="prohead">Projects</h1>
<div className="projects-container">
      {projectsData.map((project) => (
        <div key={project.id} className="project-card">
          <img src={project.Image} alt={project.title} className="project-image" />
          <h3>{project.title}</h3>
          <p>{project.description}</p>
          <div className="button-group">
            <a href={project.githubLink} target="_blank" rel="noopener noreferrer">
              <button className="probutton">GitHub</button>
            </a>
            <a href={project.liveDemoLink} target="_blank" rel="noopener noreferrer">
              <button className="probutton">Live-Demo</button>
            </a>
          </div>
        </div>
      ))}
    </div>
</section>
<section id="contact">
<div className="contact-container">
      <div className="contact-info">
        <h2>
          Contact <span>Me</span>
        </h2>
        <p>
        Feel free to reach out for collaborations, web development projects, or tech discussions. Connect with me via email or LinkedIn to explore innovative solutions together!
        </p>
        <div className="contact-details">
          <div className="contact-icon">
        <img src={gmail} className="icon"></img>
          <p>
          ssanthoshraj2730@gmail.com
          </p></div>
          <div className="contact-icon">
          <p>
          <img src={phone} className="icon"></img>8610511996
          </p></div>
        </div>
        <div className="social-icons">
          <a href="#" className="icon facebook">
            <i className="fab fa-facebook-f"></i>
          </a>
          <a href="#" className="icon twitter">
            <i className="fab fa-twitter"></i>
          </a>
          <a href="#" className="icon instagram">
            <i className="fab fa-instagram"></i>
          </a>
          <a href="#" className="icon linkedin">
            <i className="fab fa-linkedin-in"></i>
          </a>
        </div>
      </div>
      <div className="contact-form">
      <form onSubmit={handleSubmit} className="form">
      <input
       className="form-input"
        type="text"
        name="name"
        placeholder="Enter Your Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      <input
        className="form-input"
        type="email"
        name="email"
        placeholder="Enter Your Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        className="form-input"
        type="text"
        name="subject"
        placeholder="Enter Your Subject"
        value={formData.subject}
        onChange={handleChange}
      />
      <textarea
        className="form-textarea"
        name="message"
        placeholder="Enter Your Message"
        value={formData.message}
        onChange={handleChange}
        required
      ></textarea>
      <button className="form-button"  type="submit">Submit</button>
        </form>
      </div>
    </div>
</section>
<div className="downuse">
<img
            src={linkdown}
            alt="My LinkedIn profile"
            className="icon"
            onClick={() => window.location.href = "https://www.linkedin.com/in/santhoshworkspace"}
          />
          <img
            src={git_down}
            alt="My LinkedIn profile"
            className="icon"
            onClick={() => window.location.href = "https://github.com/Santhoshraj2730"}
          />
          <img
            src={leetcode}
            alt="My LinkedIn profile"
            className="icon"
            onClick={() => window.location.href = "https://leetcode.com/u/Santhosharry2730/"}
          /><img
          src={linkedin}
          alt="My LinkedIn profile"
          className="icon"
          onClick={() => window.location.href = "https://linkedin.com/"}
        />
</div>
    </>
  );
};

export default Profile;
