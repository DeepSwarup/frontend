import React, { useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import './App.css';

const App = () => {
  const webcamRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [attendanceEntries, setAttendanceEntries] = useState([]);

  // Function to fetch recent attendance entries
  const fetchAttendanceEntries = () => {
    axios.get('http://localhost:5000/recent-attendance')
      .then((response) => {
        // Reverse the order of entries to display recent ones first
        setAttendanceEntries(response.data.reverse());
      })
      .catch((error) => {
        console.error('Error fetching attendance:', error);
      });
  };

  // Fetch recent attendance entries on component mount
  useEffect(() => {
    fetchAttendanceEntries();
  }, []);

  const capture = async () => {
    if (!capturing) {
      setCapturing(true);
      let capturedFrames = [];
      const interval = setInterval(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        capturedFrames.push(imageSrc);
        if (capturedFrames.length >= 5) {
          clearInterval(interval);
          setCapturing(false);
          sendFrames(capturedFrames);
        }
      }, 500);
    }
  };

  const sendFrames = async (capturedFrames) => {
    const formData = new FormData();
    capturedFrames.forEach((frame, index) => {
      fetch(frame)
        .then((res) => res.blob())
        .then((blob) => {
          formData.append('images', blob, `capture${index}.jpg`);
          if (index === capturedFrames.length - 1) {
            axios.post('http://localhost:5000/recognize', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            })
              .then((response) => {
                alert(response.data.message);
                fetchAttendanceEntries(); // Refresh attendance entries after marking
              })
              .catch((error) => {
                if (error.response) {
                  alert(error.response.data.error);
                } else if (error.request) {
                  alert('No response received from the server.');
                } else {
                  alert('Error', error.message);
                }
              });
          }
        })
        .catch((error) => {
          console.error('Error fetching image:', error);
        });
    });
  };

  return (
    <div>
      <header className="header">
        Face Recognition Attendance System
      </header>
      <div className="main-content">
        <div className="container">
          <div className="webcam-container">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="webcam"
            />
            <div className="button-container">
              <button onClick={capture} disabled={capturing}>
                {capturing ? 'Capturing...' : 'Capture Photo'}
              </button>
            </div>
          </div>
          <div className="attendance-table">
            <h2>Recent Attendance Entries</h2>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Date</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {attendanceEntries.slice(0, 6).map((entry, index) => (
                  <tr key={index}>
                    <td>{entry.Name}</td>
                    <td>{entry.Date}</td>
                    <td>{entry.Time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <footer className="footer">
        © 2024 Developer - Deep Swarup
      </footer>
    </div>
  );
};

export default App;
