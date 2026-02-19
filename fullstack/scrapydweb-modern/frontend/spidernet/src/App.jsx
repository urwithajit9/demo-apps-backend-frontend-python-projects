import React, { useState, useEffect } from "react";

function App() {
  const JobList = () => {
    const [jobs, setJobs] = useState([]);

  function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(";");
    cookies.forEach((cookie) => {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") csrfToken = value;
    });
    return csrfToken;
  }

  const csrfToken = getCSRFToken();



  const scheduleSpider = (spiderName) => {
    fetch(`http://localhost:8000/scrapyd/schedule/${spiderName}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => console.log(data));
  };

  return (
    <div>
      <h1>Scrapyd Jobs</h1>
      <ul>
        {jobs.map((job) => (
          <li key={job.id}>
            {job.spider}: {job.status}
          </li>
        ))}
      </ul>
      <button onClick={() => scheduleSpider("Quotes")}>Schedule Spider</button>
    </div>
  );
}

export default App;
