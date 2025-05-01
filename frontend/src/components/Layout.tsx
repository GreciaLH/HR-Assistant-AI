import React, { ReactNode } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const router = useRouter();

  const isActive = (path: string) => {
    return router.pathname === path ? 'bg-primary-700 text-white' : 'text-gray-300 hover:bg-primary-600 hover:text-white';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-primary-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-white font-bold text-xl">HR Assistant</span>
              </div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <Link href="/" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/')}`}>
                    Inicio
                  </Link>
                  <Link href="/job-descriptions" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/job-descriptions')}`}>
                    Vacantes
                  </Link>
                  <Link href="/resumes" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/resumes')}`}>
                    Currículums
                  </Link>
                  <Link href="/matching" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/matching')}`}>
                    Coincidencias
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;