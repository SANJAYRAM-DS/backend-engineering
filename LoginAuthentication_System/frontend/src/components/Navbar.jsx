import React from 'react';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, LogOut, User, Key, Monitor, Activity, ShieldAlert } from 'lucide-react';

export const Navbar = ({ activeTab, setActiveTab }) => {
  const { user, logout } = useAuth();

  return (
    <nav className="glass-card" style={{ borderRadius: '0 0 16px 16px', marginBottom: '24px', padding: '16px 28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }} onClick={() => setActiveTab('dashboard')}>
          <div style={{ padding: '8px', background: 'rgba(99, 102, 241, 0.2)', borderRadius: '10px', display: 'flex' }}>
            <ShieldCheck size={26} color="#6366f1" />
          </div>
          <div>
            <h1 style={{ fontSize: '18px', fontWeight: '800', letterSpacing: '-0.02em', background: 'linear-gradient(135deg, #fff 0%, #a5b4fc 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              SentinelAuth
            </h1>
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '500' }}>Enterprise AuthN & AuthZ</span>
          </div>
        </div>

        {user && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button 
              className={`btn-secondary ${activeTab === 'dashboard' ? 'badge-indigo' : ''}`}
              onClick={() => setActiveTab('dashboard')}
              style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <User size={16} /> Dashboard
            </button>

            <button 
              className={`btn-secondary ${activeTab === 'sessions' ? 'badge-indigo' : ''}`}
              onClick={() => setActiveTab('sessions')}
              style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Monitor size={16} /> Sessions
            </button>

            <button 
              className={`btn-secondary ${activeTab === 'audit' ? 'badge-indigo' : ''}`}
              onClick={() => setActiveTab('audit')}
              style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Activity size={16} /> Audit Logs
            </button>

            <button 
              className={`btn-secondary ${activeTab === 'rbac' ? 'badge-indigo' : ''}`}
              onClick={() => setActiveTab('rbac')}
              style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <ShieldAlert size={16} /> RBAC
            </button>
          </div>
        )}

        <div>
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-main)' }}>{user.email}</div>
                <div style={{ fontSize: '11px', color: '#a5b4fc', fontWeight: '500' }}>
                  {user.is_superuser ? 'Superuser' : (user.roles?.join(', ') || 'Standard User')}
                </div>
              </div>
              <button className="btn-secondary" onClick={logout} title="Logout" style={{ padding: '8px 12px' }}>
                <LogOut size={16} color="#fb7185" />
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', gap: '8px' }}>
              <button className="btn-secondary" onClick={() => setActiveTab('login')}>Login</button>
              <button className="btn-primary" onClick={() => setActiveTab('register')}>Register</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};
