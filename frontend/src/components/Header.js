import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <header className="bg-blue-600 text-white p-4">
            <h1 className="text-xl font-bold">FinTrust Guardian</h1>
            <nav>
                <ul className="flex space-x-4">
                    <li>
                        <Link to="/" className="hover:underline">Dashboard</Link>
                    </li>
                    <li>
                        <Link to="/audit" className="hover:underline">Audit Logs</Link>
                    </li>
                    <li>
                        <Link to="/policies" className="hover:underline">Policies</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;