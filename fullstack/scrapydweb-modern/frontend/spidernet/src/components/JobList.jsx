import React, { useState, useEffect } from "react";

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

  useEffect(() => {
    fetch("http://localhost:8000/scrapyd/jobs/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setJobs(data);
        } else {
          console.error("Expected an array but received:", data);
        }
      })
      .catch((error) => console.error("Error fetching jobs:", error));
  }, []);

  return (
    <div>
      {jobs.length > 0 ? (
        jobs.map((job) => <div key={job.id}>{job.title}</div>)
      ) : (
        <p>No jobs available.</p>
      )}
    </div>
  );
};

export default JobList;
