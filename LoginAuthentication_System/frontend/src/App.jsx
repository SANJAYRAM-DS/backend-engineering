import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { VerifyEmail } from './pages/VerifyEmail';
import { PasswordReset } from './pages/PasswordReset';
import { Dashboard } from './pages/Dashboard';
import { ActiveSessions } from './pages/ActiveSessions';
import { RbacAdmin } from './pages/RbacAdmin';
import { AuditLogs } from './pages/AuditLogs';

const MainContent = () => {
  const { user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState(user ? 'dashboard' : 'login');

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: 'var(--text-muted)' }}>
        Loading Authentication Subsystem...
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', paddingBottom: '40px' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main style={{ padding: '0 20px' }}>
        {!user && activeTab === 'login' && <Login setActiveTab={setActiveTab} />}
        {!user && activeTab === 'register' && <Register setActiveTab={setActiveTab} />}
        {activeTab === 'verify-email' && <VerifyEmail setActiveTab={setActiveTab} />}
        {activeTab === 'password-reset' && <PasswordReset setActiveTab={setActiveTab} />}
        {user && activeTab === 'dashboard' && <Dashboard />}
        {user && activeTab === 'sessions' && <ActiveSessions />}
        {user && activeTab === 'rbac' && <RbacAdmin />}
        {user && activeTab === 'audit' && <AuditLogs />}
        {!user && (activeTab === 'dashboard' || activeTab === 'sessions' || activeTab === 'rbac' || activeTab === 'audit') && (
          <Login setActiveTab={setActiveTab} />
        )}
      </main>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <MainContent />
    </AuthProvider>
  );
}
