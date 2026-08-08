import React, { useState, useEffect } from 'react';
import api from '../api';
import { Activity, ShieldAlert, CheckCircle, XCircle, RefreshCw, Search } from 'lucide-react';

export const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [error, setError] = useState(null);

  const fetchAuditLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/audit/logs');
      setLogs(res.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch security audit logs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAuditLogs();
  }, []);

  const filteredLogs = logs.filter(l => 
    l.event_type.toLowerCase().includes(filter.toLowerCase()) ||
    l.status.toLowerCase().includes(filter.toLowerCase()) ||
    (l.user_email && l.user_email.toLowerCase().includes(filter.toLowerCase()))
  );

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }} className="animate-fade-in">
      <div className="glass-card" style={{ padding: '24px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Activity size={22} color="#10b981" /> Immutable Security Audit Logs
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '2px' }}>
            Append-only security records of authentication events, token revocations, and access attempts
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ position: 'relative' }}>
            <input
              type="text"
              className="input-field"
              placeholder="Search logs..."
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              style={{ paddingLeft: '36px', height: '38px', fontSize: '13px' }}
            />
            <Search size={16} color="#6b7280" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
          </div>
          <button className="btn-secondary" onClick={fetchAuditLogs} style={{ height: '38px', padding: '0 14px' }}>
            <RefreshCw size={14} /> Refresh
          </button>
        </div>
      </div>

      {error && (
        <div style={{ padding: '16px', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', borderRadius: '12px', color: '#fb7185', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <ShieldAlert size={20} /> {error}
        </div>
      )}

      <div className="glass-card table-container" style={{ padding: '0' }}>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Principal User</th>
              <th>Event Type</th>
              <th>Status</th>
              <th>Client IP</th>
              <th>Details Payload</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} style={{ textAlign: 'center', padding: '32px' }}>Querying audit store...</td></tr>
            ) : filteredLogs.length === 0 ? (
              <tr><td colSpan={6} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>No matching audit records.</td></tr>
            ) : (
              filteredLogs.map((log) => (
                <tr key={log.id}>
                  <td style={{ fontSize: '12px', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                  <td>
                    <span style={{ fontWeight: '600', fontSize: '13px' }}>{log.user_email || 'Anonymous'}</span>
                  </td>
                  <td>
                    <code style={{ fontSize: '12px', color: '#818cf8', background: 'rgba(99, 102, 241, 0.1)', padding: '2px 6px', borderRadius: '4px' }}>
                      {log.event_type}
                    </code>
                  </td>
                  <td>
                    {log.status === 'SUCCESS' ? (
                      <span className="badge badge-emerald"><CheckCircle size={10} /> SUCCESS</span>
                    ) : log.status === 'BLOCKED' ? (
                      <span className="badge badge-rose"><ShieldAlert size={10} /> BLOCKED</span>
                    ) : (
                      <span className="badge badge-amber"><XCircle size={10} /> FAILURE</span>
                    )}
                  </td>
                  <td><code style={{ fontSize: '12px', color: '#a5b4fc' }}>{log.ip_address}</code></td>
                  <td>
                    <pre style={{ fontSize: '11px', color: '#34d399', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {JSON.stringify(log.details)}
                    </pre>
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
