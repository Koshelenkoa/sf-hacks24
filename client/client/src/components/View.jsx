import React, { useState, useEffect} from 'react';
import ViewBlockDetails from './ViewBlockDetails';

const View = () => {
    
    const [blocks, setBlocks] = useState([]);
    const [visibleBlocks, setVisibleBlocks] = useState([]);
    const [nextIndex, setNextIndex] = useState(0);
    const blockSize = 5; // number of blocks to display at single time
    

    // load blockchain data on mount
    useEffect(() => {
      // where we would fetch data from server but importing for now
      import("../blockchain_data/blockchain.json")
        .then((data) => {
          const reversedData = data.default.slice().reverse(); // Assuming the data is the default export
          setBlocks(reversedData);
          setVisibleBlocks(reversedData.slice(0, blockSize));
          setNextIndex(blockSize);
        })
        .catch((error) => console.log(error));
    }, []);

    const loadMoreBlocks = () => {
        const nextBlocks = blocks.slice(nextIndex, nextIndex + blockSize);
        setVisibleBlocks([...visibleBlocks, ...nextBlocks]);
        setNextIndex(nextIndex + blockSize);
    }

    

    return (
        <div className="flex flex-col h-screen">
    
          <div className="flex-grow overflow-auto p-4">
            <div className="max-w-4xl mx-auto">
              {visibleBlocks.map((block, index) => (
                <ViewBlockDetails key={block.hash} block={block} />
              ))}
              {nextIndex < blocks.length && (
                <div className="flex justify-center mt-4">
                  <button
                    onClick={loadMoreBlocks}
                    className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                  >
                    Load More
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      );
}

export default View;