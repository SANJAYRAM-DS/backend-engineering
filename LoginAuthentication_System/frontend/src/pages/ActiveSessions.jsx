import React, { useState, useEffect } from 'react';
import api from '../api';
import { Monitor, Smartphone, Globe, ShieldOff, RefreshCw, CheckCircle2 } from 'lucide-react';

export const ActiveSessions = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState(null);

  const fetchSessions = async () => {
    setLoading(true);
    try {
      const res = await api.get('/sessions/active');
      setSessions(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleRevoke = async (sessionId) => {
    try {
      await api.post(`/sessions/revoke/${sessionId}`);
      setMsg(`Session ${sessionId} successfully revoked.`);
      fetchSessions();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRevokeAll = async () => {
    try {
      await api.post('/sessions/revoke-all');
      setMsg('All active sessions revoked across devices.');
      fetchSessions();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }} className="animate-fade-in">
      <div className="glass-card" style={{ padding: '24px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Monitor size={22} color="#06b6d4" /> Active Device Sessions
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '2px' }}>
            Track active user logins, IP addresses, and remote revocation triggers
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn-secondary" onClick={fetchSessions} style={{ padding: '8px 14px' }}>
            <RefreshCw size={14} /> Refresh
          </button>
          <button className="btn-primary" onClick={handleRevokeAll} style={{ background: 'linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)', boxShadow: '0 4px 14px 0 rgba(244, 63, 94, 0.3)' }}>
            <ShieldOff size={16} /> Revoke All Sessions
          </button>
        </div>
      </div>

      {msg && (
        <div style={{ padding: '12px 16px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '10px', color: '#34d399', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={18} /> {msg}
        </div>
      )}

      <div className="glass-card table-container" style={{ padding: '0' }}>
        <table>
          <thead>
            <tr>
              <th>Device & Client</th>
              <th>IP Address</th>
              <th>Status</th>
              <th>Last Active</th>
              <th style={{ textAlign: 'right' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} style={{ textAlign: 'center', padding: '32px' }}>Loading session store...</td></tr>
            ) : sessions.length === 0 ? (
              <tr><td colSpan={5} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>No active device sessions found.</td></tr>
            ) : (
              sessions.map((s) => (
                <tr key={s.id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <div style={{ padding: '6px', background: 'rgba(99, 102, 241, 0.15)', borderRadius: '6px', display: 'flex' }}>
                        <Globe size={16} color="#818cf8" />
                      </div>
                      <div>
                        <div style={{ fontWeight: '600', fontSize: '13px' }}>{s.device_type}</div>
                        <div style={{ fontSize: '11px', color: 'var(--text-muted)', maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {s.user_agent}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td><code style={{ fontSize: '12px', color: '#a5b4fc' }}>{s.ip_address}</code></td>
                  <td>
                    {s.is_active ? <span className="badge badge-emerald">Active</span> : <span className="badge badge-amber">Revoked</span>}
                  </td>
                  <td style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                    {new Date(s.last_activity_at).toLocaleString()}
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button className="btn-secondary" onClick={() => handleRevoke(s.id)} style={{ padding: '6px 12px', fontSize: '12px', color: '#fb7185' }}>
                      Revoke
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
