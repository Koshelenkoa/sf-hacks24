import React from "react";
import { Link } from "react-router-dom";
import big_logo from "../media/HH-logo-wide.png"

const Home = () => {
  return (
    <div className="flex flex-col h-screen ">
      <div className="container mx-auto px-6 md:px-12 xl:px-24">
        <div className="hero-section text-center p-12 md:p-24">
          <img src={big_logo} alt="Main logo" className="mx-auto md:h-40"/>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-6 bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-yellow-600">
            Transforming Business Operations with Blockchain
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            Discover a new era of transparency and efficiency by leveraging our blockchain solutions to track every step of your product's journey.
          </p>
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-3">Why Trust Us?</h2>
            <p className="text-gray-600">
              We empower your business with secure and verifiable transactions.
            </p>
          </div>
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-3">Benefits for Your Business</h2>
            <ul className="list-disc list-inside text-gray-600">
              <li>Streamlined supply chain tracking from production to point-of-sale.</li>
              <li>Improved inventory management with real-time data.</li>
              <li>Enhanced trust in business practices for employees and partners.</li>
            </ul>
          </div>
          <div className="call-to-action">
            <Link to="/addBlock" className="bg-yellow-600 text-white font-bold py-3 px-6 rounded hover:bg-yellow-700 transition duration-300">
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
