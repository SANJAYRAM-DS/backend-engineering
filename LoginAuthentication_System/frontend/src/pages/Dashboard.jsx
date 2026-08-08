import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api';
import { User, Shield, Key, RefreshCw, CheckCircle2, Copy, AlertTriangle } from 'lucide-react';

export const Dashboard = () => {
  const { user, accessToken, refreshToken, refreshProfile } = useAuth();
  const [rotatedTokens, setRotatedTokens] = useState(null);
  const [rotationError, setRotationError] = useState(null);
  const [rotating, setRotating] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleTestRTR = async () => {
    setRotating(true);
    setRotationError(null);
    try {
      const res = await api.post('/auth/refresh', {
        refresh_token: refreshToken
      });
      setRotatedTokens(res.data);
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token);
      await refreshProfile();
    } catch (err) {
      setRotationError(err.response?.data?.message || 'Token rotation failed.');
    } finally {
      setRotating(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!user) return null;

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }} className="animate-fade-in">
      {/* Header Banner */}
      <div className="glass-card" style={{ padding: '28px 32px', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <span className="badge badge-emerald" style={{ marginBottom: '8px' }}>
              <CheckCircle2 size={12} /> Identity Authenticated
            </span>
            <h2 style={{ fontSize: '24px', fontWeight: '800' }}>Welcome, {user.first_name || 'User'} {user.last_name || ''}!</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '2px' }}>
              UUID: <code style={{ color: '#818cf8', fontSize: '13px' }}>{user.id}</code>
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <span className="badge badge-indigo" style={{ padding: '6px 12px', fontSize: '13px' }}>
              <Shield size={14} /> {user.is_superuser ? 'Superuser Admin' : 'Authenticated Principal'}
            </span>
          </div>
        </div>
      </div>

      {/* Grid Specs */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
        {/* Profile Card */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <User size={18} color="#6366f1" /> Principal Claims
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Email Address:</span>
              <span style={{ fontWeight: '600' }}>{user.email}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Email Verified:</span>
              <span>{user.is_email_verified ? <span className="badge badge-emerald">Verified</span> : <span className="badge badge-amber">Unverified</span>}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Staff Privilege:</span>
              <span>{user.is_staff ? <span className="badge badge-emerald">True</span> : <span className="badge badge-indigo">False</span>}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Assigned Roles:</span>
              <span style={{ fontWeight: '600', color: '#34d399' }}>{user.roles?.length ? user.roles.join(', ') : 'Default User'}</span>
            </div>
          </div>
        </div>

        {/* RTR Engine Test Card */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <RefreshCw size={18} color="#06b6d4" /> Refresh Token Rotation (RTR) Engine
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>
            Test single-use refresh token exchange. Old refresh tokens are consumed; re-presenting an old token triggers instant family revocation!
          </p>

          {rotationError && (
            <div style={{ padding: '10px 12px', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', borderRadius: '8px', color: '#fb7185', fontSize: '12px', marginBottom: '12px', display: 'flex', gap: '6px' }}>
              <AlertTriangle size={16} /> {rotationError}
            </div>
          )}

          <button className="btn-primary" onClick={handleTestRTR} disabled={rotating} style={{ width: '100%' }}>
            <RefreshCw size={16} className={rotating ? 'animate-spin' : ''} />
            {rotating ? 'Rotating Token Family...' : 'Execute RTR Exchange'}
          </button>
        </div>
      </div>

      {/* JWT Inspector */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Key size={18} color="#f59e0b" /> Active JWT Bearer Token Inspector
          </h3>
          <button className="btn-secondary" onClick={() => copyToClipboard(accessToken)} style={{ fontSize: '12px', padding: '6px 12px' }}>
            <Copy size={14} /> {copied ? 'Copied!' : 'Copy Access Token'}
          </button>
        </div>

        <div style={{ background: 'rgba(15, 23, 42, 0.9)', padding: '16px', borderRadius: '12px', overflowX: 'auto', border: '1px solid var(--border-color)' }}>
          <div style={{ fontSize: '11px', color: '#a5b4fc', fontWeight: '600', marginBottom: '8px', letterSpacing: '0.05em' }}>HEADER & CLAIMS PAYLOAD:</div>
          <code style={{ fontSize: '12px', color: '#34d399', wordBreak: 'break-all', display: 'block' }}>
            {accessToken ? accessToken : 'No active token'}
          </code>
        </div>
      </div>
    </div>
  );
};
