import {Link, Outlet} from "react-router-dom"
import logo from "../media/HH-logo.png"

const Layout = () => {
  return (
    <>
      <header className="bg-gray-800 text-white flex items-center justify-between p-4">
        <div className="max-w-7x1 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-6">
            <div className="flex items-center space-x-4">
            <img src={logo} alt="HalfHashed logo" className="h-8 w-8" />  
            <h1 className="text-x1 font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400">HalfHashed </h1>
                <nav className="ml-10 flex space-x-4">
                    <Link to="/" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                    Home
                    </Link>

                    <Link to="/view" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                    View Block
                    </Link>

                    <Link to="/addblock" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                    Add Block
                    </Link>
                </nav>
            </div>
          </div>
        </div>
    
      </header>
      <main className="flex-grow">
        <Outlet />
      </main>

      <footer className="fixed bottom-0 w-full p-2 bg-gray-800 text-white">
        <p className="text-center"> 
          <a className='hover:bg-yellow-600 p-1 rounded-md' href="https://github.com/Koshelenkoa/sf-hacks24"> Github Link</a>
        </p>
      </footer>
    </>
  );
};

export default Layout;
