import {Link, Outlet} from "react-router-dom"

const Layout = () => {
  return (
    <>
      <header className="bg-gray-800 text-white flex items-center justify-between p-4">
        <div className="max-w-7x1 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-6">
            <div className="flex items-center">
            <h1 className="text-x1 font-bold">Blockchain App</h1>
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
        <div className="py-10">
            <Outlet />
        </div>
      </main>

      <footer className="p-4 bg-gray-800 text-white">
        <p className="text-center"> Footer </p>
      </footer>
    </>
  );
};

export default Layout;
