import React, { useState } from 'react';

const ViewBlockDetails = ({block}) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="bg-white p-6 shadow rounded-lg mb-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Block #{block.index}</h3>
          <p className="text-sm">Timestamp: {block.timestamp}</p>
          <p className="text-sm">Previous Block: {block.previous_hash}</p>
          <p className="text-sm">Hash: {block.hash}</p>
        </div>
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-300"
        >
          {showDetails ? 'Hide Details' : 'View Details'}
        </button>
      </div>
      {showDetails && (
        <div className="mt-4 overflow-auto max-h-60">
          <h4 className="text-md font-semibold mb-2">Transactions</h4>
          {block.transactions.map((tx, idx) => (
            <div key={idx} className="mb-2 p-2 rounded bg-gray-100">
              <p>Sender: {tx.sender}</p>
              <p>Recipient: {tx.recipient}</p>
              <p>Amount: {tx.amount}</p>
              <p>Timestamp: {tx.timestamp}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
 
export default ViewBlockDetails;