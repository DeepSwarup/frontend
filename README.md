#Overview
This is a web-based Face Recognition Attendance System that captures images from a webcam, detects faces, and marks attendance. The application displays the recent attendance entries in a table format. It is built with React for the frontend and communicates with a backend server (assumed to be implemented) via RESTful APIs.

#Features
Capture images from a webcam for face recognition.
Display recent attendance entries in a table.
Responsive design for different screen sizes.
Stylish and professional UI with a dark theme.
#Prerequisites
Node.js and npm installed on your system.
Backend server running locally (assumed to be at http://localhost:5000).

##Folder Structure
src/: Contains the source code for the React application.
App.js: Main component that includes webcam capture and attendance table.
App.css: Styles for the application.
##Code Explanation
App.js
useRef to reference the webcam component.
useState to manage state for capturing images and attendance entries.
useEffect to fetch recent attendance entries on component mount.
capture function to handle capturing images from the webcam.
sendFrames function to send captured images to the backend for recognition.
Fetches and displays the recent attendance entries in a table.
App.css
Styles for the application, including layout, colors, and responsiveness.
Dark theme with stylish and professional UI elements.
License
This project is licensed under the MIT License.

Author
Developed by Deep Swarup.
