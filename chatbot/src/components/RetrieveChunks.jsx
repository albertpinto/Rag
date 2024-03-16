import React, { useEffect, useState } from 'react'
import axios from 'axios'
import ChatChunks from './ChatChunks'

function RetrieveChunks({ query }) {
  const [isLoading, setIsLoading] = useState(false);
  const [serverUrl, setServerUrl] = useState("http://localhost:4044/search");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query) {
      setIsLoading(true);
      fetchData();
    }
  }, [query]);

  const fetchData = async () => {
    try {
      const url = `${serverUrl}/query=${query}`;
      console.log(url);

      const response = await axios.get(url, {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });

      const data = response.data;
      console.log(data);
      setResults(data.neighbours);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setIsLoading(false);
  };

  return (
    results.length > 0 && (
      <ChatChunks data={results} />
    )
  );
}

export default RetrieveChunks;
