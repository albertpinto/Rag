import React from "react";
import PropTypes from "prop-types";
function ChatChunks({ data, borderColor, bgColor, txtColor}) {
    return (
        <div className="bg-white w-200 pl-5 pb-5 p5 rounded-lg shadow-md">
          <div className="flex xs:flex-col sm:flex-row flex-wrap gap-2">
            {data.map((item, index) => (
              <div
                className={`p-2 w-96 h-96  border-spacing-2 border-8 border-cyan-500 rounded-2xl shadow-2xl`}
                key={index}
              >
                <strong>Search Rank:</strong> {index + 1} <br />
                <strong>Score:</strong> {item[2]} <br />
                <p><strong>Chunk: </strong> {item[1]}</p>
              </div>
            ))}
          </div>
        </div>
      );
}
ChatChunks.defaultProps = {
    bgColor: "bg-gray-700",
    txtColor: "text-black",
    shdColor: "shadow-bg-zinc-950",
    labelColor: "text-gray-700",
  };
  
  ChatChunks.propTypes = {
    bgColor: PropTypes.string,
    txtColor: PropTypes.string,
    shdColor: PropTypes.string,
    labelColor: PropTypes.string,
    borderColor: PropTypes.string,
  };
export default ChatChunks;


