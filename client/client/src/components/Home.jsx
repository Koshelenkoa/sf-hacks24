import React from "react";

const Home = () => {
  return (
    <>
      <div className="flex flex-col h-screen">
        <div className="max-w-md mx-auto">
          <div className="flex flex-col mb-4">
            <label htmlFor=""></label>
            <input type="text" className="border p-2" />
          </div>

          <div className="flex flex-col mb-4">
            <label htmlFor=""></label>
            <input type="text" className="border p-2" />
          </div>

          <div className="flex flex-col mb-4">
            <label htmlFor=""></label>
            <input type="text" className="border p-2" />
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
